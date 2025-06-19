;;; 2048-ai.scm - Simple but effective 2048 AI

(use-modules (gdb))

;; Global to store game state
(define *board-address* #f)
(define *last-board* (make-vector 16 0))

;; Read board from memory
(define (read-board addr)
  (let ((board (make-vector 16)))
    (do ((i 0 (+ i 1)))
        ((>= i 16))
      (let* ((inferior (current-inferior))
             (bytes (inferior-read-memory inferior (+ addr (* i 4)) 4)))
        (vector-set! board i (bytevector-s32-native-ref bytes 0))))
    board))

;; Display board
(define (show-board board)
  (format #t "~%Current board:~%")
  (do ((row 0 (+ row 1)))
      ((>= row 4))
    (do ((col 0 (+ col 1)))
        ((>= col 4))
      (format #t "~5d" (vector-ref board (+ (* row 4) col))))
    (format #t "~%")))

;; Check if move is possible
(define (can-move? board direction)
  (case direction
    ((up) (can-move-vertical? board -4))
    ((down) (can-move-vertical? board 4))
    ((left) (can-move-horizontal? board -1))
    ((right) (can-move-horizontal? board 1))
    (else #f)))

(define (can-move-vertical? board offset)
  (let ((start (if (< offset 0) 4 0))
        (end (if (< offset 0) 16 12)))
    (let loop ((i start))
      (if (>= i end)
          #f
          (let ((curr (vector-ref board i))
                (next-idx (+ i offset)))
            (if (and (> curr 0)
                     (or (= (vector-ref board next-idx) 0)
                         (= (vector-ref board next-idx) curr)))
                #t
                (loop (+ i 1))))))))

(define (can-move-horizontal? board offset)
  (let loop ((row 0))
    (if (>= row 4)
        #f
        (let loop2 ((col (if (< offset 0) 1 0)))
          (if (>= col (if (< offset 0) 4 3))
              (loop (+ row 1))
              (let* ((idx (+ (* row 4) col))
                     (curr (vector-ref board idx))
                     (next-idx (+ idx offset)))
                (if (and (> curr 0)
                         (or (= (vector-ref board next-idx) 0)
                             (= (vector-ref board next-idx) curr)))
                    #t
                    (loop2 (+ col 1)))))))))

;; Count empty cells
(define (count-empty board)
  (let loop ((i 0) (count 0))
    (if (>= i 16)
        count
        (loop (+ i 1)
              (if (= (vector-ref board i) 0)
                  (+ count 1)
                  count)))))

;; Simple AI strategy
(define (choose-move board)
  ;; Priority: down > right > left > up
  ;; This keeps tiles in lower rows and creates merging opportunities
  (cond
   ((can-move? board 'down) 's)   ; down
   ((can-move? board 'right) 'd)  ; right
   ((can-move? board 'left) 'a)   ; left
   ((can-move? board 'up) 'w)     ; up
   (else 'q)))                     ; quit if no moves

;; Main AI function
(define (ai-move)
  (if *board-address*
      (let* ((board (read-board *board-address*))
             (move (choose-move board)))
        (show-board board)
        (format #t "AI chooses: ~a~%" move)
        (char->integer move))
      (begin
        (format #t "Board address not set!~%")
        (char->integer #\w))))

;; Register commands
(register-command!
 (make-command "2048-find"
               #:command-class COMMAND_USER
               #:doc "Find 2048 board in memory"
               #:invoke
               (lambda (self args from-tty)
                 (execute "break main")
                 (execute "run")
                 (format #t "Searching for board...~%")
                 ;; This is a placeholder - need to implement search
                 (format #t "Use 'find' command to locate board~%"))))

(register-command!
 (make-command "2048-set-addr"
               #:command-class COMMAND_USER  
               #:doc "Set board address: 2048-set-addr 0xADDRESS"
               #:invoke
               (lambda (self args from-tty)
                 (set! *board-address* (string->number args 0))
                 (format #t "Board address set to: ~x~%" *board-address*))))

(register-command!
 (make-command "2048-auto"
               #:command-class COMMAND_USER
               #:doc "Enable AI auto-play"
               #:invoke
               (lambda (self args from-tty)
                 (execute "break wgetch")
                 (execute "commands")
                 (execute "silent")
                 (execute "guile (define result (ai-move))")
                 (execute "return $result")
                 (execute "end")
                 (format #t "AI auto-play enabled!~%"))))
