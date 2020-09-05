import cv2
import numpy as np
import CalciumAndOledUtil
import MainClass


class CropProcess():

    def __init__(self,loadedImage,index):
        self.image=loadedImage
        self.index= index

    def cropForCalcnadOledTest(self):
        self.originalImage = self.image.copy()
        print('self.orig:', self.originalImage)
        self.gray = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2GRAY)
        # edged = cv2.Canny(self.gray,55, 70)
        # cv2.imshow("edged", edged)

        # finding minimum and maximum value in the image
        naive = self.image.copy()
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(self.gray)
        cv2.circle(naive, maxLoc, 5, (180, 240, 0), 2)

        # cv2.namedWindow("Naive", cv2.WINDOW_NORMAL)
        # cv2.imshow("Naive", naive)

        print('minVal,maxVal', minVal, maxVal)

        # threshold image with detected values
        offset = (maxVal - minVal) * 0.42
        thresh = self.originalImage.copy()
        ret, thresh = cv2.threshold(thresh, minVal + offset, maxVal - offset, 0)
        # cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
        # cv2.imshow("Thresh", thresh)
        thresh1 = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

        binary = cv2.adaptiveThreshold(thresh1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 5)
        print('binarysize:', binary.size)
        height = np.size(binary, 0)
        width = np.size(binary, 1)
        print('width*height,', width, height)

        # cv2.namedWindow("AdaptThresh", cv2.WINDOW_NORMAL)
        # cv2.imshow("AdaptThresh", binary)
        # Detect Contours

        img1 = self.originalImage.copy()
        contsearch = binary.copy()
        contours, hierarchy = cv2.findContours(contsearch, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        CalciumAndOledUtilObj = CalciumAndOledUtil.CalciumAndOledUtil()
        (cnts, boundingBoxes) = CalciumAndOledUtilObj.sort_contours(self, cnts)
       # (cnts, boundingBoxes) = CalciumAndOledUtil.sort_contours(self,cnts)



        cnt = cnts[1]
        print "length of contours is", len(contours)
        print "length of cnt is", len(cnt)
        print "length of hierarchy is", len(hierarchy)

        cv2.drawContours(img1, [cnt], -1, (128, 255, 0), 3)
        # cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
        # cv2.imshow("Contours", img1)



        # select only the detected contour marked in green

        lower = np.array([128, 255, 0])
        upper = np.array([128, 255, 0])
        mask = cv2.inRange(img1, lower, upper)
        green = cv2.bitwise_and(img1, img1, mask=mask)

        # cv2.namedWindow("green", cv2.WINDOW_NORMAL)
        # cv2.imshow("green", green)


        # compute contours as binary image

        thresh2 = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
        binary2 = cv2.adaptiveThreshold(thresh2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
        # cv2.namedWindow("ContoursGreenAdaptive", cv2.WINDOW_NORMAL)
        # cv2.imshow("ContoursGreenAdaptive", binary2)


        # Detect Contours again

        img2 = binary2.copy()
        # img2 = thresh2.copy()
        contsearch2 = img2
        contours2, hierarchy2 = cv2.findContours(contsearch2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cnts2 = sorted(contours2, key=cv2.contourArea, reverse=True)[:5]
        jonty = CalciumAndOledUtil.CalciumAndOledUtil()
        (cnts2, boundingBoxes) = jonty.sort_contours(self, cnts2)
       # (cnts2, boundingBoxes) = CalciumAndOledUtil.sort_contours(cnts2)

        # detect outer shape of image

        cnt1 = cnts2[0]
        outer = self.image.copy()
        print("outer points is", cnt1)
        cv2.drawContours(outer, [cnt1], -1, (128, 255, 0), 1)

        # cv2.namedWindow("OuterContours", cv2.WINDOW_NORMAL)
        # cv2.imshow("OuterContours", outer)

        # detect boxshape

        imgcontours2 = self.image.copy()
        cnt2 = cnts2[1]
        print "length of contours is", len(contours2)
        print "length of cnt is", len(cnt2)
        print "length of hierarchy is", len(hierarchy2)
        cv2.drawContours(imgcontours2, [cnt2], -1, (128, 255, 0), 3)

        # cv2.namedWindow("Contours2", cv2.WINDOW_NORMAL)
        # cv2.imshow("Contours2", imgcontours2)

        # find best fit rectangle with minimum area

        rectpic = imgcontours2.copy()
        # print('rectpic:',rectpic)
        # rect = cv2.minAreaRect(cnt2)
        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        print("boxpoints is", box)
        cv2.drawContours(rectpic, [box], 0, (0, 0, 255), 2)

        # cv2.namedWindow("Boxpic", cv2.WINDOW_NORMAL)
        # cv2.imshow("Boxpic", rectpic)

        # calculate area and image size

        imsize = cv2.contourArea(cnt1)
        print("area in image =", imsize)
        boxarea = cv2.contourArea(box)
        print("area in box =", boxarea)
        areapart = boxarea / float(imsize)
        print("percentage of box in image =", areapart * 100)
        contoursize = cv2.contourArea(cnt)
        print("area in contour =", contoursize)
        contourpart = (boxarea - contoursize) / float(boxarea)
        print("percentage of contour in box =", contourpart * 100)

        # Writing output results in txt file

        output = open('C:\Users\Sandesh Chand\Desktop\\test_data_{}.txt'.format(self.index), 'w')
        # output = open('C:\Users\chand.s\Desktop\destination_folder\\test_data.txt', 'a')


        output.write(
            "[{}]\t[{}]\t[{}]\t[{}]\t[{}]\t".format("Image_Area ", "Box_Area ", "% box in image", "Contour_Area ",
                                                    "%Degradation in box"))
        output.write("\n")
        output.write(
            "[{}]\t[{}]\t[{}]\t[{}]\t[{}]\t".format(imsize, boxarea, areapart * 100, contoursize, contourpart * 100))
        output.close()


        # execute
        self.imgwarp = self.image.copy()
        San = CalciumAndOledUtil.CalciumAndOledUtil()
        self.cropImage = San.four_point_transform(self,self.imgwarp, box)
        #self.image = CalciumAndOledUtil.four_point_transform(self.imgwarp, box)
        print('self.image',  self.cropImage.shape)
        cv2.namedWindow("Crop_Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Crop_Image",  self.cropImage)
        cv2.imwrite('C:\\Users\\chand.s\\Desktop\\destination_folder\\crop_Image\\cropImage_{}.jpg'.format(self.index),
                    self.cropImage)
        return self.cropImage
        # self.grayscale_Image = cv2.cvtColor( self.cropedpic, cv2.COLOR_RGB2GRAY)
        #self.grayImage("FromCalciumTest")



