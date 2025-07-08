import os
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QMessageBox, QFrame # QFrame added for sidebar
)
from PyQt5.QtCore import Qt

from views.student_section import StudentSection
from views.student_detail_view import StudentDetailView # <-- NEW IMPORT

class AdminDashboard(QMainWindow):
    def __init__(self, username, geometry=None, app_window_icon=None):
        super().__init__()
        self.setWindowTitle(f"Admin Dashboard") 
        
        if geometry:
            self.setGeometry(geometry)
        else:
            self.setGeometry(150, 150, 900, 700)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.sidebar_widget = QFrame()
        self.sidebar_widget.setFixedWidth(180)
        self.sidebar_widget.setStyleSheet("""
            QFrame {
                background-color: #ffcb06;
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }
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
            QPushButton#logoutBtn {
                color: #ffadad;
            }
        """)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(18)
        sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_widget.setLayout(sidebar_layout)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, '../..', 'resources', 'logo.png')
        app_icon = QIcon(logo_path)
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)
        else:
            print(f"Warning: Could not load window icon from {logo_path}")

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

        # Logo or title
        self.app_logo_label = logo_label
        self.app_logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.app_logo_label, alignment=Qt.AlignCenter)
        sidebar_layout.addSpacing(10)

        self.btn_dashboard = QPushButton("🏠  Dashboard")
        self.btn_students = QPushButton("👨‍🎓  Students")
        self.btn_teachers = QPushButton("👩‍🏫  Teachers")
        self.btn_logout = QPushButton("🚪  Logout")
        self.btn_logout.setObjectName("logoutBtn")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_students)
        sidebar_layout.addWidget(self.btn_teachers)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(self.btn_logout)

        self.stack = QStackedWidget()
        

        # 0. Dashboard placeholder
        dashboard_label = QLabel(f"Welcome, {username}! This is the admin dashboard.")
        dashboard_label.setAlignment(Qt.AlignCenter)
        dashboard_label.setStyleSheet("font-size: 22px; color: #232946;")
        self.dashboard_idx = self.stack.addWidget(dashboard_label) # Store index 0

        # 1. Student Section (List View)
        self.students_widget = StudentSection() 
        self.student_list_idx = self.stack.addWidget(self.students_widget) # Store index 1

        # 2. Teacher Section (Placeholder for now)
        teachers_label = QLabel("Teachers Section")
        teachers_label.setAlignment(Qt.AlignCenter)
        teachers_label.setStyleSheet("font-size: 20px; color: #232946;")
        self.teachers_idx = self.stack.addWidget(teachers_label) # Store index 2

        # 3. Student Detail View (New Form View)
        # It's important to pass 'self' as the parent so StudentDetailView can update AdminDashboard's title
        self.student_detail_view = StudentDetailView(parent=self)
        self.student_detail_view_idx = self.stack.addWidget(self.student_detail_view) # Store new index, likely 3

        # --- Connect sidebar buttons to stack using a helper function ---
        self.btn_dashboard.clicked.connect(lambda: self.set_current_page(self.dashboard_idx, "Dashboard"))
        self.btn_students.clicked.connect(lambda: self.set_current_page(self.student_list_idx, "Student Management"))
        self.btn_teachers.clicked.connect(lambda: self.set_current_page(self.teachers_idx, "Teacher Management"))
        self.btn_logout.clicked.connect(self.logout)

        # --- Connect Signals for Navigation and Data Refresh ---

        # From StudentSection to AdminDashboard (to show detail view)
        self.students_widget.show_student_details.connect(self.display_student_detail)
        self.students_widget.show_add_student.connect(self.display_add_student_form)

        # From StudentDetailView to AdminDashboard (to go back or refresh list)
        self.student_detail_view.student_saved.connect(self.handle_student_data_change)
        self.student_detail_view.student_deleted.connect(self.handle_student_data_change)
        self.student_detail_view.back_to_list.connect(self.show_student_list)

        # Add sidebar and content to main layout (Crucial: ensure stretch factor for content)
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(self.stack, 4) # <-- IMPORTANT: Added the stretch factor back!

        # Set initial page on startup
        self.set_current_page(self.dashboard_idx, "Dashboard") # Start on Dashboard

    def set_current_page(self, index, title_suffix=""):
        """
        Sets the current page of the QStackedWidget and updates the main window title.
        Also handles specific page behaviors like refreshing student list.
        """
        self.stack.setCurrentIndex(index)
        self.setWindowTitle(f"Admin Dashboard - {title_suffix}")

        # Specific actions when switching pages
        if index == self.student_list_idx:
            # Ensure the student list is reloaded/refreshed when navigating to it
            self.students_widget.load_students() 
        # Add similar logic for other sections if they need data refresh

    def display_student_detail(self, student_obj, mode):
        """
        Slot to receive signal from StudentSection and show StudentDetailView for an existing student.
        """
        self.student_detail_view.set_student(student_obj, mode)
        self.stack.setCurrentIndex(self.student_detail_view_idx)

    def display_add_student_form(self):
        """
        Slot to receive signal from StudentSection and show StudentDetailView in 'add' mode.
        """
        self.student_detail_view.set_student(None, 'add') # Pass None for new student
        self.stack.setCurrentIndex(self.student_detail_view_idx)

    def show_student_list(self):
        """
        Slot to switch back to the StudentSection (list view).
        This method will also be called by handle_student_data_change.
        """
        self.set_current_page(self.student_list_idx, "Student Management")

    def handle_student_data_change(self):
        """
        Slot to handle student_saved or student_deleted signals.
        Reloads the student list and returns to it.
        """
        self.show_student_list() # This function already reloads and switches

    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            from app import MainWindow # Import MainWindow here to avoid circular dependency
            # Get current geometry before hiding/closing
            current_geometry = self.geometry()
            self.hide() # Hide current window
            
            # Create a new login window and set its geometry
            login_window = MainWindow()
            login_window.setGeometry(current_geometry)
            login_window.show()
            self.close() # Close dashboard