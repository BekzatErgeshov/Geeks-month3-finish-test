from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QDialogButtonBox, QMessageBox,
)
from models.models import Course


class CourseForm(QDialog):
    def __init__(self, parent=None, course: Course | None = None):
        super().__init__(parent)
        self._course = course
        self.setWindowTitle("Редактировать курс" if course else "Добавить курс")
        self.setMinimumWidth(350)
        self._build_ui()
        if course:
            self._populate(course)

    def _build_ui(self) -> None:
        layout = QFormLayout(self)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Математический анализ")
        layout.addRow("Название:", self.title_edit)

        self.teacher_edit = QLineEdit()
        self.teacher_edit.setPlaceholderText("Петров П.П.")
        layout.addRow("Преподаватель:", self.teacher_edit)

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 9999)
        self.duration_spin.setValue(40)
        self.duration_spin.setSuffix(" ч.")
        layout.addRow("Длительность:", self.duration_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _populate(self, course: Course) -> None:
        self.title_edit.setText(course.title)
        self.teacher_edit.setText(course.teacher)
        self.duration_spin.setValue(course.duration)

    def _validate_and_accept(self) -> None:
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым.")
            return
        if not self.teacher_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Имя преподавателя не может быть пустым.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "title": self.title_edit.text().strip(),
            "teacher": self.teacher_edit.text().strip(),
            "duration": self.duration_spin.value(),
        }
