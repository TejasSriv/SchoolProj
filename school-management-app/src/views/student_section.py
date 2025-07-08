from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
import mysql.connector

from controllers.student_controller import StudentDBManager
from models.student import Student


class StudentSection(QWidget):
    show_student_details = pyqtSignal(object, str)
    show_add_student = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.student_db_manager = StudentDBManager()

        layout = QVBoxLayout()
        title = QLabel("Student Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or ID")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(lambda: (self.search_students(), search_btn.setFocusPolicy(Qt.NoFocus)))
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        self.search_status_label = QLabel("")
        self.search_status_label.setStyleSheet("font-style: italic; color: gray;")
        layout.addWidget(self.search_status_label)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellDoubleClicked.connect(self.view_student_details)

        self.display_column_names = {
            "scholar_id": "Scholar ID",
            "name": "Name",
            "class_name": "Class",
            "address": "Address",
            "contact": "Contact"
        }
        self.table.setColumnCount(len(self.display_column_names))
        self.table.setHorizontalHeaderLabels(list(self.display_column_names.values()))
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)

        bottom_buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Add Student")
        add_btn.clicked.connect(lambda: (self.add_student(), add_btn.setFocusPolicy(Qt.NoFocus)))
        
        self.clear_search_btn = QPushButton("Clear Search")
        self.clear_search_btn.clicked.connect(lambda: (self.clear_search(), self.clear_search_btn.setFocusPolicy(Qt.NoFocus)))
        self.clear_search_btn.setVisible(False)

        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(lambda: (self.load_students(), self.refresh_btn.setFocusPolicy(Qt.NoFocus)))

        bottom_buttons_layout.addWidget(add_btn)
        bottom_buttons_layout.addWidget(self.refresh_btn)
        bottom_buttons_layout.addStretch(1)
        bottom_buttons_layout.addWidget(self.clear_search_btn)
        
        layout.addLayout(bottom_buttons_layout)

        self.setLayout(layout)

        self.load_students()

    def load_students(self, students=None):

        self.table.setRowCount(0)
        
        if students is None:
            try:
                students = self.student_db_manager.get_all_students()
                self.search_status_label.setText(f"")
                self.search_input.clear()
                self.clear_search_btn.setVisible(False)
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Database Error", f"Error loading students: {err}")
                return
            except Exception as e:
                QMessageBox.critical(self, "Application Error", f"An unexpected error occurred: {e}")
                return
            
        else:
            self.search_status_label.setText(f"Showing {len(students)} search results.")
            self.clear_search_btn.setVisible(True)


        for row_idx, student in enumerate(students):
            self.table.insertRow(row_idx)
            self.table.setVerticalHeaderItem(row_idx, QTableWidgetItem(""))
            self.table.verticalHeaderItem(row_idx).setData(Qt.UserRole, student)

            for col_idx, attr_name in enumerate(self.display_column_names.keys()):
                value = getattr(student, attr_name, "")
                if isinstance(value, (type(None))) and value is not False:
                    value_str = ""
                elif isinstance(value, bool):
                    value_str = "Yes" if value else "No"
                elif isinstance(value, (list, tuple)):
                     value_str = str(value[0]) if value and isinstance(value, tuple) else str(value)
                elif isinstance(value, (int, float)):
                    value_str = str(value)
                else:
                    value_str = str(value)
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(value_str))

    def search_students(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            self.load_students()
            return

        try:
            students = self.student_db_manager.search_students(keyword)
            self.load_students(students)
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error searching students: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Application Error", f"An unexpected error occurred: {e}")

    def clear_search(self):
        self.search_input.clear()
        self.load_students()

    def add_student(self):
        self.show_add_student.emit()

    def view_student_details(self, row, column):
        selected_student = self.table.verticalHeaderItem(row).data(Qt.UserRole)
        if selected_student:
            self.show_student_details.emit(selected_student, 'view')
        else:
            QMessageBox.critical(self, "Error", "Could not retrieve student data for details view.")