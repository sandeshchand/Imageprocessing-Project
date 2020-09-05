import Tkinter as tk
import os
import tkFileDialog
import ttk
from Tkinter import *
from Tkinter import Tk, RIGHT
from ttk import Button

import cv2
import numpy as np
from PIL import Image,ImageTk
from matplotlib import pyplot as plt
from numpy import array
from skimage.filters import threshold_adaptive
import CalciumAndOled
import GrayImage
import ExecuteTestProcess


class MainClass(tk.Frame):
  def __init__(self, master=None):

        tk.Frame.__init__(self, master)
        self.master = master
        self.grid()
        self.createWidgets()

        self.refPt= []
        self.cropping = FALSE
        self.item = None

        self.image= None
        self.cv_img = None
        self.roi = None
        self.grayscale_Image = None
        self.grayscale_Image1= None

        self.index = None
        self.threshold_Image= None
        self.invert_Image= None
        self.autoCanny=None
        self.contour_Image= None
        self.erosion= None
        self.imwrap= None
        self.croppedgray_Image= None
        self.counters=None
        self.hist=None
        self.erosion1= None
        self.area = {}
        self.area[0]= 0.0
        self.crop_Image= None

       # self.area = []
        self.cx= []

        #self.cx[0]= self.cx

        self.cy= []
       # self.cy[0] = self.cy
        self.hullarea=[]

        # Set the dimensions of the Main window
        master.minsize(width=400, height=600)
        master.maxsize(width=600, height=800)
        #self.combobox02 ='Guassianblur'
  #Create necessary GUI things

  def createWidgets(self):
        #Changes Images
        self.quitButton = tk.Button(self, text='Next',width=10,height =5,
                                    fg="red", command=self.quit)
        self.quitButton.pack( side=LEFT,padx=10, pady=10 )
        #self.quitButton.grid(row=0,column=2, rowspan=2, sticky=NSEW)

        self.loadButton1 = tk.Button(self, text='loadImage',width=10,height =5,
                                command=self.load_Image)

        self.loadButton1.pack(side=LEFT, padx=10, pady=10)
        #self.loadButton1.grid(row=1, column=1, sticky=SE)

        self.deleteButton = tk.Button(self,text='Delete', width=10,height =5,
                          command=self.deleteImage)
        self.deleteButton.pack(side=LEFT,padx= 10, pady= 10)
        #self.deleteButton.grid(row=2,column=2, rowspan=2, sticky=NE)
        self.Oled_button = tk.Button(self, text='Oled_test', width=10, height=5,
                                      command=self.Oled_button)
        self.Oled_button.pack(side=RIGHT,padx=10, pady=10)

        self.canvas = tk.Canvas(root, width=400, height=400, relief="raised",bg="white",cursor= "cross")

        self.canvas.pack(expand=YES, fill=BOTH,anchor='w')

        self.testButton = Button(root, text="Ca-Test", width=10,
                                 command=self.calcium_Test)
        self.testButton.pack(side=TOP, padx=10, pady=10)


        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.pack(anchor='w')



        self.cropButton = Button(root, text="Crop", width=10,
                                 command=self.crop_image)
        self.cropButton.pack(side=RIGHT,padx=10, pady=10)

        self.extraButton = Button(root,text= "Grayscale", width= 10,
                                  command= self.grayImage)
        self.extraButton.pack(padx= 10, pady= 10)


        self.testButton= Button(root,text= "Ca-Test",width=10,
                                command=self.calcium_Test)

        self.testButton.pack(side=TOP,padx=10,pady=10)


        self.combobox_value = StringVar()

        self.combobox= ttk.Combobox(root,width=10,values=['Guassianblur','Medianblur','biletralblur'],
                                    textvariable=self.combobox_value,state='readonly')

        self.combobox.current(0)

        self.combobox.bind("<<ComboboxSelected>>",self.comboboxblurrUpdate)
        self.combobox.pack(padx=10, pady=10)
        '''
        self.combobox_thresholdlist= StringVar()
        self.combobox_threshold= ttk.Combobox(root,width=10,values=['AdaptiveGuassian','GlobalThresholding','Otsu','Scikitthreshold'],
                                textvariable=self.combobox_thresholdlist,state= 'readonly')

        self.combobox_threshold.current(0)
        self.combobox_threshold.bind("<<ComboboxSelected>>",self.comboboxthreshold_Update)
        self.combobox_threshold.pack(padx=10, pady= 10)
        '''

# Load Image from directory
  def load_Image(self):
    # mypath = os.path.join('C:\\Users\\chand.s\\Desktop\\Imagtedir\\fresh_img')
    mypath = tkFileDialog.askdirectory(parent=root, initialdir='C:\\Users\\chand.s\\Desktop\\Imagtedir\\')

    # for item in os.listdir(mypath):
    for self.index, item in enumerate(os.listdir(mypath), start=1):

        print("item index", item, self.index)

        try:
            # this could be more correctly done with os.path.splitext
            self.image = cv2.imread(os.path.join(mypath, item))
            print  ("image_size", self.image.size)
            height = np.size(self.image, 0)
            width = np.size(self.image, 1)
            print('width*height,', width, height)
            print('Image:', self.image.shape)

            # Rearrang the color channel
            b, g, r = cv2.split(self.image)
            self.images = cv2.merge((r, g, b))

            # Convert the Image object into a TkPhoto object
            self.image1 = Image.fromarray(self.images)
            image = self.image1.resize((400, 400), Image.ANTIALIAS)
            print("Image", image)
            photo = ImageTk.PhotoImage(image=image)
            print(photo)
            self.canvas.create_image(0, 0, image=photo, anchor=NW)

            # assigned the photo to the canvas object
            # self.canvas.photo = photo
            self.canvas.config = photo
            self.cv_img = array(image)
            print("photo", self.cv_img)

            cv2.namedWindow("Original_Image", cv2.WINDOW_NORMAL)
            cv2.imshow("Original_Image", self.image)
            height = np.size(self.image, 0)
            width = np.size(self.image, 1)
            print('width*height,', width, height)
            print('Image:', self.image)
            # self.grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            self.canvas.mainloop()




        except ValueError, Arguemnt:
            print 'Invalid photo', Arguemnt

#



# Delete image in Canvas window


  def deleteImage(self):
         self.canvas.delete("all")
         self.resetCanvas()
    # self.canvas.photo = " "

  def calcium_Test(self):
      test=ExecuteTestProcess.Execute('TestForCalcium',self.image,self.index)
      test.executeAllStep()


  def Oled_button(self):
      test = ExecuteTestProcess.Execute('TestForOled', self.image, self.index)
      test.executeAllStep()


  def grayImage(self):
      test = ExecuteTestProcess.Execute('TestForMicroscopic', self.image, self.index)
      test.executeAllStep()
     # code= GrayImage.GrayImage(self.image,self.index)
     # code.grayImage()




      # Mouse click event for cropping
  def on_button_press(self, event):
          global refPt

          self.x = event.x
          self.y = event.y
          self.refPt = [(self.x, self.y)]

      # Mouse click event for cropping
  def on_button_release(self, event):
          global refPt
          x0, y0 = (self.x, self.y)
          x1, y1 = (event.x, event.y)
          self.refPt.append((x1, y1))
          # self.canvas.create_rectangle(x0,y0,x1,y1, outline="green")
          self.canvas.create_rectangle(self.refPt[0], self.refPt[1], outline="green")


 #Crop the image from the original image
  def crop_image(self):

        if len(self.refPt)== 2:

                print(self.refPt[0][1],self.refPt[1][1], self.refPt[0][0],self.refPt[1][0])
                self.roi = self.cv_img[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]

                print("Jonty",self.roi)
                cv2.imshow("ROI",self.roi)
                cv2.waitKey(5)

                cv2.imwrite("C:\\Users\\chand.s\\Desktop\\crop.jpg", self.roi)


                # Performing blurr filtering operation on input  greyscale images

  def comboboxblurrUpdate(self, event):
      self.combobox_blurrtype = self.combobox_value.get()
      print("combobox:", self.combobox_blurrtype)

      if self.combobox_blurrtype == 'Guassianblur':
          if (self.grayscale_Image2 == None):
              print('couldnot load the image,please wait!')
          else:
              height = np.size(self.grayscale_Image2, 0)
              width = np.size(self.grayscale_Image2, 1)
              print('width*height,', width, height)
              '''
              if (callFrom == None):
                  print('This is microscopic Image')
                  self.grayscale_Image1 = cv2.GaussianBlur(self.grayscale_Image2, (5, 5), 0)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("Guassianblur", cv2.WINDOW_NORMAL)
                  cv2.imshow("Guassianblur", self.grayscale_Image1)
              elif (callFrom == "FromCalciumTest"):
                  print('This is Optical calciumTest Image')
                  self.grayscale_Image1 = cv2.GaussianBlur(self.grayscale_Image2, (5, 5), 0)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("Guassianblur", cv2.WINDOW_NORMAL)
                  cv2.imshow("Guassianblur", self.grayscale_Image1)
              elif (callFrom == "FromOledTest"):
                  print('This is Oled Image')
                  self.grayscale_Image1 = cv2.GaussianBlur(self.grayscale_Image2, (5, 5), 0)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("Guassianblur", cv2.WINDOW_NORMAL)
                  cv2.imshow("Guassianblur", self.grayscale_Image1)

      elif self.combobox_blurrtype == 'Medianblur':
          if (self.grayscale_Image2 == None):
              print('couldnot load the image,please wait!')
          else:
              height = np.size(self.grayscale_Image1, 0)
              width = np.size(self.grayscale_Image1, 1)
              print('width*height,', width, height)
              if (callFrom == None):
                  print('This is microscopic Image')
                  self.grayscale_Image1 = cv2.medianBlur(self.grayscale_Image2, 15)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("Medianblur", cv2.WINDOW_NORMAL)
                  cv2.imshow("Medianblur", self.grayscale_Image1)
              elif (callFrom == "FromCalciumTest"):
                  print('This is Optical calciumTest Image')
                  self.grayscale_Image1 = cv2.medianBlur(self.grayscale_Image2, 15)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("Medianblur", cv2.WINDOW_NORMAL)
                  cv2.imshow("Medianblur", self.grayscale_Image1)
              elif (callFrom == "FromOledTest"):
                  self.grayscale_Image1 = cv2.medianBlur(self.grayscale_Image2, 15)
                  cv2.namedWindow("Medianblur", cv2.WINDOW_NORMAL)
                  cv2.imshow("Medianblur", self.grayscale_Image1)



      elif self.combobox_blurrtype == 'biletralblur':
          if (self.grayscale_Image2 == None):
              print('couldnot load the image,please wait!')
          else:
              height = np.size(self.grayscale_Image1, 0)
              width = np.size(self.grayscale_Image1, 1)
              if (callFrom == None):
                  print('This is microscopic Image')
                  self.grayscale_Image1 = cv2.bilateralFilter(self.grayscale_Image2, 9, 75, 75)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("bilateralblur", cv2.WINDOW_NORMAL)
                  cv2.imshow('bilateralblur', self.grayscale_Image1)
              elif (callFrom == "FromCalciumTest"):
                  print('This is optical calcium test')
                  self.grayscale_Image1 = cv2.bilateralFilter(self.grayscale_Image2, 9, 75, 75)
                  print('self.grayscale_Image1:', self.grayscale_Image1)
                  cv2.namedWindow("bilateralblur", cv2.WINDOW_NORMAL)
                  cv2.imshow('bilateralblur', self.grayscale_Image1)

              elif (callFrom == "FromOledTest"):
                  self.grayscale_Image1 = cv2.bilateralFilter(self.grayscale_Image2, 9, 75, 75)
                  cv2.namedWindow("bilateralblur", cv2.WINDOW_NORMAL)
                  cv2.imshow('bilateralblur', self.grayscale_Image1)



                  # Performing threshold filtering operation on input images
              '''
  cv2.destroyAllWindows()

if __name__ == '__main__':
     root = Tk()

   #root.geometry("800x600+100+100")
     app = MainClass(root)

     app.pack()
   #app.master.geometry("800x600+300+300")
     app.master.title('Image_window')
  #app.master.configure(background= 'black')
     app.mainloop()


