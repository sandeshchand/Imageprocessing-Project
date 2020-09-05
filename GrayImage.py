import cv2
import numpy as np
from matplotlib import pyplot as plt


class GrayImageProcedures():
# Conversion of RGB image to Gray scale Image and performing various functions

    def __init__(self, image,index,processFlag):
        self.ProcessFlag=processFlag
        self.image = image
        self.index = index
        self.area= None
        self.area = {}
        self.area[0] = 0.0

    def grayImage(self):

        self.original_Image= self.image.copy()

        if(self.image == None):
           print('couldnot load the image,please wait!')
        else:
             if ( self.ProcessFlag== "TestForMicroscopic"):

                #Original is converted to  8 bit gray scale image
               self.grayscale_Image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
               cv2.namedWindow("Gray_image", cv2.WINDOW_NORMAL)
               cv2.imshow('Gray_image', self.grayscale_Image)
               print('Gray_image', self.grayscale_Image)
               print('self.grayscale_Image:', self.grayscale_Image.shape)

                # Saving Gray_image in destination_folder
               cv2.imwrite('C:\\Users\\chand.s\\Desktop\\destination_folder\\Grayimage_{}.jpg'.format(self.index),
                    self.grayscale_Image)



             # Applying Guassianblur filter on Grayscalse image

               self.blurrImage = cv2.GaussianBlur(self.grayscale_Image, (5, 5), 0)
               print('self.blurrImage', self.blurrImage)
               cv2.namedWindow("Guassianblur", cv2.WINDOW_NORMAL)
               cv2.imshow("Guassianblur",self.blurrImage)

               #Applying adaptive threshold filter on blurrImage
               self.threshold_Image = cv2.adaptiveThreshold(self.blurrImage , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                        cv2.THRESH_BINARY, 11, 2)
               cv2.namedWindow("Adaptive Guassian Thresholding", cv2.WINDOW_NORMAL)
               cv2.imshow('Adaptive Guassian Thresholding', self.threshold_Image)

               cv2.imwrite(
               'C:\\Users\\chand.s\\Desktop\\destination_folder\\MicroscopicthresholdImage_{}.jpg'.format(self.index),
               self.threshold_Image)
               self.final_Image = cv2.bitwise_not(self.threshold_Image)
               cv2.namedWindow('InvEroded_Image', cv2.WINDOW_NORMAL)
               cv2.imshow('InvEroded_Image', self.final_Image)

               # Performing contouring for area calculation
               (cnts, _) = cv2.findContours(self.final_Image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
               output = open(
                    'G:\Thesis_work\data_sheet\\test_datasheet_{}.csv'.format(self.index),
                    'a')
               output.write("[{}],[{}],[{}],[{}],[{}],[{}],[{}]".format("Total no. defect","Area of defects ", "mean_value ", "median_value",
                                                           "sd_Value ", "perimeter","Total_Defect"))
               output.write("\n")
               # loop over the counters and calculating the area of defects

               counter=1
               for (i, c) in enumerate((cnts)):
                  global area
                  Total_area = []
                  # Calculate the area of defects
                  self.area[i] = cv2.contourArea(c)
                  if (self.area[i] > 0.0 and self.area[i] < 12345.0):
                        print('Total no  defects area:',len(self.area))
                        print('Area of defects', self.area[i])
                        print('Total defects area:', sum(self.area.values()))

                 # Calculating ratio of contour area to bounding rectangle area
                  x, y, w, h = cv2.boundingRect(c)
                  print('positin of rec', x, y, w, h)

                  #Calculating Aspect ratio Width/Height
                  aspect_ratio= float(w)/h
                  print('aspect_ratio:',  aspect_ratio)

                  image = self.final_Image.copy()

                  # Calculating Mean value of Defetcive regions
                  rect = image[y:y + h, x:x + w]
                  print('mean_value:', rect.mean())
                  print('median_Value:', np.median(rect))
                  print('sd_Value:', np.std(rect))

                  rect_area = w * h
                  Extend_Ratio = float(self.area[i]) / rect_area
                  print('Extend_Ratio', Extend_Ratio)

                  # perimeter of defect object
                  self.perimeter = cv2.arcLength(c, True)
                  print('perimeter', self.perimeter)

                   #Calcualting Hull area
                  hull = cv2.convexHull(c)
                  self.hullarea = cv2.contourArea(hull)
                  if (self.hullarea != 0):
                     self.solidity = float( self.area[i]) /self.hullarea
                     print('solidity',self.solidity)

                  # Calcaulate Center points of defects
                  self.Moment = cv2.moments(c)
                  if (self.Moment['m00'] != 0):
                        self.cx = int(self.Moment['m10'] / self.Moment['m00'])
                        self.cy = int(self.Moment['m01'] / self.Moment['m00'])
                        print('self.cx,self.cy', self.cx, self.cy)

                  #Calculating the circularity
                  if (self.perimeter != 0):
                     self.circularity = 4 * 3.1416 * self.area[i] / (self.perimeter * self.perimeter)
                     print('circularity:', self.circularity)

                     if(self.solidity < 0.5 or self.circularity < 0.3 ):
                         print('The defect is scratch')

                     else:
                         print('The defect is pinhole')

                        # Writing output results in txt file
                         '''
                         output.write("[{}],[{}],[{}],[{}],[{}],[{}],[{}]".format(len(self.area),self.area[i], rect.mean(), np.median(rect), np.std(rect),
                                                                        self.perimeter, sum(self.area.values())))
                         '''
                         if (self.area[i] > 0.0 and self.area[i] < 12345.0):
                             output.write(
                             "[{}],[{}],[{}],[{}],[{}],[{}],[{}]".format(counter, self.area[i], rect.mean(),
                                                                         np.median(rect), np.std(rect),
                                                                         self.perimeter, sum(self.area.values())))
                         output.write("\n")
                         counter=counter+1
               output.close()

                 # draw contour for confimation in output image
               contourimage = self.threshold_Image.copy()
               cv2.drawContours(contourimage, cnts, -1, (125, 255, 0), 2)
               cv2.namedWindow('Drawcontour', cv2.WINDOW_NORMAL)
               cv2.imshow('Drawcontour', contourimage)
               cv2.imwrite(
                    'C:\\Users\\chand.s\\Desktop\\destination_folder\crop_Image\Drawcontour{}.jpg'.format(self.index),
                    contourimage)



                # function call for different blurr type filters
               self.hist = cv2.calcHist([self.grayscale_Image], [0], None, [256], [0, 256]);

                 # print  enumerate(self.hist)
               plt.title('Histogram for Grayscale image picture')
               plt.xlabel('Gray value')
               plt.ylabel('Number of pixels')
               plt.hist(self.grayscale_Image.ravel(), 256, [0, 256]);
               plt.show()










