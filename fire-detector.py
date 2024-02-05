
import cv2
import numpy as np
import smtplib
import playsound
import threading

Alarm_Status = False
Email_Status = False
Fire_Reported = 0

playsound.playsound('alarm-sound.mp3',True)

def play_alarm_sound_function():
	while True:
		playsound.playsound('alarm-sound.mp3',False)

def send_mail_function():

    recipientEmail = "kaavyask1@gmail.com"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('21pc18@psgtech.ac.in', 587)
        server.ehlo()
        server.starttls()
        server.login("21pc18@psgtech.ac.in",'password')
        server.sendmail('21pc18@psgtech.ac.in', recipientEmail, "Warning A Fire Accident has been reported on ABC Company")
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)


video = cv2.VideoCapture("video.mp4") # If you want to use webcam use Index like 0,1.

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    size = cv2.countNonZero(mask)

    
    if int(size) <= 15000:
        print("fitreeeee")
        Fire_Reported = Fire_Reported + 1


        if Fire_Reported >= 1:
		
            if Alarm_Status == False:
                winCommand(u'play {}{}'.format(sound, ' wait' if block else ''))
                threading.Thread(target=play_alarm_sound_function).start()
                play_alarm_sound_function()
                #send_mail_function()
                Alarm_Status = True

            
                #threading.Thread(target=send_mail_function).start()
                
                


    cv2.imshow("output", output)

    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
