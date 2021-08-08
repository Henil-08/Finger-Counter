from cv2 import cv2 as cv
import HandTrackingModule as htm

# Initializing the modules
cap = cv.VideoCapture(0)
detect = htm.HandDetector(maxHands=1)

# Make this True to count the left hand
_LEFT_HAND = False

# Initializing the finger tips
tipIDs = [4, 8, 12, 16, 20]

def drawNumber(frame, noFinger):
    font = cv.FONT_HERSHEY_DUPLEX
    text = str(noFinger)
    cv.rectangle(frame, (0, 380), (70, 480), (0, 255, 0), -1)
    cv.putText(frame, text, (0, 470), font, 4, (0, 0, 255), 3)


while(cap.isOpened()):
    isSuccess, frame = cap.read()

    if isSuccess:
        frame = detect.findHands(frame)
        
        # Fliping the frame horrizontally
        frame = cv.flip(frame, 1)

        lmList_1 = detect.findPosition(frame, handNo=0, boxDraw=False)
        fW = cap.get(3)
        fH = cap.get(4)
        
        # Checking the Finger of Hand 1
        if len(lmList_1) != 0:
            fingerCheck = []

            if not _LEFT_HAND:            
                # For thumb
                if lmList_1[4][1] > lmList_1[3][1]:
                    fingerCheck.append(True)
                else:
                    fingerCheck.append(False)
            else:
                # For thumb
                if lmList_1[4][1] < lmList_1[3][1]:
                    fingerCheck.append(True)
                else:
                    fingerCheck.append(False)

            # For other fngers
            for id in range(1, 5):
                if lmList_1[tipIDs[id]][2] < lmList_1[tipIDs[id]-2][2]:
                    fingerCheck.append(True)
                else:
                    fingerCheck.append(False)
            
            totalFingers = fingerCheck.count(True)
            # print(totalFingers)

            drawNumber(frame, totalFingers)    
               
        # Calculating the FPS
        detect.addFPS(frame)

        cv.imshow("Video", frame)
        if cv.waitKey(1) & 0xFF == 27:
            break


cap.release()
cv.destroyAllWindows()  
