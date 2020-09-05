
import GrayImage
import CalciumAndOled
import ImageProcessing
class Execute:
    def __init__(self,flagTestFor,LoadedImage,Index):
        self.flagTestFor=flagTestFor
        self.LoadedImage=LoadedImage
        self.index=Index
    def executeAllStep(self):
        if(self.flagTestFor=="TestForCalcium" or self.flagTestFor=="TestForOled" ):
            cropProcessObj= CalciumAndOled.CropProcess(self.LoadedImage,self.index)
            ImageAfterCropped=cropProcessObj.cropForCalcnadOledTest()
            grayImageProceduresObj=GrayImage.GrayImageProcedures(ImageAfterCropped,self.index,self.flagTestFor)
            grayImageProceduresObj.grayImage()

        if (self.flagTestFor == "TestForMicroscopic"):
            grayImageProceduresObj = GrayImage.GrayImageProcedures(self.LoadedImage, self.index,self.flagTestFor)
            grayImageProceduresObj.grayImage()
            #grayImageProceduresObj = ImageProcessing.Microscopic_Image(self.LoadedImage, self.index,self.flagTestFor)
            #grayImageProceduresObj.grayImageTask()