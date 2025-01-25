import face_recognation
import os
import cv2
import numpy as np
import pickle
import csv
from datetime import datetime


class FaceRecognitionManager:
    def __init__(self, data_file="known_faces.pkl"):
        """
        Initialize the FaceRecognitionManager class.
        :param data_file: Path to the file where known faces and IDs are stored.
        """
        self.data_file = data_file
        self.known_face_encodings = []
        self.known_face_ids = []

        # Load known faces and IDs from file if it exists
        if os.path.exists(self.data_file):
            self.load_known_faces()

    def save_register_records(self, user_id):
        # get the currect date and time
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')  # date format : YYYY-MM-DD
        time = now.strftime('%H-%M-%S')  # time format : HH:MM:SS
        # wite to csv file
        with open('registered_users.csv', mode='a', newline='') as file:
            write = csv.writer(file)
            write.writerow([user_id, date, time])

    def load_known_faces(self):
        """Load known faces and their IDs from the data file."""
        with open(self.data_file, "rb") as file:
            data = pickle.load(file)
            self.known_face_encodings = data["encodings"]
            self.known_face_ids = data["ids"]

    def save_known_faces(self):
        """Save known faces and their IDs to the data file."""
        with open(self.data_file, "wb") as file:
            data = {"encodings": self.known_face_encodings, "ids": self.known_face_ids}
            pickle.dump(data, file)

    def add_new_face(self, image_path, user_id):
        """
        Learn a new face and associate it with an ID.
        :param image_path: Path to the image containing the face.
        :param face_id: A unique ID for the face.
        """
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            self.known_face_encodings.append(face_encodings[0])
            self.known_face_ids.append(user_id)
            self.save_known_faces()
            self.save_register_records(user_id=user_id)
            return {'message': 'user_registered'}
        else:
            return {'message': 'no_face_found_in_the_image'}

    def recognize_faces(self, image_path):
        """
        Recognize faces in an image and return their IDs.
        :param image_path: Path to the image containing faces.
        :return: List of recognized face IDs.
        """
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        recognized_ids = []

        for face_encoding in face_encodings:
            # Compare the face with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            if matches:
                # Find the best match
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    recognized_ids.append(self.known_face_ids[best_match_index])
                else:
                    recognized_ids.append("Unknown")
            else:
                recognized_ids.append("Unknown")

        return recognized_ids

    def get_known_faces(self):
        """Return the list of known face IDs."""
        return self.known_face_ids
