;; Emacs GDB configuration for fibonacci debugging

(require 'gdb-mi)

;; Configure GDB
(setq gdb-many-windows t)
(setq gdb-show-main t)
(setq gdb-thread-buffer-verbose-names t)
(setq gdb-window-configuration 'gdb-many-windows)

;; Custom layout function
(defun my-gdb-setup ()
  "Custom GDB window layout"
  (interactive)
  (gdb-many-windows)
  ;; Additional customization
  (split-window-horizontally)
  (other-window 1)
  (gdb-set-window-buffer 'gdb-locals-buffer)
  (other-window 1)
  (gdb-set-window-buffer 'gdb-stack-buffer))

;; Keybindings
(global-set-key (kbd "C-c g d") 'gdb)
(global-set-key (kbd "C-c g l") 'my-gdb-setup)

;; Function to debug fibonacci with preset breakpoints
(defun debug-fibonacci (n)
  "Start debugging fibonacci with argument N"
  (interactive "nFibonacci argument: ")
  (let ((program (expand-file-name "./fibonacci")))
    (gdb (format "gdb -i=mi %s" program))
    (sleep-for 1)  ; Wait for GDB to start
    (gdb-send-string (format "break fib_recursive\n"))
    (gdb-send-string (format "break fib_memoized\n"))
    (gdb-send-string (format "run %d\n" n))))
