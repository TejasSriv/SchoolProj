from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QComboBox, QTextEdit, QDateEdit, QCheckBox, QScrollArea, QWidget
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QDate, QRegExp

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.setWindowTitle("Student Details")
        self.setFixedWidth(400)
        self.setFixedHeight(500)  # Reduce dialog height

        # Main layout for dialog
        dialog_layout = QVBoxLayout(self)

        # Scroll area setup
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        int_fields = [
            "scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"
        ]

        self.fields = {
            "scholar_id": QLineEdit(),
            "apaar_id": QLineEdit(),
            "permanent_enrollment_number": QLineEdit(),
            "name": QLineEdit(),
            "class": QLineEdit(),
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
                label = QLabel(key.replace("_", " ").title() + ":")
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
        self.save_btn.clicked.connect(self.validate_and_accept)  # Use validation

        if student:
            for key, widget in self.fields.items():
                value = student.get(key, "")
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QTextEdit):
                    widget.setPlainText(str(value))
                elif isinstance(widget, QComboBox):
                    idx = widget.findText(str(value))
                    widget.setCurrentIndex(idx if idx >= 0 else 0)
                elif isinstance(widget, QDateEdit):
                    if value:
                        widget.setDate(QDate.fromString(str(value), "yyyy-MM-dd"))
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
            self.fields["scholar_id"].setReadOnly(True)

        # List of required fields (update as per your schema)
        self.required_fields = [
            "scholar_id", "name"
        ]

    def get_data(self):
        data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                text = widget.text()
                if key in ["scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"]:
                    data[key] = int(text) if text else None
                else:
                    data[key] = text
            elif isinstance(widget, QTextEdit):
                data[key] = widget.toPlainText()
            elif isinstance(widget, QComboBox):
                data[key] = widget.currentText()
            elif isinstance(widget, QDateEdit):
                data[key] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QCheckBox):
                data[key] = widget.isChecked()
        return data

    def validate_and_accept(self):
        missing = []
        for key in self.required_fields:
            widget = self.fields[key]
            if isinstance(widget, QLineEdit) and not widget.text().strip():
                missing.append(key.replace("_", " ").title())
            elif isinstance(widget, QTextEdit) and not widget.toPlainText().strip():
                missing.append(key.replace("_", " ").title())
            elif isinstance(widget, QComboBox) and not widget.currentText().strip():
                missing.append(key.replace("_", " ").title())
        if missing:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Missing Fields", f"Please fill in the following required fields:\n- " + "\n- ".join(missing))
            return
        self.accept()