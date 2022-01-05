import numpy as np
import cv2 as cv
import pandas as pd

img=cv.imread('before tensile test')
output=img.copy()

gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray=cv.medianBlur(gray,5)

circles=cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,25,param1=50,param2=30,minRadius=25,maxRadius=35)
detected_circles=np.uint16(np.around(circles))

for (x,y,r) in detected_circles[0,:]:
    cv.circle(output,(x,y),r,(0,255,0),2)
    cv.circle(output,(x,y),1,(0,0,255),2)
    
cv.imwrite("image/Circles.jpg",output,[int(cv.IMWRITE_JPEG_QUALITY),100])
cv.imshow('output',output)

P=circles[0]
l=len(P)
print("The number of circles：",l)

# prepare for data
data=circles.reshape((l,3))
data_df = pd.DataFrame(data)

# change the index and column name
data_df.columns = ['x','y','r']

avg=data_df["r"].mean()
print("average radius：",avg)
new=pd.DataFrame({'x':0,'y':0,'r':avg},index=[l]) 
data_df=data_df.append(new) 

# create and writer pd.DataFrame to excel
writer = pd.ExcelWriter('Circles_Excel.xlsx')
data_df.to_excel(writer,'page_1',float_format='%.5f')
writer.save()

cv.waitKey(0)
cv.destroyAllWindows()
