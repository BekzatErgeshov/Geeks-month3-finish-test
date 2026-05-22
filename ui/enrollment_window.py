from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView,
)
from PyQt6.QtCore import Qt
from sqlalchemy.orm import Session
from logic import student_logic, course_logic


class EnrollmentWindow(QDialog):
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)
        self._session = session
        self.setWindowTitle("Запись студентов на курсы")
        self.setMinimumSize(700, 500)
        self._build_ui()
        self._refresh_combos()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        # -- enroll panel --
        enroll_layout = QHBoxLayout()
        enroll_layout.addWidget(QLabel("Студент:"))
        self.student_combo = QComboBox()
        self.student_combo.setMinimumWidth(220)
        enroll_layout.addWidget(self.student_combo)

        enroll_layout.addWidget(QLabel("Курс:"))
        self.course_combo = QComboBox()
        self.course_combo.setMinimumWidth(220)
        enroll_layout.addWidget(self.course_combo)

        btn_enroll = QPushButton("Записать")
        btn_enroll.clicked.connect(self._enroll)
        enroll_layout.addWidget(btn_enroll)
        root.addLayout(enroll_layout)

        # -- view panel --
        view_layout = QHBoxLayout()

        # left: students of a course
        left = QVBoxLayout()
        left.addWidget(QLabel("Студенты курса:"))
        self.course_filter = QComboBox()
        self.course_filter.currentIndexChanged.connect(self._load_students_of_course)
        left.addWidget(self.course_filter)
        self.students_table = self._make_table(["ID", "ФИО", "Email"])
        left.addWidget(self.students_table)
        btn_unenroll = QPushButton("Удалить запись")
        btn_unenroll.clicked.connect(self._unenroll_from_course)
        left.addWidget(btn_unenroll)
        view_layout.addLayout(left)

        # right: courses of a student
        right = QVBoxLayout()
        right.addWidget(QLabel("Курсы студента:"))
        self.student_filter = QComboBox()
        self.student_filter.currentIndexChanged.connect(self._load_courses_of_student)
        right.addWidget(self.student_filter)
        self.courses_table = self._make_table(["ID", "Название", "Преподаватель"])
        right.addWidget(self.courses_table)
        btn_unenroll2 = QPushButton("Удалить запись")
        btn_unenroll2.clicked.connect(self._unenroll_from_student)
        right.addWidget(btn_unenroll2)
        view_layout.addLayout(right)

        root.addLayout(view_layout)

    @staticmethod
    def _make_table(headers: list[str]) -> QTableWidget:
        t = QTableWidget(0, len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return t

    def _refresh_combos(self) -> None:
        students = student_logic.get_all_students(self._session)
        courses = course_logic.get_all_courses(self._session)

        for combo in (self.student_combo, self.student_filter):
            combo.clear()
            for s in students:
                combo.addItem(s.full_name, s.id)

        for combo in (self.course_combo, self.course_filter):
            combo.clear()
            for c in courses:
                combo.addItem(c.title, c.id)

        self._load_students_of_course()
        self._load_courses_of_student()

    def _enroll(self) -> None:
        student_id = self.student_combo.currentData()
        course_id = self.course_combo.currentData()
        if student_id is None or course_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите студента и курс.")
            return
        ok = course_logic.enroll_student(self._session, student_id, course_id)
        if not ok:
            QMessageBox.warning(self, "Ошибка", "Студент уже записан на этот курс.")
            return
        self._load_students_of_course()
        self._load_courses_of_student()

    def _load_students_of_course(self) -> None:
        course_id = self.course_filter.currentData()
        self.students_table.setRowCount(0)
        if course_id is None:
            return
        for s in course_logic.get_students_of_course(self._session, course_id):
            row = self.students_table.rowCount()
            self.students_table.insertRow(row)
            self.students_table.setItem(row, 0, QTableWidgetItem(str(s.id)))
            self.students_table.setItem(row, 1, QTableWidgetItem(s.full_name))
            self.students_table.setItem(row, 2, QTableWidgetItem(s.email))

    def _load_courses_of_student(self) -> None:
        student_id = self.student_filter.currentData()
        self.courses_table.setRowCount(0)
        if student_id is None:
            return
        for c in course_logic.get_courses_of_student(self._session, student_id):
            row = self.courses_table.rowCount()
            self.courses_table.insertRow(row)
            self.courses_table.setItem(row, 0, QTableWidgetItem(str(c.id)))
            self.courses_table.setItem(row, 1, QTableWidgetItem(c.title))
            self.courses_table.setItem(row, 2, QTableWidgetItem(c.teacher))

    def _unenroll_from_course(self) -> None:
        course_id = self.course_filter.currentData()
        row = self.students_table.currentRow()
        if row < 0 or course_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите студента в таблице.")
            return
        student_id = int(self.students_table.item(row, 0).text())
        course_logic.unenroll_student(self._session, student_id, course_id)
        self._load_students_of_course()
        self._load_courses_of_student()

    def _unenroll_from_student(self) -> None:
        student_id = self.student_filter.currentData()
        row = self.courses_table.currentRow()
        if row < 0 or student_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите курс в таблице.")
            return
        course_id = int(self.courses_table.item(row, 0).text())
        course_logic.unenroll_student(self._session, student_id, course_id)
        self._load_courses_of_student()
        self._load_students_of_course()
