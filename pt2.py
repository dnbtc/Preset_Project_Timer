import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QTimer, QTime
from datetime import datetime

class ProjectTrackerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.project_name_input = QLineEdit()
        self.layout.addWidget(self.project_name_input)

        self.save_button = QPushButton('Save Project Name')
        self.save_button.clicked.connect(self.save_project_name)
        self.layout.addWidget(self.save_button)

        self.project_name_label = QLabel()
        self.layout.addWidget(self.project_name_label)

        self.preset_label = QLabel('Preset: 0')
        self.preset_label.setStyleSheet("font-size: 60px")
        self.layout.addWidget(self.preset_label)

        self.increment_button = QPushButton('Increment Preset')
        self.increment_button.clicked.connect(self.increment_preset)
        self.layout.addWidget(self.increment_button)

        self.decrement_button = QPushButton('Decrement Preset')
        self.decrement_button.clicked.connect(self.decrement_preset)
        self.layout.addWidget(self.decrement_button)

        self.create_preset_button = QPushButton('Create Preset')
        self.create_preset_button.clicked.connect(self.create_preset)
        self.layout.addWidget(self.create_preset_button)

        self.timer_label = QLabel('Timer: 10:00.00')
        self.timer_label.setStyleSheet("font-size: 60px")
        self.layout.addWidget(self.timer_label)

        self.preset_created_button = QPushButton('Preset Created')
        self.preset_created_button.clicked.connect(self.preset_created)
        self.layout.addWidget(self.preset_created_button)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.remaining_time = QTime(0, 10, 0, 0)
        self.start_time = datetime.now()  # Initialize start_time

        self.load_state()

    def load_state(self):
        if os.path.exists('state.json'):
            with open('state.json', 'r') as f:
                data = json.load(f)
                self.project_name_input.setText(data.get('project_name', ''))
                self.project_name_label.setText(data.get('project_name', ''))
                self.preset_label.setText(f"Preset: {data.get('presets_count', 0)}")

    def save_project_name(self):
        self.project_name_label.setText(self.project_name_input.text())
        current_preset = int(self.preset_label.text().split(': ')[1])
        with open('state.json', 'w') as f:
            json.dump({'project_name': self.project_name_input.text(), 'presets_count': current_preset}, f)

    def increment_preset(self):
        current_preset = int(self.preset_label.text().split(': ')[1])
        self.preset_label.setText(f'Preset: {current_preset + 1}')
        self.save_project_name()

    def decrement_preset(self):
        current_preset = int(self.preset_label.text().split(': ')[1])
        self.preset_label.setText(f'Preset: {max(0, current_preset - 1)}')
        self.save_project_name()

    def create_preset(self):
        self.timer.start(10)
        self.start_time = datetime.now()  # Update start_time when preset is created

    def update_progress(self):
        self.remaining_time = self.remaining_time.addMSecs(-10)
        self.timer_label.setText(f'Timer: {self.remaining_time.toString("mm:ss.zzz")[:-1]}')

        if self.remaining_time == QTime(0, 0, 0, 0):
            self.timer.stop()
            self.remaining_time = QTime(0, 10, 0, 0)
            self.timer_label.setText('Timer: 10:00.00')
            self.increment_preset()

    def preset_created(self):
        if self.start_time is not None:
            elapsed_time = datetime.now() - self.start_time
            current_preset = int(self.preset_label.text().split(': ')[1])
            with open('track.json', 'a') as f:
                json.dump({'elapsed_time': str(elapsed_time), 'current_preset': current_preset}, f)
                f.write('\n')  # Add a newline for each new entry
            self.timer.stop()
            self.remaining_time = QTime(0, 10, 0, 0)
            self.timer_label.setText('Timer: 10:00.00')
            self.increment_preset()
        else:
            print("Preset has not been started yet.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProjectTrackerApp()
    window.show()
    sys.exit(app.exec_())
