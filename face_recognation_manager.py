import os
import pickle
import cv2
import mediapipe as mp


class FaceRecognitionManager:
    def __init__(self, database_path="face_database.pickle"):
        """
        Initializes the FaceRecognitionManager with a database file to store encodings and IDs.
        :param database_path: Path to the database file.
        """
        self.database_path = database_path
        self.face_data = self._load_database()
        self.mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    def _load_database(self):
        """Loads the face database from the pickle file or initializes an empty one."""
        if os.path.exists(self.database_path):
            with open(self.database_path, "rb") as f:
                return pickle.load(f)
        return {"face_images": [], "ids": []}

    def _save_database(self):
        """Saves the current face data to the database file."""
        with open(self.database_path, "wb") as f:
            pickle.dump(self.face_data, f)

    def _extract_face(self, image):
        """
        Extracts a face region from the image using Mediapipe Face Detection.
        :param image: Input image as a numpy array.
        :return: Cropped face image or None if no face is detected.
        """
        results = self.mp_face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                face = image[y:y + h, x:x + w]
                return cv2.resize(face, (100, 100))  # Resize for consistency
        return None

    def add_new_face(self, image_path, user_id):
        """
        Adds a new face with a specific user ID to the database.
        :param image_path: Path to the image containing the face.
        :param user_id: Unique ID associated with the face.
        """
        # type checking for user_id
        if not isinstance(user_id, (str, int)):
            raise TypeError('User ID must be a string or an integer.')

        image = cv2.imread(image_path)
        face = self._extract_face(image)

        if face is None:
            raise ValueError("No face detected in the provided image.")

        # Add the face and ID to the database
        self.face_data["face_images"].append(face)
        self.face_data["ids"].append(user_id)

        # Save the updated database
        self._save_database()
        print('new_face_added_succesfully')

    def recognize_face(self, image_path):
        """
        Recognizes a face from the provided image and returns the associated ID.
        :param image_path: Path to the image containing the face to recognize.
        :return: The ID of the recognized face or 'Unknown' if no match is found.
        """
        image = cv2.imread(image_path)
        face = self._extract_face(image)

        if face is None:
            raise ValueError("No face detected in the provided image.")

        # Compare the face with stored faces
        for stored_face, user_id in zip(self.face_data["face_images"], self.face_data["ids"]):
            # Compare using simple pixel-wise difference
            diff = cv2.absdiff(stored_face, face)
            score = diff.mean()

            if score < 50:
                return user_id

        return "unknown"


# for test
if __name__ == '__main__':
    fr = FaceRecognitionManager()
    for i in range(1, 5):
        fr.add_new_face(image_path=f'photos/image{i}.jpg', user_id=i)
