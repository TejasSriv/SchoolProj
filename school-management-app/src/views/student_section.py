from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView, QDialog
)
from PyQt5.QtCore import Qt
import mysql.connector

from controllers.student_controller import StudentDBManager
from models.student import Student
from .student_details_dialog import StudentDetailsDialog

class StudentSection(QWidget):
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

        bottom_buttons_layout.addWidget(add_btn)
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
        dialog = StudentDetailsDialog(self, student=None, mode='add')
        if dialog.exec_() == QDialog.Accepted:
            new_student = dialog.get_data()
            try:
                self.student_db_manager.add_student(new_student)
                self.load_students()
                QMessageBox.information(self, "Success", "Student added successfully.")
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    QMessageBox.warning(self, "Duplicate Entry", f"A student with the provided Scholar ID, APAAR ID, or Permanent Enrollment Number already exists. Details: {err}")
                else:
                    QMessageBox.critical(self, "Database Error", f"Error adding student: {err}")
            except Exception as e:
                QMessageBox.critical(self, "Application Error", f"An unexpected error occurred during student addition: {e}")

    def view_student_details(self, row, column):
        selected_student = self.table.verticalHeaderItem(row).data(Qt.UserRole)
        if not selected_student:
            QMessageBox.critical(self, "Error", "Could not retrieve student data for details view.")
            return

        dialog = StudentDetailsDialog(self, student=selected_student, mode='view')
        if dialog.exec_() == QDialog.Accepted:
            if self.search_input.text().strip():
                self.search_students()
            else:
                self.load_students()