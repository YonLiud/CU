from __future__ import division

import cv2
import numpy as np

import track
import detect

def main():
    cap = cv2.VideoCapture(0)
    ticks = 0

    lt = track.LaneTracker(2, 0.1, 500)
    ld = detect.LaneDetector(180)
    while cap.isOpened():
        ret, frame = cap.read()
        try:
            precTick = ticks
            ticks = cv2.getTickCount()
            dt = (ticks - precTick) / cv2.getTickFrequency()

            predicted = lt.predict(dt)

            predicted = np.array(predicted)

            lanes = ld.detect(frame)

            if predicted is not None:
                cv2.line(frame, (predicted[0][0], predicted[0][1]), (predicted[0][2], predicted[0][3]), (0, 0, 255), 5)
                cv2.line(frame, (predicted[1][0], predicted[1][1]), (predicted[1][2], predicted[1][3]), (0, 0, 255), 5)

            lt.update(lanes)
        except Exception as e:
            print(e)
        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()