
import cv2
import numpy as np
from .Utils import *
def openCvFunction(imagePath):
    webCamFeed = True
    extension1 = imagePath[-4:]
    pathImage = imagePath
    cap = cv2.VideoCapture(0)
    cap.set(10,160)
    heightImg = 640
    widthImg  = 480
   # initializeTrackbars()
    count=0
    while True:
        img = cv2.imread(pathImage)
        img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
        imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
        thres=(90,200) # GET TRACK BAR VALUES FOR THRESHOLDS
        imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1])
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
    
        ## FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
        #cv2.imshow("hello",imgContours)
        cv2.imwrite("D:/PROJECTS/DocumentScanner/Project/imgCoontiiur"+str(count)+extension1,imgContours)
        # FIND THE BIGGEST COUNTOUR
        biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            print('hi')
            biggest=reorder(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
            imgBigContour = drawRectangle(imgBigContour,biggest,2)
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    
            #REMOVE 20 PIXELS FORM EACH SIDE
            imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))
    
            # APPLY ADAPTIVE THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
            imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
            imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
            imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
    
            # Image Array for Display
            imageArray = ([img,imgGray,imgThreshold,imgContours],
                        [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])
    
        else:
            print('else')
            imageArray = ([img,imgGray,imgThreshold,imgContours],
                        [imgBlank, imgBlank, imgBlank, imgBlank])
    
        # LABELS FOR DISPLAY
        lables = [["Original","Gray","Threshold","Contours"],
                ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]
    
        stackedImage = stackImages(imageArray,0.75,lables)
    
        cv2.imwrite("D:/PROJECTS/DocumentScanner/Project/myImage"+str(count)+extension1,imgWarpColored)
        imagePath2 = "D:/PROJECTS/DocumentScanner/Project/myImage"+str(count)+extension1
      
        count += 1
        break
    return imagePath2
 


