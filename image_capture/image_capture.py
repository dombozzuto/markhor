from cv2 import *
cam = VideoCapture(0)
s, img = cam.read()
if s:
    namedWindow("cam-test", CV_WINDOW_AUTOSIZE)
    imshow("cam-test", img)
    waitKey(0)
    destroyWindow("cam-test")
    imwrite("file.jpg", img)
