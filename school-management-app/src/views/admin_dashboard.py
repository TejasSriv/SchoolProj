from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt

class AdminDashboard(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(150, 150, 900, 700)
        label = QLabel(f"Welcome, {username}! This is the admin dashboard.", self)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)