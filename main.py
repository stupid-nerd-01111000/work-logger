import sys
import cv2
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QMessageBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
from face_recognation_manager import FaceRecognitionManager
import uuid


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

    def capture_photo(self):
        """Capture a photo and save it to a file."""
        ret, frame = self.capture.read()
        if ret:
            # Create folder if it doesn't exist
            if not os.path.exists("captured_photos"):
                os.makedirs("captured_photos")

            # Generate a unique file name
            photo_path = os.path.join("captured_photos", "photo.jpg")
            counter = 1
            while os.path.exists(photo_path):
                photo_path = os.path.join("captured_photos", f"photo_{counter}.jpg")
                counter += 1

            # Save the image using OpenCV
            cv2.imwrite(photo_path, frame)
            return photo_path

    def register_user(self):
        photo_path = self.capture_photo()
        if photo_path:
            new_id = self.generate_unique_id()
            face_manager = FaceRecognitionManager()
            face_manager.add_new_face(image_path=photo_path, user_id=new_id)
            QMessageBox.information(self, "Registration", f"User registered with ID: {new_id}")
        else:
            QMessageBox.warning(self, "Registration", "Failed to capture photo.")

    def enter_user(self):
        pass

    def exit_user(self):
        pass

    def closeEvent(self, event):
        """Release the camera on close."""
        self.capture.release()
        super().closeEvent(event)

    def generate_unique_id(self):
        return str(uuid.uuid4())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
