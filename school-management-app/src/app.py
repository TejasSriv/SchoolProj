import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

from controllers.auth import check_user_credentials
from views.admin_dashboard import AdminDashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management App")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add vertical stretch to center the form vertically
        main_layout.addStretch(1)

        # Form container with fixed width
        form_container = QWidget()
        form_container.setFixedWidth(350)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)  # Add more spacing between fields
        form_container.setLayout(form_layout)

        # Welcome label
        label = QLabel("Welcome to the School Management App!", self)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(label)

        # Username field
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)  # Increase height
        form_layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)  # Increase height
        form_layout.addWidget(self.password_input)

        # Login button
        login_button = QPushButton("Login", self)
        login_button.setFixedHeight(40)  # Increase height
        login_button.clicked.connect(self.handle_login)  # Connect to login handler
        form_layout.addWidget(login_button)

        # Center the form horizontally
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(form_container)
        h_layout.addStretch(1)
        main_layout.addLayout(h_layout)

        # Add vertical stretch to center the form vertically
        main_layout.addStretch(1)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if check_user_credentials(username, password):
            self.dashboard = AdminDashboard(
                username,
                self.geometry()
            )
            self.dashboard.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())