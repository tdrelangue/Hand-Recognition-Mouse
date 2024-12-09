import cv2
import mediapipe
import pyautogui
import math

screen_width, screen_height = pyautogui.size()
mp_hands = mediapipe.solutions.hands
capture_hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
drawing_option = mediapipe.solutions.drawing_utils
camera = cv2.VideoCapture(0)
x1 = x2 = y1 = y2 = x3 = y3 = 0

while True:
    _,image = camera.read()
    image = cv2.flip(image, 1) # the image is flipped
    image_height, image_width, _ = image.shape

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    output_hands = capture_hands.process(rgb_image)

    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image,hand) # ,connections=mp_hands.HAND_CONNECTIONS
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == mp_hands.HandLandmark.THUMB_TIP: # point 4 = thumb tip
                    cv2.circle(image,(x,y), 10, (0,255,255))
                    x2, y2 = x, y

                if id == mp_hands.HandLandmark.INDEX_FINGER_TIP: # point 8 = index tip
                    # mouse_x = int(screen_width / image_width *x)
                    # mouse_y = int(screen_height / image_height * y)
                    # pyautogui.moveTo(mouse_x,mouse_y)
                    x1, y1 = x, y
                    print(int(15 + 100 * (-lm.z)))
                    print(math.sqrt((y2 - y1)**2) + math.sqrt((x2 - x1)**2))
                    if math.sqrt((y2 - y1)**2) + math.sqrt((x2 - x1)**2) <= int(15 + 100 * (-lm.z)):
                        cv2.circle(image,(x,y), 10, (0,0,255))
                    else:
                        cv2.circle(image,(x,y), 10, (0,255,255))
                    

                if id == mp_hands.HandLandmark.MIDDLE_FINGER_TIP: # point 12 = thumb tip
                    x3, y3 = x, y
                    if math.sqrt((y2 - y3)**2)+math.sqrt((x2 - x3)**2) <= int(15 + 100 * (-lm.z)):
                        cv2.circle(image,(x,y), 10, (0,0,255))
                    else:
                        cv2.circle(image,(x,y), 10, (0,255,255))

    
            x, y = (x1+x2)/2, (y1+y2)/2
            mouse_x = int(screen_width / image_width *x)
            mouse_y = int(screen_height / image_height * y)
            pyautogui.moveTo(mouse_x,mouse_y)
                


        distThumbIndex = (y2 - y1)/2+(x2 - x1)/2
        distThumbMiddle = (y2 - y3)/2+(x2 - x3)/2

        if distThumbIndex <= 10:
            pyautogui.click()
        if distThumbMiddle <= 10:
            pyautogui.rightClick()

    cv2.imshow("hand movement gesture", image)

    # stop when escape is pressed
    key = cv2.waitKey(1)
    if key == 27: # key nb 27 = escape
        break



camera.release()
cv2.destroyAllWindows()