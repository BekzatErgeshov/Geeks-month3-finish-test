from sqlalchemy.orm import Session
from models.models import Student


def get_all_students(session: Session) -> list[Student]:
    return session.query(Student).order_by(Student.full_name).all()


def search_students(session: Session, name: str) -> list[Student]:
    return (
        session.query(Student)
        .filter(Student.full_name.ilike(f"%{name}%"))
        .order_by(Student.full_name)
        .all()
    )


def get_student(session: Session, student_id: int) -> Student | None:
    return session.get(Student, student_id)


def create_student(
    session: Session,
    full_name: str,
    age: int,
    email: str,
    phone: str,
) -> Student:
    student = Student(full_name=full_name, age=age, email=email, phone=phone)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def update_student(
    session: Session,
    student_id: int,
    full_name: str,
    age: int,
    email: str,
    phone: str,
) -> Student | None:
    student = session.get(Student, student_id)
    if student is None:
        return None
    student.full_name = full_name
    student.age = age
    student.email = email
    student.phone = phone
    session.commit()
    session.refresh(student)
    return student


def delete_student(session: Session, student_id: int) -> bool:
    student = session.get(Student, student_id)
    if student is None:
        return False
    session.delete(student)
    session.commit()
    return True
