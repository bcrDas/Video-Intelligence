# USAGE
# python videobased_realtime_attendance_system.py --image_database_path inputs/images/attendance_system_image_database --attendance_logger_path outputs/attendance_logger/Attendance.csv

#############################################################################################################################

import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import argparse

#############################################################################################################################

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--image_database_path", required=True)
ap.add_argument("-l", "--attendance_logger_path", required=True)

args = vars(ap.parse_args())

#############################################################################################################################

# Importing Images form database
path = args["image_database_path"]
images = []
className = []
myList = os.listdir(path)
for x,cl in enumerate(myList):
    curImg = cv2.imread('{}/{}'.format(path, cl))
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

#############################################################################################################################

# Compute Encodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)
print('Encodings Completed.')

#############################################################################################################################

# Saving attendance into excel file.
def markAttendance(name):
    with open(args["attendance_logger_path"],'r+') as f:
        myDataList = f.readlines()
        nameList =[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in  line:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines('\n{},{}'.format(name,dt_string))

#############################################################################################################################

cap = cv2.VideoCapture(0)

while True:
    # Taking webcam image 
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Finding face locations and encodings
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    # Finding the face match
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        # Look for the optimal face similarity matching
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = className[matchIndex].upper()
            print("\nThis is {}!!!\n".format(name))
            y1,x2,y2,x1=faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4  
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0), 1)
            markAttendance(name)

    cv2.imshow('Livefeed(PRESS "q" to quit)',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#############################################################################################################################

cap.release()
cv2.destroyAllWindows()

#############################################################################################################################
