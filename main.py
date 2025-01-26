import sys
import cv2
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QMessageBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
from face_recognation_manager import FaceRecognitionManager
import uuid
import csv
from datetime import datetime
from attendance_analyzer import app
from threading import Thread


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera App")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Camera feed label (to display the live feed)
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setFixedSize(640, 480)
        self.layout.addWidget(self.camera_label)

        # Button layout (horizontal layout under the camera)
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # Buttons
        self.register_button = QPushButton("Register")
        self.enter_button = QPushButton("Enter")
        self.exit_button = QPushButton("Exit")

        # Add buttons to the layout
        self.button_layout.addWidget(self.enter_button)
        self.button_layout.addWidget(self.exit_button)
        self.button_layout.addWidget(self.register_button)

        # OpenCV video capture
        self.capture = cv2.VideoCapture(0)  # Default camera (0)

        # Timer for updating the camera feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(30)  # Update every 30ms

        # Connect buttons
        self.register_button.clicked.connect(self.register_user)
        self.enter_button.clicked.connect(self.enter_user)
        self.exit_button.clicked.connect(self.exit_user)

        # file name
        self.registration_users_file = 'registration_users.csv'
        self.users_log_file = 'logs.csv'

        # run some methodes app need
        self.create_registrations_users_file()
        self.create_users_log_file()
        self.make_photos_dir()

    def make_photos_dir(self):
        if not os.path.exists('photos'):
            os.makedirs('photos')

    def create_registrations_users_file(self):
        # check if the file exists, and create it with header if not.
        if not os.path.exists(self.registration_users_file):
            with open(self.registration_users_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['user_id', 'register_date', 'register_time'])  # write headers
            print(f'{self.registration_users_file} created successfuly.')
        else:
            print(f'{self.registration_users_file} already exists.')

    def create_users_log_file(self):
        # check if the file exists, and create it with header if not.
        if not os.path.exists(self.users_log_file):
            with open(self.users_log_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['user_id', 'date', 'time', 'enter_or_exit'])  # write headers
            print(f'{self.users_log_file} created successfuly.')
        else:
            print(f'{self.users_log_file} already exists.')

    def update_camera_feed(self):
        """Update the live camera feed in the QLabel."""
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(q_image))

    def capture_photo(self, work):
        """Capture a photo and save it to a file."""
        ret, frame = self.capture.read()
        if ret:
            # Generate a unique file name and id
            new_id = self.generate_unique_id()
            photo_path = os.path.join("photos", f'photo_{new_id}.jpg')

            # Save the image using OpenCV
            cv2.imwrite(photo_path, frame)
            if work == 'register':
                return photo_path, new_id
            elif work == 'enter-or-exit':
                return photo_path

    def register_user(self):
        photo_path, new_id = self.capture_photo('register')
        face_manager = FaceRecognitionManager()
        user = face_manager.recognize_face(photo_path)
        if user == 'unknown':
            if photo_path:
                # Teaching the machine a new user
                face_manager.add_new_face(image_path=photo_path, user_id=new_id)

                # get-the-currect-date-and-time
                date, time = self.get_date_time()

                # append-the-new-user-information-to-the-file
                with open(self.registration_users_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([new_id, date, time])
                QMessageBox.information(self, "Registration", f"User registered with ID: {new_id}")
            else:
                QMessageBox.warning(self, "Registration", "Failed to capture photo.")
        else:
            QMessageBox.warning(self, 'Registration', 'You have already registered')

    def enter_user(self):
        photo_path = self.capture_photo('enter-or-exit')
        face_manager = FaceRecognitionManager()
        user_id = face_manager.recognize_face(photo_path)
        date, time = self.get_date_time()
        if user_id == 'unknown':
            QMessageBox.warning(self, 'unknown', 'you must register first')
        else:
            # append-information-to-file
            with open(self.users_log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, date, time, 'enter'])
            QMessageBox.information(self, 'Welcome', f'your entry has been recorded with id : {user_id}')

    def exit_user(self):
        photo_path = self.capture_photo('enter-or-exit')
        face_manager = FaceRecognitionManager()
        user_id = face_manager.recognize_face(photo_path)
        date, time = self.get_date_time()
        if user_id == 'unknown':
            QMessageBox.warning(self, 'unknown', 'you must register first')
        else:
            # append-information-to-file
            with open(self.users_log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, date, time, 'exit'])
            QMessageBox.information(self, 'I will miss you', f'your exit has been recorded with id : {user_id}')

    def get_date_time(self):
        # get-the-currect-date-and-time
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        return date, time

    def closeEvent(self, event):
        """Release the camera on close."""
        self.capture.release()
        super().closeEvent(event)

    def generate_unique_id(self):
        return str(uuid.uuid4())


def run_flask():
    # if you want debug run app in main 
    app.run(debug=False)


if __name__ == "__main__":
    # run flask in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # run pyqt in the main thread
    qtapp = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(qtapp.exec())
