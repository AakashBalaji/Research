import cv2
import numpy as np
import imutils
import os
import glob


#path to images
mask_path = os.getcwd() + "/nuclei/*.png"
#image names
mask_names = glob.glob(mask_path)

#get upto last 8 characters
img_names = [mask_name[:-8] + "original.tif" for mask_name in mask_names]

#iterate through images in path

for imageNo, (img, mask) in enumerate(zip(img_names, mask_names)):
    groupNo = 0

    #reads in image
    img = cv2.imread(img)
    #for binary/greyscale image
    mask = cv2.imread(mask, 0)
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    
    
    for i in range(len(contours)):
    
      #get file name
      imageName = "{}_{}i.png".format(imageNo, groupNo)
      maskName = "{}_{}m.png".format(imageNo, groupNo)

      moments = cv2.moments(contours[i])
      if moments['m00'] > 0:
          
        #rectFinal = cv2.rectangle(img,(int(moments['m10']/moments['m00']) - 64, int(moments['m01']/moments['m00']) - 64),((int(moments['m10']/moments['m00']) + 64,int(moments['m01']/moments['m00']) + 64)),(255,0,255),2)
        x = (int(moments['m10']/moments['m00']) + 64)
        y = int(moments['m01']/moments['m00']) + 64

        x1 = int(moments['m10']/moments['m00']) - 64
        y1 = (int(moments['m01']/moments['m00']) - 64)
        
        if(x1 >= 0 and y1 >= 0 and x <= 2000 and y <= 2000):
          #for color image
          cropped_img = img[y1:y, x1:x, :]
          #for binary/greyscale image
          cropped_mask = mask[y1:y, x1:x]
        
          cv2.imwrite(maskName, cropped_mask)
          cv2.imwrite(imageName, cropped_img)

          groupNo += 1
