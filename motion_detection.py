import threading
import cv2
import imutils
import time

cap = cv2.VideoCapture(0, cv2.CAP_ANY)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    cap.release()
    exit()

# Allow the camera to initialize (add a delay)
time.sleep(2)

_, start_frame = cap.read()
if start_frame is None:
    print("Error: Unable to capture the initial frame.")
    cap.release()
    exit()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm

    for _ in range(5):
        if not alarm_mode:
            break

        print("Alarm")


while True:
    _, frame = cap.read()
    if frame is None:
        print("Error: Unable to capture the frame.")
        break

    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(start_frame, frame_bw)

        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        # Update start_frame only when motion is detected
        if threshold.sum() > 200:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
                start_frame = frame_bw

        cv2.imshow("cam", threshold)
    else:
        cv2.imshow("cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm,daemon=True).start()

    key_pressed = cv2.waitKey(30)

    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0

    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()




