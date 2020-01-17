# -*- coding=utf-8 -*-
import cv2

# https://github.com/openalpr/openalpr/tree/master/runtime_data/region
facePath = "./xml/us.xml"
faceCascade = cv2.CascadeClassifier(facePath)

imglist = ("car1.jpg", "car2.jpg", "car3.jpg")
for filename in imglist:
    img = cv2.imread("./image/" + filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # 畫出每一個車牌
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow('車牌', img)
    # 任意鍵離開(若設定為 0 就表示持續等待至使用者按下按鍵為止)
    c = cv2.waitKey(0)

cv2.destroyAllWindows()
