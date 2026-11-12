"""REST endpoints for students: /students."""

import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models import Student, StudentIn, StudentStats
from app.repository import StudentRepository
from app.services import grade, student_stats

router = APIRouter(prefix="/students", tags=["students"])


def get_repo(conn: Annotated[sqlite3.Connection, Depends(get_db)]) -> StudentRepository:
    return StudentRepository(conn)


Repo = Annotated[StudentRepository, Depends(get_repo)]


def _not_found(student_id: int) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"Student {student_id} not found")


@router.get("", response_model=list[Student])
def list_students(repo: Repo):
    """List all students."""
    return repo.list()


@router.get("/stats", response_model=StudentStats)
def get_student_stats(repo: Repo):
    """Mean, median, standard deviation, pass rate, highest and lowest."""
    return student_stats(repo.list())


@router.get("/{student_id}")
def get_student(student_id: int, repo: Repo) -> dict:
    """Get one student, including their letter grade."""
    student = repo.get(student_id)
    if student is None:
        raise _not_found(student_id)
    return {**student.model_dump(), "grade": grade(student.score)}


@router.post("", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentIn, repo: Repo):
    """Add a student. Invalid names or scores are rejected with 422."""
    return repo.add(data)


@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, data: StudentIn, repo: Repo):
    """Replace a student's name and score."""
    student = repo.update(student_id, data)
    if student is None:
        raise _not_found(student_id)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, repo: Repo) -> None:
    """Delete a student."""
    if not repo.delete(student_id):
        raise _not_found(student_id)
