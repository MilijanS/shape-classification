-Python 3.5.2
-Numpy 1.11.3+mkl
-Scipy 0.18.1
-Scikit-learn 0.18.1
-OpenCV 3.2.0

Packages downloaded from Unofficial Windows Binaries for Python Extension Packages page at:
http://www.lfd.uci.edu/~gohlke/pythonlibs/

Preinstalled Anaconda/Miniconda repositories might not work.

The classifier is initialized with four basic shapes - circle, square, triangle and star and is able to identify multiple instances of these shapes drawn on the canvas. New shapes are learned by clearing the canvas, inputing the shape name, drawing one specific shape and pressing the learn shape button. Repeat for better accuracy. Make sure the drawn shapes are relatively closed(OpenCV contoure detection hierarchy needs tweaking; a heart shape would be a good candidate, but non disjoint open shapes such as  letters M, W, S are also fine)




