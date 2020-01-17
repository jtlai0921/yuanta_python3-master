import cv2  # 安裝 py-opencv
import requests
import sys

face_cascade = cv2.CascadeClassifier('./xml/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('./xml/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('./xml/haarcascade_smile.xml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,              # 待檢測圖片，一般為灰度圖像加快檢測速度
        scaleFactor=1.1,   # 檢測粒度 scaleFactor 。更大的粒度將會加快檢測的速度，但是會對檢測準確性產生影響。相反的，一個更小的粒度將會影響檢測的時間，但是會增加準確性。
        minNeighbors=5,    # 每個目標至少檢測到幾次以上，才可被認定是真數據。
        minSize=(30, 30),  # 設定數據搜尋的最小尺寸 ，如 minSize=(30,30)
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # 畫出每一個臉的範圍
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

        roi_gray  = gray [y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # 對人臉進行眼部偵測
        eyes = eye_cascade.detectMultiScale(roi_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

        # 對人臉進行微笑偵測
        smile = smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=100,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # 框出上揚嘴角，並打上 Smile 標籤
        for (sx, sy, sw, sh) in smile:
            cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 0, 0), 2)
            cv2.putText(frame, 'Smile', (x, y - 7), 3, 1.2, (0, 255, 0), 2)


    # 顯示
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()