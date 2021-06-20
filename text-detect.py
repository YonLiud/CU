import numpy as np
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time
import asyncio
from yaspin import yaspin
from dotenv import dotenv_values

config = dotenv_values(".env")
car_cascade = cv2.CascadeClassifier('cars.xml') 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

async def detect_cars(image, sp):
    text = None
    Cropped = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,     cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None
    for c in cnts:
       peri = cv2.arcLength(c, True)
       approx = cv2.approxPolyDP(c, 0.018 * peri, True)
       if len(approx) == 4:
         screenCnt = approx
         break
    if screenCnt is None:
      detected = 0
      sp.write("X No contour detected")
    else:
      detected = 1
    if detected == 1:
      cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    mask = np.zeros(gray.shape,np.uint8)
    try:
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(image,image,mask=mask)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        Cropped = cv2.resize(Cropped, (200,100))
        text = str(pytesseract.image_to_string(Cropped, config='--psm 11'))

        text = ''.join([c for c in text if c in '0123456789'])
    except Exception as e:
        sp.write(e)
    if not text or text is None:
        text = "0 / Error Accrued"

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, 'Recent Plate: '+text, (10,450), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    sp.write("> plate: " + str(text))
    cv2.imshow("Frame", image)
    if Cropped is not None:
        cv2.imshow('Cropped',Cropped)

async def main(cap):
    with yaspin(text="Working") as sp:
        sp.color = "magenta"
        while True:
            ret, frame = cap.read()
            cars = car_cascade.detectMultiScale(frame)
            img = None

            height, width= frame.shape[:2]

            roi = frame[0:width, int(height/2):height]


            await detect_cars(roi, sp)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1)


if __name__ == "__main__":
    if (config["INPUT"].isdigit()):
        cap = cv2.VideoCapture(int(config["INPUT"]))
    else:
        cap = cv2.VideoCapture(config["INPUT"])
    asyncio.run(main(cap))
    cap.release()
