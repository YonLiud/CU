import argparse
import asyncio
import sys

import cv2
import imutils
import numpy as np
import pytesseract


async def print_plate(plate):
    print(f"License plate: {str(plate)}")


async def detect_cars(image):
    text = None
    cropped = None

    # Convert to grey scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur to reduce noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # Perform Edge detection
    edged = cv2.Canny(gray, 30, 200)

    # Get contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    screenCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    # Draw contours
    if detected == 1:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)

    mask = np.zeros(gray.shape, np.uint8)

    if screenCnt is not None:
        new_image = cv2.drawContours(
            mask,
            [screenCnt],
            0,
            255,
            -1,
        )
        new_image = cv2.bitwise_and(image, image, mask=mask)
        (x, y) = np.where(mask == 255)
        (top_x, top_y) = (np.min(x), np.min(y))
        (bottom_x, bottom_y) = (np.max(x), np.max(y))

        cropped = gray[top_x : bottom_x + 1, top_y : bottom_y + 1]
        cropped = cv2.resize(cropped, (200, 100))

        text = str(pytesseract.image_to_string(cropped, config="--psm 11"))
        text = "".join([c for c in text if c in "0123456789"])

    if not text or text is None:
        text = "0 / Error Occurred"

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "License Recent Plate: " + text, (10, 450), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    print(f"Recent License Plate: {text}")
    cv2.imshow("Frame", image)

    if cropped is not None:
        cv2.imshow("Cropped image", cropped)


async def main(cap):
    while True:
        ret, frame = cap.read()
        cars = car_cascade.detectMultiScale(frame)
        # img = None
        # for (x, y, w, h) in cars:
        #     img = frame[y : y + h, x : x + w]
        # if img is not None:
        #     await detect_cars(img)
        await detect_cars(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":

    user_os = sys.platform
    car_cascade = cv2.CascadeClassifier("cars.xml")

    if user_os == "win32":
        # TODO: this might not always be tessaract execution path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-source", type=str)

    args = parser.parse_args()

    if args.input_source.isdigit():
        cap = cv2.VideoCapture(int(args.input_source))
    else:
        cap = cv2.VideoCapture(args.input_source)

    asyncio.run(main(cap))
    cap.release()
