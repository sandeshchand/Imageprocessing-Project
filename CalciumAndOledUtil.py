import cv2
import  numpy as np


class CalciumAndOledUtil():
    def __init__(self):
        print('Constructor')

    @staticmethod
    def sort_contours(self,cnts):
        # initialize the reverse flag and sort index
        reverse = False
        i = 1
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
          # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)



    # crop image to boxsize and rotate
     # define funtion to order points in detected box

    @staticmethod
    def order_points(self,pts):
       rect = np.zeros((4, 2), dtype="float32")
       s = pts.sum(axis=1)
       rect[0] = pts[np.argmin(s)]
       rect[2] = pts[np.argmax(s)]

       diff = np.diff(pts, axis=1)
       rect[1] = pts[np.argmin(diff)]
       rect[3] = pts[np.argmax(diff)]
       return rect
# define function to perform four point transformation
    @staticmethod
    def four_point_transform(self,image, pts):
       rect = CalciumAndOledUtil.order_points(self,pts)
       (tl, tr, br, bl) = rect
       widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
       widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
       maxWidth = max(int(widthA), int(widthB))
       heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
       heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
       maxHeight = max(int(heightA), int(heightB))
       dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
       M = cv2.getPerspectiveTransform(rect, dst)
       warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
       return warped

