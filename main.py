import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0);

# load known faces
deep_image = face_recognition.load_image_file("faces/deep.jpg")
deep_encoding = face_recognition.face_encodings(deep_image)[0]
rajat_image = face_recognition.load_image_file("faces/rajat.jpg")
rajat_encoding = face_recognition.face_encodings(rajat_image)[0]

known_face_encodings = [deep_encoding, rajat_encoding]
known_face_name = ["deep", "rajat"]

# list of expected student
students = known_face_name.copy()

face_locations = [];
face_encoding = [];

# get the current date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + ".csv", "w+", newline="")

lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_location = face_recognition.face_locations(rgb_small_frame)
    face_encoding = face_recognition.face_encodings(rgb_small_frame, face_location)

    for face_encodin in face_encoding:
        matches = face_recognition.compare_faces(known_face_encodings,face_encodin)
        face_distance = face_recognition.face_distance(known_face_encodings,face_encodin)
        best_match_index = np.argmin(face_distance)
        if(matches[best_match_index]):
            name = known_face_name[best_match_index]

        if name in known_face_name:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name+" Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

            if name in students:
                students.remove(name)
                current_time = now.strftime("%H-%M%S")
                lnwriter.writerow([name, current_time])

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()