
import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('D:\MK\Coding\OJ\parkinglot\Park.mp4')

with open('D:\MK\Coding\OJ\CarParkPos2', 'rb') as f:
    posList = pickle.load(f)

width, height = 50, 40


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        # x, y = pos
        ls = pos

        rect = cv2.boundingRect(ls)
        # cv2.drawContours(imgPro, [ls], -1, (255, 255, 255), -1, cv2.LINE_AA)
        x, y, w, h = rect
        imgCrop = imgPro[y:y+h-10, x:x+w-10]
        # imgCrop = imgPro[y:y+30, x:x+30]
        # imgCrop = imgPro[]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        # if count < 900:
        if count < 2400:  # 해당 이미지 내에서 경계값을 나타냄
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.polylines(img, np.int32([pos]), True, color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 2)  # blur의 정도를 결정함
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 2)  # 맨 마지막 값이 선명도를 이야기함.
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=2)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(1)
