import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

cap = cv2.VideoCapture(0)

pTime = 0

detector = htm.handDetector(detectionCon=0.7)

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
vol = 0
volPerc = 0


while True:
    success, img = cap.read()
    img =detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
       # print(lmList[4], lmList[8])

       x1, y1 = lmList[4][1], lmList[4][2]
       x2, y2 = lmList[8][1], lmList[8][2]
       cx, cy = (x1 + x2) // 2, (y1 + y2)  // 2

       cv2.circle(img, (x1, y1), 9, (255, 0, 255), cv2.FILLED)
       cv2.circle(img, (x2, y2), 9, (255, 0, 255), cv2.FILLED)
       cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
       cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)

       length = math.hypot(x2 - x1, y2 - y1)
       # print(length)

       # hand range 30 - 180
       # volume range -63 - 0

       vol = np.interp(length, [30, 180],[minVol, maxVol])
       volBar = np.interp(length, [30, 180], [400, 150])
       volPerc = np.interp(length, [30, 180], [0, 100])
       volume.SetMasterVolumeLevel(vol, None)

       print(int(length), vol)
       if length<=30:
           cv2.circle(img, (cx, cy), 9, (0, 255, 0), cv2.FILLED)
       if length>=180:
           cv2.circle(img, (cx, cy), 9, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPerc)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cTime = time.time()
    fps = 1 /(cTime - pTime)
    pTime = cTime

    cv2.imshow("Img", img)
    cv2.waitKey(1)
