from sqlalchemy.orm import Session
from models.models import Course, Student


def get_all_courses(session: Session) -> list[Course]:
    return session.query(Course).order_by(Course.title).all()


def search_courses(session: Session, title: str) -> list[Course]:
    return (
        session.query(Course)
        .filter(Course.title.ilike(f"%{title}%"))
        .order_by(Course.title)
        .all()
    )


def get_course(session: Session, course_id: int) -> Course | None:
    return session.get(Course, course_id)


def create_course(
    session: Session,
    title: str,
    teacher: str,
    duration: int,
) -> Course:
    course = Course(title=title, teacher=teacher, duration=duration)
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def update_course(
    session: Session,
    course_id: int,
    title: str,
    teacher: str,
    duration: int,
) -> Course | None:
    course = session.get(Course, course_id)
    if course is None:
        return None
    course.title = title
    course.teacher = teacher
    course.duration = duration
    session.commit()
    session.refresh(course)
    return course


def delete_course(session: Session, course_id: int) -> bool:
    course = session.get(Course, course_id)
    if course is None:
        return False
    session.delete(course)
    session.commit()
    return True


def enroll_student(session: Session, student_id: int, course_id: int) -> bool:
    student = session.get(Student, student_id)
    course = session.get(Course, course_id)
    if student is None or course is None:
        return False
    if course in student.courses:
        return False
    student.courses.append(course)
    session.commit()
    return True


def unenroll_student(session: Session, student_id: int, course_id: int) -> bool:
    student = session.get(Student, student_id)
    course = session.get(Course, course_id)
    if student is None or course is None:
        return False
    if course not in student.courses:
        return False
    student.courses.remove(course)
    session.commit()
    return True


def get_students_of_course(session: Session, course_id: int) -> list[Student]:
    course = session.get(Course, course_id)
    if course is None:
        return []
    return course.students


def get_courses_of_student(session: Session, student_id: int) -> list[Course]:
    student = session.get(Student, student_id)
    if student is None:
        return []
    return student.courses
