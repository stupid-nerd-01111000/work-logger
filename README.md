# Work Logger - Employee Attendance System

## Overview

The **Work Logger** is a comprehensive system designed to manage and monitor employee attendance in a company. It utilizes face recognition technology to ensure accurate logging and provides both a desktop interface for attendance logging and a web-based interface for data visualization and management.

## Features

- **Face Recognition**: Automated attendance tracking using facial recognition technology.
- **Data Analysis**: Tools for analyzing attendance trends and generating reports.
- **Web Interface**: User-friendly web application for viewing results, including identifying late arrivals and absences.
- **Desktop Interface**: PyQt-based application for efficient attendance logging.
- **Customizable**: Easily extendable and configurable for different organizational needs.

## Project Structure

```
work-logger-main/
├── main.py                   # Main entry point for the application
├── web_app.py                # Web application logic
├── face_recognation_manager.py  # Face recognition management
├── data_analyze.py           # Data analysis tools
├── requirements.txt          # Dependencies
├── templates/                # HTML templates for the web interface
├── static/                   # Static files (CSS, JS, images)
└── .gitignore                # Git ignore file
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd work-logger-main
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   - **Desktop Application (PyQt):**
     ```bash
     python main.py
     ```
   - **Web Interface:**
     ```bash
     python web_app.py
     ```

## Usage

- Use the PyQt application to log employee attendance using face recognition.
- Access the web interface by navigating to `http://localhost:5000` in your browser to view results, including late arrivals and absences.
- Analyze attendance data using the provided tools.

## Requirements

- Python 3.8+
- Flask
- PyQt5
- OpenCV
- Other dependencies listed in `requirements.txt`

## Contributing

We welcome contributions! Please fork the repository and submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to reach out with questions or feedback!

