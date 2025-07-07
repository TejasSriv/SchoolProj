from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PyQt5.QtCore import Qt

class AdminDashboard(QMainWindow):
    def __init__(self, username, geometry=None):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        if geometry:
            self.setGeometry(geometry)
        else:
            # Default geometry if not provided
            self.setGeometry(150, 150, 900, 700)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(20)
        sidebar.setAlignment(Qt.AlignTop)

        btn_dashboard = QPushButton("Dashboard")
        btn_students = QPushButton("Students")
        btn_teachers = QPushButton("Teachers")
        btn_logout = QPushButton("Logout")

        sidebar.addWidget(btn_dashboard)
        sidebar.addWidget(btn_students)
        sidebar.addWidget(btn_teachers)
        sidebar.addStretch(1)
        sidebar.addWidget(btn_logout)

        # Content area (stacked widget for switching screens)
        self.stack = QStackedWidget()
        dashboard_label = QLabel(f"Welcome, {username}! This is the admin dashboard.")
        dashboard_label.setAlignment(Qt.AlignCenter)
        students_label = QLabel("Students Section")
        students_label.setAlignment(Qt.AlignCenter)
        teachers_label = QLabel("Teachers Section")
        teachers_label.setAlignment(Qt.AlignCenter)

        self.stack.addWidget(dashboard_label)  # index 0
        self.stack.addWidget(students_label)   # index 1
        self.stack.addWidget(teachers_label)   # index 2

        # Connect sidebar buttons to stack
        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_students.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_teachers.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_logout.clicked.connect(self.logout)

        # Add sidebar and content to main layout
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 4)

    def logout(self):
        self.close()
        
        from app import MainWindow
        self.login_window = MainWindow()
        self.login_window.setGeometry(self.geometry())
        self.login_window.show()