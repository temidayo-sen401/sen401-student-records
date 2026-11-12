"""Student data module.

Holds the in-memory list of students and basic operations on it.
Requires Python 3.12+ (uses the PEP 695 ``type`` statement).
"""

from pydantic import BaseModel, Field

# Adaptive: Python 3.12 type alias syntax (PEP 695)
type StudentRecord = dict[str, str | float]


class Student(BaseModel):
    """Validated student record (Adaptive: Pydantic v2 data validation)."""

    name: str = Field(min_length=1)
    score: float = Field(ge=0, le=100, strict=True)


students: list[StudentRecord] = [
    {"name": "James", "score": 45},
    {"name": "Deborah", "score": 82},
    {"name": "Aisha", "score": 67},
    {"name": "Chinedu", "score": 91},
    {"name": "Tunde", "score": 58},
]


def average_score(data: list[StudentRecord]) -> float:
    if len(data) == 0:
        return 0  # Preventive maintenance: avoid division by zero
    total = 0
    for d in data:
        total += d["score"]
    return total / len(data)


def add_student(name: str, score: float) -> None:
    # Adaptive: Pydantic validates name and score (number, 0-100).
    # ValidationError is a subclass of ValueError.
    student = Student(name=name, score=score)
    students.append(student.model_dump())


# Corrective fix: only print when run directly, not on import.
if __name__ == "__main__":
    print("Current Students:", students)
    print("Average Score:", average_score(students))
