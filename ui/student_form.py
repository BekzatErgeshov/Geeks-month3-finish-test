from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QDialogButtonBox, QMessageBox,
)
from models.models import Student


class StudentForm(QDialog):
    def __init__(self, parent=None, student: Student | None = None):
        super().__init__(parent)
        self._student = student
        self.setWindowTitle("Редактировать студента" if student else "Добавить студента")
        self.setMinimumWidth(350)
        self._build_ui()
        if student:
            self._populate(student)

    def _build_ui(self) -> None:
        layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Иванов Иван Иванович")
        layout.addRow("ФИО:", self.name_edit)

        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 120)
        self.age_spin.setValue(18)
        layout.addRow("Возраст:", self.age_spin)

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("example@mail.com")
        layout.addRow("Email:", self.email_edit)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("+7 (999) 000-00-00")
        layout.addRow("Телефон:", self.phone_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _populate(self, student: Student) -> None:
        self.name_edit.setText(student.full_name)
        self.age_spin.setValue(student.age)
        self.email_edit.setText(student.email)
        self.phone_edit.setText(student.phone)

    def _validate_and_accept(self) -> None:
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "ФИО не может быть пустым.")
            return
        if not self.email_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Email не может быть пустым.")
            return
        if not self.phone_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Телефон не может быть пустым.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "full_name": self.name_edit.text().strip(),
            "age": self.age_spin.value(),
            "email": self.email_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
        }
