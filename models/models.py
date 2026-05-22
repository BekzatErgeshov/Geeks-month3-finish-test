from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


enrollment = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    phone = Column(String(50), nullable=False)

    courses = relationship("Course", secondary=enrollment, back_populates="students")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    teacher = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)

    students = relationship("Student", secondary=enrollment, back_populates="courses")
