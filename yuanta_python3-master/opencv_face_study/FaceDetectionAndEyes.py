import cv2  # 安裝 py-opencv
import requests
import sys

face_cascade = cv2.CascadeClassifier('./xml/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('./xml/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,  # 待檢測圖片，一般為灰度圖像加快檢測速度
        scaleFactor=1.1,  # 表示在前後兩次相繼的掃描中，搜索窗口的比例係數。默認為1.1即每次搜索窗口依次擴大10%;
        minNeighbors=5,  # 每個目標至少檢測到幾次以上，才可被認定是真數據。
        minSize=(30, 30),  # 設定數據搜尋的最小尺寸 ，如 minSize=(30,30)
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # 在臉部周圍畫矩形框
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

        # 獲取該人臉矩形框的感興趣區域 ROI(region of interest), 淺複製(子圖像區域)
        roi_gray  = gray [y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()