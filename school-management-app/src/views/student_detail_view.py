import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QComboBox, QTextEdit, QDateEdit, QCheckBox, QScrollArea, QMessageBox,
    QFormLayout, QGroupBox
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QDate, QRegExp, Qt, pyqtSignal

import mysql.connector
from models.student import Student
from controllers.student_controller import StudentDBManager
import datetime

class StudentDetailView(QWidget):

    student_saved = pyqtSignal()
    student_deleted = pyqtSignal()
    back_to_list = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.student = None
        self.original_student_data = None
        self.student_db_manager = StudentDBManager()
        self.current_mode = 'view'

        self.setStyleSheet("QWidget { background-color: #F8F9FA; }")

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("studentDetailScrollArea")
        scroll.setStyleSheet("""
            QScrollArea#studentDetailScrollArea {
                border: none;
                background-color: #F8F9FA;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #6C757D;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setObjectName("studentDetailContent")
        scroll_content.setStyleSheet("""
            QWidget#studentDetailContent {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
            }
        """)
        form_layout = QFormLayout(scroll_content)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        int_fields = [
            "scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"
        ]

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.calendar_icon_path = os.path.join(script_dir, '../..', 'resources', 'calendar-symbol.svg')

        if not os.path.exists(self.calendar_icon_path):
            print(f"Warning: Calendar icon not found at {self.calendar_icon_path}. Falling back to default QDateEdit arrow.")
            calendar_icon_style = """
                QDateEdit::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: center right;
                    width: 20px;
                    border-left: 1px solid #6C757D;
                    background-color: #F0F2F5;
                }
                QDateEdit::down-arrow {
                    image: url();
                }
            """
        else:
            calendar_icon_style = f"""
                QDateEdit::drop-down {{
                    subcontrol-origin: padding;
                    subcontrol-position: center right;
                    width: 24px;
                    border-left: 1px solid #6C757D;
                    border-top-right-radius: 4px;
                    border-bottom-right-radius: 4px;
                    background-color: #F0F2F5;
                }}
                QDateEdit::down-arrow {{
                    image: url({self.calendar_icon_path});
                    width: 16px;
                    height: 16px;
                    padding-right: 2px;
                }}
                QDateEdit::drop-down:hover {{
                    background-color: #E0E2E5;
                }}
            """

        self.input_field_style = f"""
            QLineEdit, QTextEdit, QComboBox, QDateEdit {{
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #6C757D;
                border-radius: 4px;
                padding: 8px;
                min-height: 30px;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {{
                border: 1px solid #28A745;
                outline: none;
            }}
            QLineEdit::placeholder, QTextEdit::placeholder {{
                color: #666666;
            }}
            QComboBox::drop-down {{
                border: 0px;
            }}
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #6C757D;
                selection-background-color: #C1D9E8;
                selection-color: #333333;
                background-color: #FFFFFF;
            }}
            {calendar_icon_style}
        """

        self.read_only_field_style = """
            QLineEdit[readOnly="true"], QTextEdit[readOnly="true"],
            QComboBox:disabled, QDateEdit:disabled, QCheckBox:disabled {
                background-color: #ECEFF1;
                color: #666666;
                border: 1px solid #B0BEC5;
            }
            QLineEdit[readOnly="true"]::placeholder, QTextEdit[readOnly="true"]::placeholder {
                color: #90A4AE;
            }
        """
        
        self.fields = {
            "scholar_id": QLineEdit(),
            "apaar_id": QLineEdit(),
            "permanent_enrollment_number": QLineEdit(),
            "name": QLineEdit(),
            "class_name": QComboBox(),
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
            "aadhaar": QCheckBox(""),
            "birth_certificate": QCheckBox("")
        }

        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit) or isinstance(widget, QComboBox) or isinstance(widget, QDateEdit):
                widget.setStyleSheet(self.input_field_style)
            elif isinstance(widget, QCheckBox):
                widget.setStyleSheet("QCheckBox { color: #333333; }")

        self.fields["gender"].addItems(["Male", "Female", "Other"])
        self.fields["social_category"].addItems(["General", "SC", "ST", "OBC", "Other"])
        self.fields["class_name"].addItems(["Nursery", "LKG", "UKG", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"])
        
        for key in ["dob", "admission_date"]:
            self.fields[key].setCalendarPopup(True)
            self.fields[key].setDisplayFormat("dd-MM-yyyy")
            self.fields[key].setDate(QDate.currentDate())
            self.fields[key].setMaximumDate(QDate.currentDate())

        digit_validator = QRegExpValidator(QRegExp(r'^\d{0,20}$'), self)
        for key in int_fields:
            self.fields[key].setValidator(digit_validator)
            self.fields[key].setMaxLength(20)
            self.fields[key].setPlaceholderText("Enter numbers only")

        for key, widget in self.fields.items():
            label_text = key.replace("_", " ").title()
            if key == "class_name":
                label_text = "Class"
            elif key == "aadhaar":
                label_text = "Aadhaar Card Submitted?"
            elif key == "birth_certificate":
                label_text = "Birth Certificate Submitted?"
            
            label = QLabel(label_text + ":")
            label.setStyleSheet("color: #333333; font-weight: 500;")            
            if isinstance(widget, QCheckBox):
                form_layout.addRow(label, widget)
            elif isinstance(widget, QTextEdit):
                widget.setFixedHeight(60)
                form_layout.addRow(label, widget)
            else:
                widget.setFixedHeight(35)
                form_layout.addRow(label, widget)

        details_group = QGroupBox("Student Information")
        details_group.setObjectName("detailsGroup")
        details_group.setStyleSheet("""
            QGroupBox#detailsGroup {
                font-size: 18px;
                font-weight: bold;
                color: #2C3E50;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox#detailsGroup::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background-color: #FFFFFF;
            }
        """)
        details_group.setLayout(form_layout)
        scroll_content.setLayout(form_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.btn_layout = QHBoxLayout()
        button_base_style = """
            QPushButton {
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                min-width: 100px;
                min-height: 35px;
            }
        """
        
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("secondaryActionBtn")
        self.edit_btn.setStyleSheet(button_base_style + """
            QPushButton#secondaryActionBtn {
                background-color: #6C757D;
                color: #FFFFFF;
            }
            QPushButton#secondaryActionBtn:hover {
                background-color: #5A6268;
            }
            QPushButton#secondaryActionBtn:pressed {
                background-color: #495057;
            }
        """)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("dangerActionBtn")
        self.delete_btn.setStyleSheet(button_base_style + """
            QPushButton#dangerActionBtn {
                background-color: #DC3545;
                color: #FFFFFF;
            }
            QPushButton#dangerActionBtn:hover {
                background-color: #C82333;
            }
            QPushButton#dangerActionBtn:pressed {
                background-color: #B02A37;
            }
        """)

        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("primaryActionBtn")
        self.save_btn.setStyleSheet(button_base_style + """
            QPushButton#primaryActionBtn {
                background-color: #28A745;
                color: #FFFFFF;
            }
            QPushButton#primaryActionBtn:hover {
                background-color: #218838;
            }
            QPushButton#primaryActionBtn:pressed {
                background-color: #1E7E34;
            }
        """)

        self.action_cancel_btn = QPushButton("Back")
        self.action_cancel_btn.setObjectName("secondaryActionBtn") # Reusing secondaryActionBtn style
        self.action_cancel_btn.setStyleSheet(button_base_style + """
            QPushButton#secondaryActionBtn {
                background-color: #6C757D;
                color: #FFFFFF;
            }
            QPushButton#secondaryActionBtn:hover {
                background-color: #5A6268;
            }
            QPushButton#secondaryActionBtn:pressed {
                background-color: #495057;
            }
        """)

        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.edit_btn)
        self.btn_layout.addWidget(self.delete_btn)
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addWidget(self.action_cancel_btn)
        self.btn_layout.addStretch(1)
        main_layout.addLayout(self.btn_layout)

        self.edit_btn.clicked.connect(lambda: (self.set_edit_mode(), self.edit_btn.setFocusPolicy(Qt.NoFocus)))
        self.delete_btn.clicked.connect(lambda: (self.delete_student(), self.delete_btn.setFocusPolicy(Qt.NoFocus)))
        self.save_btn.clicked.connect(lambda: (self.save_student_data(), self.save_btn.setFocusPolicy(Qt.NoFocus)))
        self.action_cancel_btn.clicked.connect(lambda: (self.handle_cancel_or_back(), self.action_cancel_btn.setFocusPolicy(Qt.NoFocus)))

        self.required_fields = ["scholar_id", "name"]

    def set_student(self, student: Student = None, mode='view'):

        self.student = student
        self.current_mode = mode

        if self.current_mode != 'add':
            self.original_student_data = student
            if student:
                self._populate_fields(student)
            else:
                self.clear_fields()
        else:
            self.original_student_data = None
            self.clear_fields()

        if self.current_mode == 'view':
            self.set_view_mode()
        elif self.current_mode == 'edit':
            self.set_edit_mode()
        elif self.current_mode == 'add':
            self.set_add_mode()
        
    def _populate_fields(self, student: Student):
        self.clear_fields()

        for key, widget in self.fields.items():
            value = getattr(student, key, None)
            
            if key == "class_name" and hasattr(student, 'class_name'):
                value = student.class_name
            
            if isinstance(widget, QLineEdit):
                widget.setText(str(value) if value is not None else "")
            elif isinstance(widget, QTextEdit):
                widget.setPlainText(str(value) if value is not None else "")
            elif isinstance(widget, QComboBox):
                idx = widget.findText(str(value))
                if idx >= 0:
                    widget.setCurrentIndex(idx)
                else:
                    widget.setCurrentIndex(0)
            elif isinstance(widget, QDateEdit):
                if isinstance(value, datetime.date):
                    widget.setDate(QDate(value.year, value.month, value.day))
                elif isinstance(value, QDate):
                    widget.setDate(value)
                elif isinstance(value, (str, bytes)):
                    date_str = value.decode('utf-8') if isinstance(value, bytes) else value
                    qdate = QDate.fromString(date_str, "yyyy-MM-dd")
                    if qdate.isValid():
                        widget.setDate(qdate)
                    else:
                        widget.setDate(QDate.currentDate())
                else:
                    widget.setDate(QDate.currentDate())
            elif isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
    
    def clear_fields(self):
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)

    def set_view_mode(self):
        self.current_mode = 'view'
        
        window_title = "Student Details"
        if self.student and self.student.name:
            window_title = f"Student Details: {self.student.name}"
        self.parent().setWindowTitle(window_title)

        for key, widget in self.fields.items():
            if key == "scholar_id":
                widget.setReadOnly(True)
                widget.setProperty("readOnly", True) # for CSS
            elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(True)
                widget.setProperty("readOnly", True)
            elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setEnabled(False)
        
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit) or isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setStyleSheet(self.input_field_style + self.read_only_field_style)


        self.action_cancel_btn.setText("Back")
        self.action_cancel_btn.setVisible(True)
        self.edit_btn.setVisible(True)
        self.delete_btn.setVisible(True)
        self.save_btn.setVisible(False)

    def set_edit_mode(self):
        self.current_mode = 'edit'
        
        window_title = "Edit Student"
        if self.student and self.student.name:
            window_title = f"Edit Student: {self.student.name}"
        self.parent().setWindowTitle(window_title)

        for key, widget in self.fields.items():
            if key == "scholar_id":
                 widget.setReadOnly(True)
                 widget.setProperty("readOnly", True)
            elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(False)
                widget.setProperty("readOnly", False)
            elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setEnabled(True)
        
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit) or isinstance(widget, QComboBox) or isinstance(widget, QDateEdit):
                widget.setStyleSheet(self.input_field_style)
            elif isinstance(widget, QCheckBox):
                widget.setStyleSheet("QCheckBox { color: #333333; }")

        self.action_cancel_btn.setText("Cancel")
        self.action_cancel_btn.setVisible(True)
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)
        self.save_btn.setVisible(True)

    def set_add_mode(self):
        self.current_mode = 'add'
        self.parent().setWindowTitle("Add New Student")
        
        self.clear_fields()
        
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.setReadOnly(False)
                widget.setProperty("readOnly", False)
            elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
                widget.setEnabled(True)
            if isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
        
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit) or isinstance(widget, QComboBox) or isinstance(widget, QDateEdit):
                widget.setStyleSheet(self.input_field_style)
            elif isinstance(widget, QCheckBox):
                widget.setStyleSheet("QCheckBox { color: #333333; }")

        self.fields["scholar_id"].setReadOnly(False)
        self.fields["scholar_id"].setProperty("readOnly", False)
        self.fields["scholar_id"].setPlaceholderText("Enter Scholar ID (optional, leave blank for auto-generate)")


        self.action_cancel_btn.setText("Cancel")
        self.action_cancel_btn.setVisible(True)
        self.edit_btn.setVisible(False)
        self.delete_btn.setVisible(False)
        self.save_btn.setVisible(True)

    def get_data_from_fields(self) -> Student:
        data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                text = widget.text().strip()
                if key in ["scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"]:
                    try:
                        data[key] = int(text) if text else None
                    except ValueError:
                        QMessageBox.warning(self, "Invalid Input", f"{key.replace('_', ' ').title()} must be a valid number.")
                        return None
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
        
        if 'class_name' in data and data['class_name'] == "None":
            data['class_name'] = None
            
        if not data.get("name"):
            QMessageBox.warning(self, "Validation", "Student Name cannot be empty.")
            return None

        return Student(**data)

    def validate_input(self, student_data: Student) -> list:
        errors = []
        
        if self.current_mode == 'add' and student_data.scholar_id is not None:
            if not isinstance(student_data.scholar_id, int):
                errors.append("Scholar ID must be a number if provided.")
            elif self.student_db_manager.get_student_by_id(student_data.scholar_id):
                errors.append(f"Scholar ID {student_data.scholar_id} already exists. Please choose a unique one or leave blank for auto-generation.")

        if not student_data.name:
            errors.append("Name is required.")
        
        if not student_data.class_name:
            errors.append("Class is required.")

        if not student_data.contact:
            errors.append("Contact Number is required.")
        elif not isinstance(student_data.contact, int) or len(str(student_data.contact)) < 10:
             errors.append("Contact Number must be a valid 10-digit number.")
        
        if student_data.email and "@" not in student_data.email:
            errors.append("Email must be a valid email address.")

        return errors

    def save_student_data(self):
        new_student = self.get_data_from_fields()
        if new_student is None:
            return

        validation_errors = self.validate_input(new_student)

        if validation_errors:
            QMessageBox.warning(self, "Validation Error", f"Please correct the following issues:\n- " + "\n- ".join(validation_errors))
            return

        try:
            if self.current_mode == 'add':
                self.student_db_manager.add_student(new_student)
                QMessageBox.information(self, "Success", "Student added successfully.")
                self.student_saved.emit()
                self.back_to_list.emit()
            elif self.current_mode == 'edit':
                new_student.scholar_id = self.student.scholar_id if self.student else None
                if new_student.scholar_id is None:
                    QMessageBox.critical(self, "Error", "Student ID missing for update operation.")
                    return

                self.student_db_manager.update_student(new_student)
                QMessageBox.information(self, "Success", f"Student {new_student.name} updated successfully.")
                self.student_saved.emit()
                self.set_student(new_student, mode='view') 

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

    def handle_cancel_or_back(self):
        """Unified handler for 'Cancel' (add/edit mode) or 'Back to List' (view mode)."""
        if self.current_mode == 'add':
            reply = QMessageBox.question(self, "Confirm Cancel",
                                         "Are you sure you want to cancel adding this student? Any unsaved data will be lost.",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.back_to_list.emit()
        elif self.current_mode == 'edit':
            reply = QMessageBox.question(self, "Confirm Cancel", "Discard changes?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.set_student(self.original_student_data, mode='view')
            else:
                self.back_to_list.emit()
        elif self.current_mode == 'view':
            self.back_to_list.emit()