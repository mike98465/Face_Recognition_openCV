
'''
Modified from Examples in https://github.com/ageitgey/face_recognition
MIT License
Copyright (c) 2017, Adam Geitgey
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import face_recognition
import cv2
import pickle
import numpy as np

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# for raspberry pi 3 pi camera
#video_capture = cv2.VideoCapture('http://ip:port/stream.mjpg')

# Load face encodings
with open('dataset_faces.dat', 'rb') as f:
	all_face_encodings = pickle.load(f)
	
# Grab the list of names and the list of encodings
known_face_names = list(all_face_encodings.keys())

known_face_encodings = np.array(list(all_face_encodings.values()))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2, model = "cnn")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,num_jitters = 25)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
	    # Asian face dataset need strict tolerence, if you need to run on other dataset, you can try tolerence = 0.5
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance = 0.375)
            name = "Unknown"
			
            #print(matches)
			
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                match_index = matches.index(True)
                #matches[match_index] = False
                name = known_face_names[match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Face_recognition', frame)

    # Hit 'enter' on the keyboard to quit!
    if cv2.waitKey(1) == 13:
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
