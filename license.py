import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#now to read the image file
image = cv2.imread('red.jpg')
#we will standardise and resize the image to 500
image = imutils.resize(image, width = 500)

# we will display original image when it will start finding 
cv2.imshow("Original Image",image)
cv2.waitKey(0)
# Now convert image to grayscale
gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Scale Image",gray)
cv2.waitKey(0)
# now we will reduce noise from our image and make it smooth
gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("Smoother Image",gray)
cv2.waitKey(0)

# now we will do the edge detection
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("Canny edge",edged)
cv2.waitKey(0)

cnts , new = cv2.findContours(edged.copy(), cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)
#NOW WE WILL CREATE A COPY OF THE ORIGINAL IMAGE TO DRAW ALL THE CONTOURS
image1 = image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
cv2.imshow("Canny after contouring",image1)
cv2.waitKey(0)

# Now since we are only interested in the contours of the number plate
#but we cant directly locate all so we will sort them out on the basis of their areas by selescting the areas which are 
#maximum ,so we will sort top 30 areas
#but it will give a sorted list as in order of min to max 
# so for that we will reverse the order of sorting
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:30]
NumberPlateCount = None
#to draw top 30 contours we will make copy of original image
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("Top 30 Contours",image2)
cv2.waitKey(0)
# Now we will run a for loop to find the expected contour of our number plate
count = 0
name = 1 #name of our image
for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i,0.02*perimeter,True)
    if(len(approx)==4):
        NumberPlateCount = approx # means number of corners which will be 4 for our number plate
        #now we will crop that rectangle part
        x,y,w,h = cv2.boundingRect(i)
        crp_img = image[y:y+h,x:x+w]

                ########################
                #                      #
                #                      #
                #                      #
                ########################
        cv2.imwrite(str(name)+'.png',crp_img)
        name+=1
        break
cv2.drawContours(image,[NumberPlateCount],-1,(0,255,0),3)
cv2.imshow("Final image",image)
cv2.waitKey(0) 

crop_img_loc = '1.png'
cv2.imshow("Cropped Image",cv2.imread(crop_img_loc))
cv2.waitKey(0)

text = pytesseract.image_to_string(crop_img_loc,lang='eng')
print("Number is: ", text)
cv2.waitKey(0)
