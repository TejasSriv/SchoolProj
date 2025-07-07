from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
import mysql.connector

from controllers.student_controller import StudentDBManager
from models.student import Student
from .student_dialog import StudentDialog

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
        search_btn.clicked.connect(self.search_students)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        
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
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Student")
        edit_btn = QPushButton("Edit Student")
        delete_btn = QPushButton("Delete Student")
        add_btn.clicked.connect(self.add_student)
        edit_btn.clicked.connect(self.edit_student)
        delete_btn.clicked.connect(self.delete_student)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)

        layout.addStretch(1)
        self.setLayout(layout)

        self.load_students()

    def load_students(self):
        self.table.setRowCount(0)
        try:
            students = self.student_db_manager.get_all_students()
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
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error loading students: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Application Error", f"An unexpected error occurred: {e}")


    def search_students(self):
        keyword = self.search_input.text().strip()
        self.table.setRowCount(0)
        try:
            students = self.student_db_manager.search_students(keyword)
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
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error searching students: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Application Error", f"An unexpected error occurred: {e}")

    def add_student(self):
        dialog = StudentDialog(self)
        if dialog.exec_():
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

    def edit_student(self):
        selected_row_idx = self.table.currentRow()
        if selected_row_idx < 0:
            QMessageBox.warning(self, "Select Student", "Please select a student to edit.")
            return

        student_to_edit = self.table.verticalHeaderItem(selected_row_idx).data(Qt.UserRole)
        if not student_to_edit:
            QMessageBox.critical(self, "Error", "Could not retrieve student data for editing.")
            return

        dialog = StudentDialog(self, student_to_edit)
        if dialog.exec_():
            updated_student = dialog.get_data()
            try:
                self.student_db_manager.update_student(updated_student)
                self.load_students()
                QMessageBox.information(self, "Success", "Student updated successfully.")
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    QMessageBox.warning(self, "Duplicate Entry", f"The updated APAAR ID or Permanent Enrollment Number already exists for another student. Details: {err}")
                else:
                    QMessageBox.critical(self, "Database Error", f"Error updating student: {err}")
            except Exception as e:
                QMessageBox.critical(self, "Application Error", f"An unexpected error occurred during student update: {e}")

    def delete_student(self):
        selected_row_idx = self.table.currentRow()
        if selected_row_idx < 0:
            QMessageBox.warning(self, "Select Student", "Please select a student to delete.")
            return

        student_to_delete = self.table.verticalHeaderItem(selected_row_idx).data(Qt.UserRole)
        if not student_to_delete or not student_to_delete.scholar_id:
            QMessageBox.critical(self, "Error", "Could not retrieve Scholar ID for deletion.")
            return

        scholar_id_to_delete = student_to_delete.scholar_id
        student_name = student_to_delete.name if student_to_delete.name else "selected student"

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete student: {student_name} (ID: {scholar_id_to_delete})?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.student_db_manager.delete_student(scholar_id_to_delete)
                QMessageBox.information(self, "Success", f"Student {student_name} deleted successfully.")
                self.load_students()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Database Error", f"Error deleting student: {err}")
            except Exception as e:
                QMessageBox.critical(self, "Application Error", f"An unexpected error occurred during student deletion: {e}")