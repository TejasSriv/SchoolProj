from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PyQt5.QtCore import Qt

from views.student_section import StudentSection

class AdminDashboard(QMainWindow):
    def __init__(self, username, geometry=None):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        if geometry:
            self.setGeometry(geometry)
        else:
            self.setGeometry(150, 150, 900, 700)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Sidebar as a QWidget for styling
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(180)
        sidebar_widget.setStyleSheet("""
            background-color: #232946;
            border-top-right-radius: 12px;
            border-bottom-right-radius: 12px;
        """)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(18)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_widget.setLayout(sidebar_layout)

        # Logo or title
        logo = QLabel("SCHOOL")
        logo.setStyleSheet("color: #eebbc3; font-size: 22px; font-weight: bold; letter-spacing: 2px;")
        logo.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(10)

        # Sidebar buttons with modern style
        btn_style = """
            QPushButton {
                color: #eebbc3;
                background: transparent;
                border: none;
                padding: 12px 0;
                font-size: 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #393e6a;
                border-radius: 6px;
            }
        """

        btn_dashboard = QPushButton("🏠  Dashboard")
        btn_dashboard.setStyleSheet(btn_style)
        btn_students = QPushButton("👨‍🎓  Students")
        btn_students.setStyleSheet(btn_style)
        btn_teachers = QPushButton("👩‍🏫  Teachers")
        btn_teachers.setStyleSheet(btn_style)
        btn_logout = QPushButton("🚪  Logout")
        btn_logout.setStyleSheet(btn_style + "QPushButton {color: #ffadad;}")

        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_students)
        sidebar_layout.addWidget(btn_teachers)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(btn_logout)

        # Content area (stacked widget for switching screens)
        self.stack = QStackedWidget()
        dashboard_label = QLabel(f"Welcome, {username}! This is the admin dashboard.")
        dashboard_label.setAlignment(Qt.AlignCenter)
        dashboard_label.setStyleSheet("font-size: 22px; color: #232946;")
        students_widget = StudentSection()
        teachers_label = QLabel("Teachers Section")
        teachers_label.setAlignment(Qt.AlignCenter)
        teachers_label.setStyleSheet("font-size: 20px; color: #232946;")

        self.stack.addWidget(dashboard_label)  # index 0
        self.stack.addWidget(students_widget)   # index 1
        self.stack.addWidget(teachers_label)   # index 2

        # Connect sidebar buttons to stack
        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_students.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_teachers.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_logout.clicked.connect(self.logout)

        # Add sidebar and content to main layout
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stack, 4)

    def logout(self):
        self.close()
        from app import MainWindow
        self.login_window = MainWindow()
        self.login_window.setGeometry(self.geometry())
        self.login_window.show()