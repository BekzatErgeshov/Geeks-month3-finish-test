from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QLabel,
)
from PyQt6.QtCore import Qt
from sqlalchemy.orm import Session

from logic import student_logic, course_logic
from ui.student_form import StudentForm
from ui.course_form import CourseForm
from ui.enrollment_window import EnrollmentWindow


class MainWindow(QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session
        self.setWindowTitle("Student Course Manager")
        self.setMinimumSize(900, 600)
        self._build_ui()
        self._load_students()
        self._load_courses()

    def _build_ui(self) -> None:
        tabs = QTabWidget()
        tabs.addTab(self._build_students_tab(), "Студенты")
        tabs.addTab(self._build_courses_tab(), "Курсы")

        btn_enrollments = QPushButton("Записи на курсы")
        btn_enrollments.clicked.connect(self._open_enrollments)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(tabs)
        layout.addWidget(btn_enrollments)
        self.setCentralWidget(central)

    # ------------------------------------------------------------------ students
    def _build_students_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # search bar
        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Поиск:"))
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Введите имя...")
        self.student_search.textChanged.connect(self._search_students)
        search_row.addWidget(self.student_search)
        layout.addLayout(search_row)

        # table
        self.students_table = self._make_table(["ID", "ФИО", "Возраст", "Email", "Телефон"])
        layout.addWidget(self.students_table)

        # buttons
        btn_row = QHBoxLayout()
        for label, slot in [
            ("Добавить", self._add_student),
            ("Изменить", self._edit_student),
            ("Удалить", self._delete_student),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)
        layout.addLayout(btn_row)
        return widget

    def _load_students(self, query: str = "") -> None:
        if query:
            students = student_logic.search_students(self._session, query)
        else:
            students = student_logic.get_all_students(self._session)
        self.students_table.setRowCount(0)
        for s in students:
            row = self.students_table.rowCount()
            self.students_table.insertRow(row)
            self.students_table.setItem(row, 0, QTableWidgetItem(str(s.id)))
            self.students_table.setItem(row, 1, QTableWidgetItem(s.full_name))
            self.students_table.setItem(row, 2, QTableWidgetItem(str(s.age)))
            self.students_table.setItem(row, 3, QTableWidgetItem(s.email))
            self.students_table.setItem(row, 4, QTableWidgetItem(s.phone))

    def _search_students(self, text: str) -> None:
        self._load_students(text)

    def _selected_student_id(self) -> int | None:
        row = self.students_table.currentRow()
        if row < 0:
            return None
        return int(self.students_table.item(row, 0).text())

    def _add_student(self) -> None:
        dlg = StudentForm(self)
        if dlg.exec() != StudentForm.DialogCode.Accepted:
            return
        data = dlg.get_data()
        try:
            student_logic.create_student(self._session, **data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать студента:\n{e}")
            return
        self._load_students(self.student_search.text())

    def _edit_student(self) -> None:
        sid = self._selected_student_id()
        if sid is None:
            QMessageBox.information(self, "Выбор", "Выберите студента в таблице.")
            return
        student = student_logic.get_student(self._session, sid)
        dlg = StudentForm(self, student)
        if dlg.exec() != StudentForm.DialogCode.Accepted:
            return
        data = dlg.get_data()
        try:
            student_logic.update_student(self._session, sid, **data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить студента:\n{e}")
            return
        self._load_students(self.student_search.text())

    def _delete_student(self) -> None:
        sid = self._selected_student_id()
        if sid is None:
            QMessageBox.information(self, "Выбор", "Выберите студента в таблице.")
            return
        reply = QMessageBox.question(
            self, "Удаление", "Удалить выбранного студента?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        student_logic.delete_student(self._session, sid)
        self._load_students(self.student_search.text())

    # ------------------------------------------------------------------ courses
    def _build_courses_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Поиск:"))
        self.course_search = QLineEdit()
        self.course_search.setPlaceholderText("Введите название...")
        self.course_search.textChanged.connect(self._search_courses)
        search_row.addWidget(self.course_search)
        layout.addLayout(search_row)

        self.courses_table = self._make_table(["ID", "Название", "Преподаватель", "Длительность (ч.)"])
        layout.addWidget(self.courses_table)

        btn_row = QHBoxLayout()
        for label, slot in [
            ("Добавить", self._add_course),
            ("Изменить", self._edit_course),
            ("Удалить", self._delete_course),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)
        layout.addLayout(btn_row)
        return widget

    def _load_courses(self, query: str = "") -> None:
        if query:
            courses = course_logic.search_courses(self._session, query)
        else:
            courses = course_logic.get_all_courses(self._session)
        self.courses_table.setRowCount(0)
        for c in courses:
            row = self.courses_table.rowCount()
            self.courses_table.insertRow(row)
            self.courses_table.setItem(row, 0, QTableWidgetItem(str(c.id)))
            self.courses_table.setItem(row, 1, QTableWidgetItem(c.title))
            self.courses_table.setItem(row, 2, QTableWidgetItem(c.teacher))
            self.courses_table.setItem(row, 3, QTableWidgetItem(str(c.duration)))

    def _search_courses(self, text: str) -> None:
        self._load_courses(text)

    def _selected_course_id(self) -> int | None:
        row = self.courses_table.currentRow()
        if row < 0:
            return None
        return int(self.courses_table.item(row, 0).text())

    def _add_course(self) -> None:
        dlg = CourseForm(self)
        if dlg.exec() != CourseForm.DialogCode.Accepted:
            return
        data = dlg.get_data()
        try:
            course_logic.create_course(self._session, **data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать курс:\n{e}")
            return
        self._load_courses(self.course_search.text())

    def _edit_course(self) -> None:
        cid = self._selected_course_id()
        if cid is None:
            QMessageBox.information(self, "Выбор", "Выберите курс в таблице.")
            return
        course = course_logic.get_course(self._session, cid)
        dlg = CourseForm(self, course)
        if dlg.exec() != CourseForm.DialogCode.Accepted:
            return
        data = dlg.get_data()
        try:
            course_logic.update_course(self._session, cid, **data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить курс:\n{e}")
            return
        self._load_courses(self.course_search.text())

    def _delete_course(self) -> None:
        cid = self._selected_course_id()
        if cid is None:
            QMessageBox.information(self, "Выбор", "Выберите курс в таблице.")
            return
        reply = QMessageBox.question(
            self, "Удаление", "Удалить выбранный курс?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        course_logic.delete_course(self._session, cid)
        self._load_courses(self.course_search.text())

    # ------------------------------------------------------------------ enrollments
    def _open_enrollments(self) -> None:
        dlg = EnrollmentWindow(self._session, self)
        dlg.exec()

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _make_table(headers: list[str]) -> QTableWidget:
        t = QTableWidget(0, len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return t
