import numpy as np
import cv2
from datetime import datetime
from yaspin import yaspin

cap = cv2.VideoCapture(2)

lower_yellow = np.array([20, 100, 100], dtype="uint8")
upper_yellow = np.array([30, 255, 255], dtype="uint8")
low_threshold = 20
high_threshold = 150


def region_of_interest(image):
    imshape = image.shape
    lower_left = [imshape[1], imshape[0]]
    lower_right = [0, imshape[0]]
    top_left = [imshape[1], imshape[0]/2]
    top_right = [0, imshape[0]/2]
    vertices = [np.array([lower_left, top_left, top_right, lower_right], dtype=np.int32)]
    mask = np.zeros_like(image)
    if len(image.shape) > 2:
        channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def get_gray(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def get_canny(frame):
        gray_image = get_gray(frame)
        mask_yellow = cv2.inRange(frame, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(gray_image, 150, 255)
        mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
        mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)
        gauss_gray = cv2.GaussianBlur(mask_yw_image, (5, 5), 0)
        return cv2.Canny(gauss_gray, low_threshold, high_threshold)


with yaspin(text="Initiating", color="cyan") as sp:
        sp.text = "Working"

        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1270)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        while True:
                now = datetime.now()
                now = now.strftime("%Y/%m/%d %H:%M:%S")

                ret, frame = cap.read()

                cv2.putText(frame, str(now), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 3)

                canny = get_canny(frame)

                roi = region_of_interest(frame)

                cv2.imshow('frame', frame)
                cv2.imshow('canny', canny)
                cv2.imshow('roi', roi)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
# When everything done, release the capture
sp.text = ""
sp.ok("✔ Done")
cap.release()
cv2.destroyAllWindows()
