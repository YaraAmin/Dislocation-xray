
# coding: utf-8

# In[ ]:


##import libraries
import cv2
import numpy as np
import math

#calc and Display contours areas function
#load img from pc
img=cv2.imread("MURA/Bone images annotation/i.png",0)
#small the image to its 25size
# img = cv2.resize(img,None,fx=.25,fy=0.25)
cv2.imshow("original",img)

#detect circle bone
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,20, param1=4,param2=2,minRadius=38,maxRadius = 70)
for i in circles [:, 0]:
   # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),1)
    print (i)
    print (i[0],i[1])
#     cv2.circle(img,(int(i[0]),int(i[1])),10,(0,0,0),-1)
   # draw the center of the circle
    cv2.circle(circles,(i[0],i[1]),2,(255,255,255),1)
    # get rectangle bounding circular bone
xcenter=int(i[0])
ycenter=int(i[1])
r_point_x=math.floor(i[2]+i[0])
r_point_y=math.floor(-i[2]+i[1])
w=h=math.floor(1.5*i[2])
x=math.floor(i[0]-h)
y=math.floor(i[1]-w)
print("x",x)
print("y",y)
print("r",i[2])
# cv2.circle(img,(xcenter,ycenter),3,(0,0,0),-11)
# cv2.rectangle(ROI,(x,y),(x+2*w,y+2*h),(255,255,255),2)
#crop ROI from img
ROI = img[y:y+2*h, x:x+2*w]
ROI1=ROI.copy()
cv2.imshow("copy",ROI1)
cv2.imshow("ROI1", ROI)
ROI=cv2.pyrUp(ROI)
cv2.imshow("ROI",ROI)
equ = cv2.equalizeHist(ROI)
cv2.imshow('equ' , equ)
#apply threshold
th, th3 = cv2.threshold(ROI, 62, 255, cv2.THRESH_BINARY)
cv2.imshow("threshold",th3)
# #apply threshold
# th3 = cv2.adaptiveThreshold(equ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# cv2.imshow("g",th3)
kernal = np.ones((9,9), np.uint8)
#Erosion .. add pixels to the boundries of object if the kernal "fits"
erosion = cv2.dilate(th3,kernal,iterations=2)
cv2.imshow('erosion',erosion)
edges = cv2.Canny(erosion,150,200,apertureSize = 3)
cv2.imshow("canny",edges)
#Finding contours
edges, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(ROI, contours, -1, (255, 255, 255), 1, cv2.LINE_AA)
cv2.imshow("Result", ROI)
#get curves of ROI
minLineLength = 10 #The minimum number of points that can form a line
maxLineGap = 2 # maximum gap between two points to be considered in the same line
arr =[]
lines = cv2.HoughLinesP(edges,cv2.HOUGH_PROBABILISTIC, np.pi/180, 20, minLineLength,maxLineGap)
print("num of circles",len(lines))
for j in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[j]:
        cv2.line(ROI,(x1,y1),(x2,y2),(0,0,0),2, cv2.LINE_AA)
        pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
        cv2.polylines(ROI, [pts], True, (0,0,0))
        if ((lines[j][0][0]>xcenter) and (lines[j][0][1]<ycenter)) or ((lines[j][0][2]>xcenter) and (lines[j][0][3]<ycenter)):
            arr.append(lines[j])
print("number of curves lines",len(arr))

# get nearest x of the bone
highest_x = arr[0][0][0]
for a in range(0, len(arr)):  
    for x1,y1,x2,y2 in arr[a]:    
        if ( arr[a][0][0] > highest_x):
            highest_x=arr[a][0]
 
print("H",highest_x)
cv2.circle(img,(xcenter,r_point_y),5,(0,0,0),-11)
cv2.circle(img,(r_point_x,ycenter),5,(0,0,0),-11)
cv2.circle(img,(xcenter,ycenter),5,(0,0,0),-11)
cv2.circle(ROI,(int(highest_x[2]),int(highest_x[3])),5,(0,0,0),-11)
# print("selected points on cropp",highest_x[2],highest_x[3])
cv2.circle(img,(int((highest_x[2]/2)+(x)),int((highest_x[3]/2)+(y))),5,(0,0,0),-11)
# print("selected points on original",highest_x[2]+x,highest_x[3]+y)

cv2.circle(img,(int(highest_x[2]),int(highest_x[3])),5,(0,0,0),-11)
#  # print(lines[1][0])
# # print(len(arr))
# # print(arr[0][0])
cv2.imshow("curves lines", ROI)
cv2.imshow("curves line", img)
#calc distance between circular bone and nearest curve
dist_x = math.sqrt((((highest_x[2]/2)+(x)) - xcenter)**2 + (((highest_x[3]/2)+(y)) - r_point_y)**2)
dist_y = math.sqrt((((highest_x[2]/2)+(x)) - r_point_x)**2 + (((highest_x[3]/2)+(y)) - ycenter)**2)

print("distances ",dist_x,dist_y)
print("point1",xcenter,r_point_y)
print("point2",r_point_x,ycenter)
print("main point",((highest_x[2]/2)+(x)),((highest_x[3]/2)+(y)))
# #make condition to detemine if there is a dislocation or not
# if (dist_x<20 or dist_x>30) or (dist_y<30 or dist_y>40):  
#      print("dislocation detected")

cv2.waitKey(0)
cv2.destroyAllWindows()

