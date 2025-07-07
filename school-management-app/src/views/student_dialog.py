from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QComboBox, QTextEdit
from PyQt5.QtGui import QIntValidator

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.setWindowTitle("Student Details")
        self.setFixedWidth(400)
        layout = QVBoxLayout()

        # Fields that must be integers
        int_fields = [
            "scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"
        ]

        self.fields = {
            "scholar_id": QLineEdit(),
            "apaar_id": QLineEdit(),
            "permanent_enrollment_number": QLineEdit(),
            "name": QLineEdit(),
            "class": QLineEdit(),
            "dob": QLineEdit(),
            "gender": QComboBox(),
            "social_category": QLineEdit(),
            "father": QLineEdit(),
            "mother": QLineEdit(),
            "last_school": QLineEdit(),
            "tc_number": QLineEdit(),
            "address": QTextEdit(),
            "city": QLineEdit(),
            "state": QLineEdit(),
            "contact": QLineEdit(),
            "alternate_contact": QLineEdit(),
            "email": QLineEdit(),
            "aadhaar": QLineEdit(),
            "birth_certificate": QLineEdit()
        }

        self.fields["gender"].addItems(["Male", "Female", "Other"])

        # Set integer validators
        int_validator = QIntValidator(0, 9223372036854775807, self)
        for key in int_fields:
            self.fields[key].setValidator(int_validator)

        for key, widget in self.fields.items():
            label = QLabel(key.replace("_", " ").title() + ":")
            layout.addWidget(label)
            layout.addWidget(widget)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)

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

    def get_data(self):
        data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                text = widget.text()
                # Convert to int if field is supposed to be int and not empty
                if key in ["scholar_id", "apaar_id", "permanent_enrollment_number", "tc_number", "contact", "alternate_contact"]:
                    data[key] = int(text) if text else None
                else:
                    data[key] = text
            elif isinstance(widget, QTextEdit):
                data[key] = widget.toPlainText()
            elif isinstance(widget, QComboBox):
                data[key] = widget.currentText()
        return data