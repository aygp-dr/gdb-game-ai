(use-modules (gdb))

(define (inject-up)
  (execute "return 119"))  ; 'w' key

(register-command!
  (make-command "play-2048"
    #:invoke (lambda (self args from-tty)
               (execute "break getch")
               (execute "commands")
               (execute "silent") 
               (execute "guile (inject-up)")
               (execute "continue")
               (execute "end")
               (display "2048 auto-play enabled\n"))))
