from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from controllers.db import get_connection
from .student_dialog import StudentDialog

class StudentSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Student Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

                # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or ID")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_students)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # Table for students
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "scholar_id", "name", "class", "address"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Buttons
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

        # Add more widgets for student management here (e.g., table, add/edit/delete buttons)
        layout.addStretch(1)
        self.setLayout(layout)

        self.load_students()

    def load_students(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT scholar_id, name, class, address FROM students")
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            for col_idx, key in enumerate(["scholar_id", "name", "class", "address"]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data.get(key, ""))))
        cursor.close()
        conn.close()

    def search_students(self):
        keyword = self.search_input.text()
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT scholar_id, name, class, address FROM students WHERE name LIKE %s OR scholar_id LIKE %s"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        for row_idx, row_data in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            for col_idx, key in enumerate(["scholar_id", "name", "class", "address"]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(row_data.get(key, ""))))
        cursor.close()
        conn.close()

    def add_student(self):
        dialog = StudentDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (
                    scholar_id, apaar_id, permanent_enrollment_number, name, class, dob, gender,
                    social_category, father, mother, last_school, tc_number, address, city, state,
                    contact, alternate_contact, email, aadhaar, birth_certificate
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(data[k] for k in [
                "scholar_id", "apaar_id", "permanent_enrollment_number", "name", "class", "dob", "gender",
                "social_category", "father", "mother", "last_school", "tc_number", "address", "city", "state",
                "contact", "alternate_contact", "email", "aadhaar", "birth_certificate"
            ]))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_students()
            QMessageBox.information(self, "Success", "Student added successfully.")

    def edit_student(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Select Student", "Please select a student to edit.")
            return
        student = {}
        for col, key in enumerate([
            "scholar_id", "apaar_id", "permanent_enrollment_number", "name", "class", "dob", "gender",
            "social_category", "father", "mother", "last_school", "tc_number", "address", "city", "state",
            "contact", "alternate_contact", "email", "aadhaar", "birth_certificate"
        ]):
            student[key] = self.table.item(selected, col).text()
        dialog = StudentDialog(self, student)
        if dialog.exec_():
            data = dialog.get_data()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students SET
                    apaar_id=%s, permanent_enrollment_number=%s, name=%s, class=%s, dob=%s, gender=%s,
                    social_category=%s, father=%s, mother=%s, last_school=%s, tc_number=%s, address=%s,
                    city=%s, state=%s, contact=%s, alternate_contact=%s, email=%s, aadhaar=%s, birth_certificate=%s
                WHERE scholar_id=%s
            """, tuple(
                [data[k] for k in [
                    "apaar_id", "permanent_enrollment_number", "name", "class", "dob", "gender",
                    "social_category", "father", "mother", "last_school", "tc_number", "address", "city", "state",
                    "contact", "alternate_contact", "email", "aadhaar", "birth_certificate"
                ]] + [student["scholar_id"]]
            ))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_students()
            QMessageBox.information(self, "Success", "Student updated successfully.")

    def delete_student(self):
        QMessageBox.information(self, "Delete Student", "Delete student dialog goes here.")