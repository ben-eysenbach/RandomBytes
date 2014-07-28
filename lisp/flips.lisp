(defun my-last (lst)
  (first (last lst)))

(defun my-random (n)
  (if (= n 0)
      0
      (random n)))

(defun all-but-last (lst)
  (subseq lst 0 (- (length lst) 1)))

(defun random-stack (n)
  (setf lst nil)
  (loop for x from 1 to n do
       (let ((m (my-random (length lst))))
	 (setf lst (append (subseq lst 0 m) (list x) (subseq lst m)))))
  lst)

(defun check (lst)
  (equal lst (remove-duplicates lst)))

(defun find-place (lst)
  (if (null lst)
      nil
      (let ((m (apply #'max lst)))
	(if (= m (my-last lst))
	    (find-place (all-but-last lst))
	    (position m lst)))))

(defun flip-to-front (n lst)
  (setf n (+ n 1)) ;subseq doesn't include last item
  (append (reverse (subseq lst 0 n)) (subseq lst n)))

(defun flip-to-back (lst)
  (let ((n (first lst)))
    (append (reverse (subseq lst 0 n)) (subseq lst n))))

(defun run (lst c)
  (if (check lst)
  (if (equal (sort (copy-list lst) #'<) lst)
      c
      (let ((n (find-place lst)))
	(run (flip-to-back (flip-to-front n lst)) (+ c 1))))))

(defun repeated-run (n)
  (loop do
       (let ((lst (random-stack n)))
	 (print (run lst 0)))))
