;; hanoi.lisp
;; recursively solved the towers of hanoi problem

;Generating tower
(defun range (n)
  (loop for x from 1 to n collect x))

(defun create-towers (n)
  (setf towers (list (range n) nil nil)))

;Printing tower
(defun max-length (tower-list)
  (if (null tower-list)
      0
      (max (length (first tower-list)) (max-length (rest tower-list)))))

(defun print-towers (tower-list)
  (let ((max-height (- (max-length tower-list) 1)))
    (loop for height from max-height downto 0 do
	 (loop for tower in towers do
	      (if (null (nth height tower))
		  (format t "                    ") ;twenty spaces
		  (let ((disk-size (nth (- (length tower) height 1) tower)))
		    (dotimes (c disk-size)
		      (format t "*"))
		    (dotimes (c (- 20 disk-size))
		      (format t " ")))))
	 (format t "~%")))
  (format t "+-------------------+-------------------+-------------------~%~%"))

;Solving puzzle
(defun find-third-tower (tower1 tower2)
  (first (set-difference '(0 1 2) (list tower1 tower2))))

(defun move-tower (from to index)
  "ex: (move-tower 1 2 3) moves the top 4 elements of the
   second tower to the third tower"
  (if (= 0 index)
      (progn
	(push (first (nth from towers)) (nth to towers))
	(setf (nth from towers) (rest (nth from towers)))
	(print-towers towers))
      (let ((third-tower (find-third-tower from to)))
	(move-tower from third-tower (- index 1)) ; move the top n-1 disks to the other tower
	(move-tower from to 0) ; moves the bottom disk to the new tower
	(move-tower third-tower to (- index 1))))) ; move disks from the other tower to the new tower

;Concise form
(defun solve (n)
  (create-towers n)
  (move-tower 0 2 (- n 1)))
