#!/usr/bin/python3
# -*- coding: utf-8 -*-

import face_recognition
import cv2
import numpy as np
import glob
import os
import screeninfo
import time
from PIL import Image, ImageFont, ImageDraw
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.LOW)
base_path = "/home/pi"
monitor = None
for m in screeninfo.get_monitors():
    monitor = m
    break

# Convert name to an Image
def get_chinese_name(name):
    font = ImageFont.truetype(os.path.join(base_path, 'simsun.ttf'), 32)
    width, height = font.getsize(name)
    img = Image.new("RGB", (width, height), (255, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), name, fill="#FFFFFF", font=font)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
# video_capture.set(cv2.CAP_PROP_FPS, 1)
# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

faces_dir = "/home/pi/faces"

for image in glob.glob(os.path.join(faces_dir, '*')):
    if image.endswith('.jpg') or image.endswith('.png'):
        print("Adding %s" % (image, ))
        name, _ = os.path.splitext(os.path.basename(image))
        img = face_recognition.load_image_file(image)
        face_encodings = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(face_encodings)
        known_face_names.append(get_chinese_name(name))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
unknown_name = get_chinese_name("不认识")
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    if not ret:
        continue
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.4)
            name = unknown_name

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #    first_match_index = matches.index(True)
            #    name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                 name = known_face_names[best_match_index]
            face_names.append(name)
            if name is unknown_name:
                 GPIO.output(23,GPIO.HIGH)
                 time.sleep(1)
                 GPIO.output(23, GPIO.LOW)
                 time.sleep(1)
            else:
                 GPIO.output(18,GPIO.HIGH)
                 time.sleep(1)
                 GPIO.output(18,GPIO.LOW)
                

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

        # Draw matching name
        x_offset = left
        y_offset = bottom

        y1, y2 = max(0, y_offset), min(frame.shape[0], y_offset + name.shape[0])
        x1, x2 = max(0, x_offset), min(frame.shape[1], x_offset + name.shape[1])
        y1o, y2o = max(0, -y_offset), min(name.shape[0], frame.shape[0] - y_offset)
        x1o, x2o = max(0, -x_offset), min(name.shape[1], frame.shape[1] - x_offset)
        frame[y1:y2, x1:x2] = name[y1o:y2o, x1o:x2o]

    # Display the resulting image
    cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    if monitor is None:
        cv2.imshow('Video', frame)
    else:
        cv2.imshow('Video', cv2.resize(frame, (monitor.width, monitor.height)))
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
