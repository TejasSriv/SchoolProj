from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QComboBox, QTextEdit, QDateEdit, QCheckBox, QScrollArea, QMessageBox
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QDate, QRegExp, Qt, pyqtSignal

import mysql.connector
from models.student import Student
from controllers.student_controller import StudentDBManager

class StudentDetailView(QWidget):

    student_saved = pyqtSignal()
    student_deleted = pyqtSignal()
    back_to_list = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.student = None
        self.student_db_manager = StudentDBManager()
        self.current_mode = 'view'

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setAlignment(Qt.AlignTop)

        int_fields = [
            "scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"
        ]

        self.fields = {
            "scholar_id": QLineEdit(),
            "apaar_id": QLineEdit(),
            "permanent_enrollment_number": QLineEdit(),
            "name": QLineEdit(),
            "class_name": QLineEdit(),
            "dob": QDateEdit(),
            "gender": QComboBox(),
            "social_category": QComboBox(),
            "father": QLineEdit(),
            "mother": QLineEdit(),
            "last_school": QLineEdit(),
            "tc_number": QLineEdit(),
            "address": QTextEdit(),
            "city": QLineEdit(),
            "state": QLineEdit(),
            "admission_date": QDateEdit(),
            "contact": QLineEdit(),
            "alternate_contact": QLineEdit(),
            "email": QLineEdit(),
            "aadhaar": QCheckBox("Has Aadhaar?"),
            "birth_certificate": QCheckBox("Has Birth Certificate?")
        }

        self.fields["gender"].addItems(["Male", "Female", "Other"])
        self.fields["social_category"].addItems(["General", "SC", "ST", "OBC", "Other"])
        
        for key in ["dob", "admission_date"]:
            self.fields[key].setCalendarPopup(True)
            self.fields[key].setDisplayFormat("yyyy-MM-dd")
            self.fields[key].setDate(QDate.currentDate())

        digit_validator = QRegExpValidator(QRegExp(r'^\d{0,20}$'), self)
        for key in int_fields:
            self.fields[key].setValidator(digit_validator)
            self.fields[key].setMaxLength(20)

        for key, widget in self.fields.items():
            if isinstance(widget, QCheckBox):
                form_layout.addWidget(widget)
            else:
                label_text = key.replace("_", " ").title()
                if key == "class_name":
                    label_text = "Class:"
                label = QLabel(label_text)
                form_layout.addWidget(label)
                form_layout.addWidget(widget)

        scroll_content.setLayout(form_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("Back to List")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        self.btn_layout.addWidget(self.back_btn)
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.edit_btn)
        self.btn_layout.addWidget(self.delete_btn)
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(self.btn_layout)

        self.back_btn.clicked.connect(lambda: (self.back_to_list.emit(), self.back_btn.setFocusPolicy(Qt.NoFocus)))
        self.edit_btn.clicked.connect(lambda: (self.set_edit_mode(), self.edit_btn.setFocusPolicy(Qt.NoFocus)))
        self.delete_btn.clicked.connect(lambda: (self.delete_student(), self.delete_btn.setFocusPolicy(Qt.NoFocus)))
        self.save_btn.clicked.connect(lambda: (self.save_student_data(), self.save_btn.setFocusPolicy(Qt.NoFocus)))
        self.cancel_btn.clicked.connect(lambda: (self.set_view_mode(), self.cancel_btn.setFocusPolicy(Qt.NoFocus)))

        self.required_fields = ["scholar_id", "name"]

    def set_student(self, student: Student = None, mode='view'):
        
        self.student = student
        self.current_mode = mode

        if self.student:
            self._populate_fields(self.student)
            if mode == 'view':
                self.set_view_mode()
            elif mode == 'edit':
                self.set_edit_mode()
            else:
                 self.set_add_mode()
        else:
            self.set_add_mode()

    def _populate_fields(self, student: Student):
        
        for key, widget in self.fields.items():
            value = getattr(student, key, None)
            
            if value is None:
                if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                    widget.clear()
                elif isinstance(widget, QComboBox):
                    widget.setCurrentIndex(0)
                elif isinstance(widget, QDateEdit):
                    widget.setDate(QDate.currentDate())
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(False)
                continue

            if isinstance(widget, QLineEdit):
                widget.setText(str(value))
            elif isinstance(widget, QTextEdit):
                widget.setPlainText(str(value))
            elif isinstance(widget, QComboBox):
                idx = widget.findText(str(value))
                if idx >= 0:
                    widget.setCurrentIndex(idx)
            elif isinstance(widget, QDateEdit):
                if isinstance(value, QDate):
                    widget.setDate(value)
                elif isinstance(value, (str, bytes)):
                    date_str = value.decode('utf-8') if isinstance(value, bytes) else value
                    qdate = QDate.fromString(date_str, "yyyy-MM-dd")
                    if qdate.isValid():
                        widget.setDate(qdate)
                    else:
                        widget.setDate(QDate.currentDate())
            elif isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))

    def set_view_mode(self):
        self.current_mode = 'view'
        
        if self.student and self.student.name:
            self.parent().setWindowTitle(f"Student Details: {self.student.name}")
        else:
            self.parent().setWindowTitle("Student Details")

        for key, widget in self.fields.items():
            if key == "scholar_id" and self.student:
                widget.setReadOnly(True)
            elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(True)
            elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setEnabled(False)
        
        self.back_btn.setVisible(True)
        self.edit_btn.setVisible(True)
        self.delete_btn.setVisible(True)
        self.save_btn.setVisible(False)
        self.cancel_btn.setVisible(False)

    def set_edit_mode(self):
        self.current_mode = 'edit'
        if self.student and self.student.name:
            self.parent().setWindowTitle(f"Edit Student: {self.student.name}")
        else:
            self.parent().setWindowTitle("Edit Student")

        for key, widget in self.fields.items():
            if key == "scholar_id":
                 widget.setReadOnly(self.student is not None and self.student.scholar_id is not None)
            elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(False)
            elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setEnabled(True)
        
        self.back_btn.setVisible(False)
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)
        self.save_btn.setVisible(True)
        self.cancel_btn.setVisible(True)

    def set_add_mode(self):
        self.current_mode = 'add'
        self.parent().setWindowTitle("Add New Student")
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(False)
                widget.clear()
            elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setEnabled(True)
            if isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)

        self.fields["scholar_id"].setReadOnly(False)

        self.back_btn.setVisible(False)
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)
        self.save_btn.setVisible(True)
        self.cancel_btn.setVisible(True)

    def get_data_from_fields(self) -> Student:
        """Collects data from the form fields and returns a Student object."""
        data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                text = widget.text().strip()
                if key in ["scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"]:
                    try:
                        data[key] = int(text) if text else None
                    except ValueError:
                        data[key] = None
                else:
                    data[key] = text if text else None
            elif isinstance(widget, QTextEdit):
                text = widget.toPlainText().strip()
                data[key] = text if text else None
            elif isinstance(widget, QComboBox):
                data[key] = widget.currentText() if widget.currentText() else None
            elif isinstance(widget, QDateEdit):
                data[key] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QCheckBox):
                data[key] = widget.isChecked()
        
        return Student(**data)

    def validate_input(self, student_data: dict) -> list:
        missing_fields = []
        validation_map = {
            "scholar_id": "Scholar ID",
            "name": "Name",
            "class_name": "Class"
        }

        for key in self.required_fields:
            value = student_data.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                display_name = validation_map.get(key, key.replace("_", " ").title())
                missing_fields.append(display_name)
        

        if self.current_mode == 'add':
            scholar_id = student_data.get('scholar_id')
            if scholar_id is not None and self.student_db_manager.get_student_by_id(scholar_id):
                missing_fields.append("Scholar ID already exists. Please choose a unique Scholar ID.")

        return missing_fields

    def save_student_data(self):
        collected_data = self.get_data_from_fields().to_dict()
        validation_errors = self.validate_input(collected_data)

        if validation_errors:
            QMessageBox.warning(self, "Validation Error", f"Please correct the following issues:\n- " + "\n- ".join(validation_errors))
            return

        new_student = self.get_data_from_fields()

        try:
            if self.current_mode == 'add':
                self.student_db_manager.add_student(new_student)
                QMessageBox.information(self, "Success", "Student added successfully.")
            elif self.current_mode == 'edit':
                self.student_db_manager.update_student(self.student.scholar_id, new_student)
                QMessageBox.information(self, "Success", f"Student {new_student.name} updated successfully.")
            
            self.student_saved.emit()
            self.student = self.student_db_manager.get_student_by_id(new_student.scholar_id)
            if self.student:
                self.set_student(self.student, mode='view')
            else:
                QMessageBox.critical(self, "Error", "Student data not found after save. Returning to list.")
                self.back_to_list.emit()

        except mysql.connector.Error as err:
            if err.errno == 1062:
                QMessageBox.warning(self, "Duplicate Entry", f"A student with this Scholar ID, APAAR ID, or Permanent Enrollment Number already exists. Error: {err}")
            else:
                QMessageBox.critical(self, "Database Error", f"Error saving student: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Application Error", f"An unexpected error occurred during student save: {e}")

    def delete_student(self):
        if not self.student or not self.student.scholar_id:
            QMessageBox.critical(self, "Error", "No student selected for deletion.")
            return

        scholar_id_to_delete = self.student.scholar_id
        student_name = self.student.name if self.student.name else "selected student"

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete student: {student_name} (ID: {scholar_id_to_delete})?\nThis action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.student_db_manager.delete_student(scholar_id_to_delete)
                QMessageBox.information(self, "Success", f"Student {student_name} deleted successfully.")
                self.student_deleted.emit()
                self.back_to_list.emit()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Database Error", f"Error deleting student: {err}")
            except Exception as e:
                QMessageBox.critical(self, "Application Error", f"An unexpected error occurred during student deletion: {e}")
