import cv2
import copy


def detect_lanes(img):
    return img




def main(cap):
    ret, img = cap.read()
    original = copy.deepcopy(img)
    height, width, channels = img.shape

    img = img[int(width/2):int(width), int((height)/3):int((height*2)/3)]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cannyimg = cv2.Canny(img,100,200)


    detect_lanes(gray)

    return cannyimg






if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        img = main(cap)
        cv2.imshow("canny", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()