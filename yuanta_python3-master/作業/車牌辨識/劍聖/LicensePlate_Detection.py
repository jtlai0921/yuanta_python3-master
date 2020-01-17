# -*- coding=utf-8 -*-
import cv2

carPath = "./xml/tw.xml"
carCascade = cv2.CascadeClassifier(carPath)

# smilePath = "./xml/haarcascade_smile.xml"
# smileCascade = cv2.CascadeClassifier(smilePath)

img = cv2.imread("./image/car3.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cars = carCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=8,
    minSize=(60, 60),
    flags=cv2.CASCADE_SCALE_IMAGE
)

# 畫出車牌
for (x, y, w, h) in cars:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

cv2.imshow('LicensePlate?', img)
# 儲存檔案
cv2.imwrite("./image/LicensePlate3.jpg",img)
# 任意鍵離開(若設定為 0 就表示持續等待至使用者按下按鍵為止)
c = cv2.waitKey(0)
