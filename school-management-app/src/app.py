import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

# Removed: from qt_material import apply_stylesheet # <--- REMOVED FOR FRESH COLOR CONTROL

from controllers.auth import AuthManager
from views.admin_dashboard import AdminDashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Presidency Public School - Login")
        self.setGeometry(100, 100, 1000, 600)

        # Set background color for the main window (Very Light Gray)
        self.setStyleSheet("QMainWindow { background-color: #F8F9FA; }")

        self.auth_manager = AuthManager()
        self.auth_manager.create_admin_table_if_not_exists()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, '..', 'resources', 'logo.png')
        app_icon = QIcon(logo_path)
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)
        else:
            print(f"Warning: Could not load window icon from {logo_path}")


        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add vertical stretch to center the form vertically
        main_layout.addStretch(1)

        # Form container with fixed width (Pure White background)
        form_container = QWidget()
        form_container.setObjectName("formContainer") # Give it an object name for targeting
        form_container.setFixedWidth(350)
        form_container.setStyleSheet("""
            #formContainer {
                background-color: #FFFFFF; /* Pure White */
                border-radius: 8px; /* Slightly rounded corners for a softer look */
                padding: 25px; /* Add some internal padding */
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20) # Add more spacing between fields
        form_container.setLayout(form_layout)

        try:
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                print(f"Error: Could not load logo image from {logo_path}")
                logo_label = QLabel("Logo Missing")
            else:
                scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label = QLabel()
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                logo_label.setFixedSize(100, 100)
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = QLabel("Logo Error")
        
        form_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        
        # School Name Label (Primary Dark Text)
        label = QLabel("The Presidency Public School", self)
        label.setObjectName("schoolNameLabel") # Object name for targeting
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            #schoolNameLabel {
                color: #333333; /* Primary Dark Text */
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px; /* Space below label */
            }
        """)
        form_layout.addWidget(label)

        # Username field (Pure White background, Dark Text, Neutral Gray border)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; /* Pure White */
                color: #333333; /* Primary Dark Text */
                border: 1px solid #6C757D; /* Neutral Gray border */
                border-radius: 4px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #28A745; /* Success Green on focus */
                outline: none; /* Remove default focus outline */
            }
            QLineEdit::placeholder {
                color: #666666; /* Secondary Text */
            }
        """)
        form_layout.addWidget(self.username_input)

        # Password field (Pure White background, Dark Text, Neutral Gray border)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; /* Pure White */
                color: #333333; /* Primary Dark Text */
                border: 1px solid #6C757D; /* Neutral Gray border */
                border-radius: 4px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #28A745; /* Success Green on focus */
                outline: none;
            }
            QLineEdit::placeholder {
                color: #666666; /* Secondary Text */
            }
        """)
        form_layout.addWidget(self.password_input)

        # Login button (Success Green background, White Text)
        login_button = QPushButton("Login", self)
        login_button.setObjectName("loginButton") # Object name for targeting
        login_button.setFixedHeight(40)
        login_button.clicked.connect(self.handle_login)
        login_button.setStyleSheet("""
            #loginButton {
                background-color: #28A745; /* Success Green */
                color: #FFFFFF; /* White Text */
                border: none;
                border-radius: 5px;
                padding: 8px 20px; /* Adjusted padding to fit height */
                font-weight: bold;
                font-size: 16px;
            }
            #loginButton:hover {
                background-color: #218838; /* Darker Green on hover */
            }
            #loginButton:pressed {
                background-color: #1E7E34; /* Even Darker Green on pressed */
            }
        """)
        form_layout.addWidget(login_button)

        # Enter key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(form_container)
        h_layout.addStretch(1)
        main_layout.addLayout(h_layout)

        main_layout.addStretch(1)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.auth_manager.authenticate(username, password):
            app_window_icon = self.windowIcon()
            self.dashboard = AdminDashboard(
                username,
                self.geometry(),
                app_window_icon
            )
            self.dashboard.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("The Presidency Public School")
    
    # Removed apply_stylesheet for full color control as requested
    # apply_stylesheet(app, theme='light_blue.xml') 
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())