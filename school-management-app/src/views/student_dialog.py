from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QComboBox, QTextEdit, QDateEdit, QCheckBox, QScrollArea, QWidget,
    QMessageBox
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QDate, QRegExp, Qt
from models.student import Student

class StudentDialog(QDialog):
    def __init__(self, parent=None, student: Student = None):
        super().__init__(parent)
        self.setWindowTitle("Student Details")
        self.setFixedWidth(450)
        self.setFixedHeight(550)

        dialog_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setAlignment(Qt.AlignTop)

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
                layout.addWidget(widget)
            else:
                label_text = key.replace("_", " ").title()
                if key == "class_name":
                    label_text = "Class:"
                label = QLabel(label_text)
                layout.addWidget(label)
                layout.addWidget(widget)

        scroll_content.setLayout(layout)
        scroll.setWidget(scroll_content)
        dialog_layout.addWidget(scroll)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        dialog_layout.addLayout(btn_layout)
        self.setLayout(dialog_layout)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.validate_and_accept)

        if student:
            self.setWindowTitle("Edit Student Details")
            for key, widget in self.fields.items():
                
                if key == 'class_name':
                    value = getattr(student, 'class_name', None) or getattr(student, 'class', None)
                else:
                    value = getattr(student, key, None)
                
                if value is None:
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
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))

            self.fields["scholar_id"].setReadOnly(True)
        
        self.required_fields = [
            "scholar_id", "name"
        ]

    def get_data(self) -> Student:

        data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                text = widget.text().strip()
                if key in ["scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"]:
                    data[key] = int(text) if text else None
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
        
        if 'class_name' in data:
            data['class_name'] = data['class_name'] # Already correctly named
        
        return Student(**data)

    def validate_and_accept(self):
        missing = []
        data = self.get_data().to_dict()

        validation_map = {
            "scholar_id": "Scholar ID",
            "name": "Name",
            "class_name": "Class"
        }

        for key in self.required_fields:
            value = data.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                display_name = validation_map.get(key, key.replace("_", " ").title())
                missing.append(display_name)
        
        if missing:
            QMessageBox.warning(self, "Missing Fields", f"Please fill in the following required fields:\n- " + "\n- ".join(missing))
            return
        
        self.accept()