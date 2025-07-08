# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout,
#     QComboBox, QTextEdit, QDateEdit, QCheckBox, QScrollArea, QWidget,
#     QMessageBox
# )
# from PyQt5.QtGui import QRegExpValidator
# from PyQt5.QtCore import QDate, QRegExp, Qt
# import mysql

# from models.student import Student
# from controllers.student_controller import StudentDBManager

# class StudentDetailsDialog(QDialog):
#     def __init__(self, parent=None, student: Student = None, mode='view'):
#         super().__init__(parent)
#         self.student = student
#         self.student_db_manager = StudentDBManager()
#         self.current_mode = mode

#         self.setWindowTitle("Student Details")
#         self.setFixedWidth(450)
#         self.setFixedHeight(550)

#         self.original_geometry = None

#         dialog_layout = QVBoxLayout(self)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll_content = QWidget()
#         layout = QVBoxLayout(scroll_content)
#         layout.setAlignment(Qt.AlignTop)

#         int_fields = [
#             "scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"
#         ]

#         self.fields = {
#             "scholar_id": QLineEdit(),
#             "apaar_id": QLineEdit(),
#             "permanent_enrollment_number": QLineEdit(),
#             "name": QLineEdit(),
#             "class_name": QLineEdit(),
#             "dob": QDateEdit(),
#             "gender": QComboBox(),
#             "social_category": QComboBox(),
#             "father": QLineEdit(),
#             "mother": QLineEdit(),
#             "last_school": QLineEdit(),
#             "tc_number": QLineEdit(),
#             "address": QTextEdit(),
#             "city": QLineEdit(),
#             "state": QLineEdit(),
#             "admission_date": QDateEdit(),
#             "contact": QLineEdit(),
#             "alternate_contact": QLineEdit(),
#             "email": QLineEdit(),
#             "aadhaar": QCheckBox("Has Aadhaar?"),
#             "birth_certificate": QCheckBox("Has Birth Certificate?")
#         }

#         self.fields["gender"].addItems(["Male", "Female", "Other"])
#         self.fields["social_category"].addItems(["General", "SC", "ST", "OBC", "Other"])
        
#         for key in ["dob", "admission_date"]:
#             self.fields[key].setCalendarPopup(True)
#             self.fields[key].setDisplayFormat("yyyy-MM-dd")
#             self.fields[key].setDate(QDate.currentDate())
        
#         digit_validator = QRegExpValidator(QRegExp(r'^\d{0,20}$'), self)
#         for key in int_fields:
#             self.fields[key].setValidator(digit_validator)
#             self.fields[key].setMaxLength(20)

#         for key, widget in self.fields.items():
#             if isinstance(widget, QCheckBox):
#                 layout.addWidget(widget)
#             else:
#                 label_text = key.replace("_", " ").title()
#                 if key == "class_name":
#                     label_text = "Class:"
#                 label = QLabel(label_text)
#                 layout.addWidget(label)
#                 layout.addWidget(widget)

#         scroll_content.setLayout(layout)
#         scroll.setWidget(scroll_content)
#         dialog_layout.addWidget(scroll)

#         # Buttons layout
#         self.btn_layout = QHBoxLayout()
#         self.edit_btn = QPushButton("Edit")
#         self.delete_btn = QPushButton("Delete")
#         self.save_btn = QPushButton("Save")
#         self.cancel_btn = QPushButton("Cancel")
#         self.close_btn = QPushButton("Close")

#         self.btn_layout.addWidget(self.edit_btn)
#         self.btn_layout.addWidget(self.delete_btn)
#         self.btn_layout.addStretch(1)
#         self.btn_layout.addWidget(self.save_btn)
#         self.btn_layout.addWidget(self.cancel_btn)
#         self.btn_layout.addWidget(self.close_btn)
#         dialog_layout.addLayout(self.btn_layout)
#         self.setLayout(dialog_layout)

#         self.edit_btn.clicked.connect(lambda: (self.set_edit_mode(), self.edit_btn.setFocusPolicy(Qt.NoFocus)))
#         self.delete_btn.clicked.connect(lambda: (self.delete_student(), self.delete_btn.setFocusPolicy(Qt.NoFocus)))
#         self.save_btn.clicked.connect(lambda: (self.validate_and_accept(), self.save_btn.setFocusPolicy(Qt.NoFocus)))
#         self.cancel_btn.clicked.connect(lambda: (self.set_view_mode(), self.cancel_btn.setFocusPolicy(Qt.NoFocus)))
#         self.close_btn.clicked.connect(lambda: (self.close(), self.close_btn.setFocusPolicy(Qt.NoFocus)))

#         self.required_fields = ["scholar_id", "name"]

#         if student:
#             self._populate_fields(student)
#             if mode == 'view':
#                 self.set_view_mode()
#             else:
#                 self.set_edit_mode()
#         else:
#             self.set_add_mode()
#             self.setWindowTitle("Add New Student")

#     def _populate_fields(self, student: Student):
#         for key, widget in self.fields.items():
#             value = getattr(student, key, None)
            
#             if value is None:
#                 continue

#             if isinstance(widget, QLineEdit):
#                 widget.setText(str(value))
#             elif isinstance(widget, QTextEdit):
#                 widget.setPlainText(str(value))
#             elif isinstance(widget, QComboBox):
#                 idx = widget.findText(str(value))
#                 if idx >= 0:
#                     widget.setCurrentIndex(idx)
#             elif isinstance(widget, QDateEdit):
#                 if isinstance(value, QDate):
#                     widget.setDate(value)
#                 elif isinstance(value, (str, bytes)):
#                     date_str = value.decode('utf-8') if isinstance(value, bytes) else value
#                     qdate = QDate.fromString(date_str, "yyyy-MM-dd")
#                     if qdate.isValid():
#                         widget.setDate(qdate)
#             elif isinstance(widget, QCheckBox):
#                 widget.setChecked(bool(value))

#     def set_view_mode(self):
#         self.current_mode = 'view'
#         self.setWindowTitle(f"Student Details: {self.student.name}" if self.student and self.student.name else "Student Details")
#         for key, widget in self.fields.items():
#             if key == "scholar_id":
#                 widget.setReadOnly(True)
#             elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
#                 widget.setReadOnly(True)
#             elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
#                 widget.setEnabled(False)
        
#         self.edit_btn.setVisible(True)
#         self.delete_btn.setVisible(True)
#         self.save_btn.setVisible(False)
#         self.cancel_btn.setVisible(False)
#         self.close_btn.setVisible(True)
#         self.adjustSize()

#     def set_edit_mode(self):
#         self.current_mode = 'edit'
#         self.setWindowTitle(f"Edit Student: {self.student.name}" if self.student and self.student.name else "Edit Student")
#         for key, widget in self.fields.items():
#             if key == "scholar_id":
#                  widget.setReadOnly(self.student is not None and self.student.scholar_id is not None)
#             elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
#                 widget.setReadOnly(False)
#             elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
#                 widget.setEnabled(True)
        
#         self.edit_btn.setVisible(False)
#         self.delete_btn.setVisible(False)
#         self.save_btn.setVisible(True)
#         self.cancel_btn.setVisible(True)
#         self.close_btn.setVisible(False)
#         self.adjustSize()

#     def set_add_mode(self):
#         self.current_mode = 'add'
#         self.setWindowTitle("Add New Student")
#         for key, widget in self.fields.items():
#             if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
#                 widget.setReadOnly(False)
#                 widget.clear()
#             elif isinstance(widget, QComboBox) or isinstance(widget, QDateEdit) or isinstance(widget, QCheckBox):
#                 widget.setEnabled(True)
#             if isinstance(widget, QDateEdit):
#                 widget.setDate(QDate.currentDate())
#             if isinstance(widget, QCheckBox):
#                 widget.setChecked(False)

#         self.fields["scholar_id"].setReadOnly(False)

#         self.edit_btn.setVisible(False)
#         self.delete_btn.setVisible(False)
#         self.save_btn.setVisible(True)
#         self.cancel_btn.setVisible(True)
#         self.close_btn.setVisible(False)
#         self.adjustSize()

#     def get_data(self) -> Student:
#         data = {}
#         for key, widget in self.fields.items():
#             if isinstance(widget, QLineEdit):
#                 text = widget.text().strip()
#                 if key in ["scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"]:
#                     data[key] = int(text) if text else None
#                 else:
#                     data[key] = text if text else None
#             elif isinstance(widget, QTextEdit):
#                 text = widget.toPlainText().strip()
#                 data[key] = text if text else None
#             elif isinstance(widget, QComboBox):
#                 data[key] = widget.currentText() if widget.currentText() else None
#             elif isinstance(widget, QDateEdit):
#                 data[key] = widget.date().toString("yyyy-MM-dd")
#             elif isinstance(widget, QCheckBox):
#                 data[key] = widget.isChecked()
        
#         return Student(**data)

#     def validate_and_accept(self):
#         missing = []
#         data = self.get_data().to_dict()
        
#         validation_map = {
#             "scholar_id": "Scholar ID",
#             "name": "Name",
#             "class_name": "Class"
#         }

#         for key in self.required_fields:
#             value = data.get(key)
#             if value is None or (isinstance(value, str) and not value.strip()):
#                 display_name = validation_map.get(key, key.replace("_", " ").title())
#                 missing.append(display_name)
        
#         if missing:
#             QMessageBox.warning(self, "Missing Fields", f"Please fill in the following required fields:\n- " + "\n- ".join(missing))
#             return
        
#         if self.current_mode == 'edit':
#             self.student = self.get_data()
#             self.accept()
#         elif self.current_mode == 'add':
#             self.accept()

#     def delete_student(self):
#         if not self.student or not self.student.scholar_id:
#             QMessageBox.critical(self, "Error", "No student selected for deletion.")
#             return

#         scholar_id_to_delete = self.student.scholar_id
#         student_name = self.student.name if self.student.name else "selected student"

#         reply = QMessageBox.question(self, "Confirm Delete",
#                                      f"Are you sure you want to delete student: {student_name} (ID: {scholar_id_to_delete})?\nThis action cannot be undone.",
#                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

#         if reply == QMessageBox.Yes:
#             try:
#                 self.student_db_manager.delete_student(scholar_id_to_delete)
#                 QMessageBox.information(self, "Success", f"Student {student_name} deleted successfully.")
#                 self.accept()
#             except mysql.connector.Error as err:
#                 QMessageBox.critical(self, "Database Error", f"Error deleting student: {err}")
#             except Exception as e:
#                 QMessageBox.critical(self, "Application Error", f"An unexpected error occurred during student deletion: {e}")