import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import pyautogui as auto
import webbrowser
# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.7)

# Variable to store the maximum open distance and previous ratio
open_hand_distance = None
previous_ratio = None
webbrowser.open("https://chromedino.com/")
while True:
    # Capture the video frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Resize the frame for better visibility
    frame = cv2.resize(frame, (1080, 720))

    # Detect hands in the frame
    hands, frame = detector.findHands(frame)

    if hands:
        # Get the first detected hand
        
        hand = hands[0]
        lmList = hand['lmList']  # List of 21 landmarks

        # Calculate the distance between the tip of the thumb (landmark 4) and the tip of the index finger (landmark 8)
        length, info, frame = detector.findDistance(lmList[4][0:2], lmList[8][0:2], frame)
        
        # Set the open hand distance (this should be done once when the hand is fully open)
        if open_hand_distance is None:
            open_hand_distance = length
            #print(f"Open hand distance set: {open_hand_distance}")

        # Calculate the ratio of the current distance to the open hand distance
        ratio = length / open_hand_distance if open_hand_distance else 1
        #print(f"Distance: {round(length)}, Ratio: {round(ratio, 2)}")

        # Check if previous ratio is set, and if the ratio changes by more than 0.3
        if previous_ratio is not None:
            if abs(ratio - previous_ratio) > 0.3:
                #print("Significant ratio change detected! Pressing space...")
                auto.press('space')

        # Update the previous ratio
        previous_ratio = ratio

    # Show the frame in a window
    cv2.imshow('Window', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()

