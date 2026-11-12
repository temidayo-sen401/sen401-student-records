"""Student data module.

Defines the validated ``Student`` model, the default in-memory student list,
and pure functions that operate on any list of student records.

Design notes (preventive maintenance):
    * Functions take the data they work on as a parameter instead of
      silently reaching into module-level state, so they are easy to test
      and reuse with other data sources.
    * Validation rules live in one place (the ``Student`` model).
    * The module has no side effects on import.

Requires Python 3.12+ (uses the PEP 695 ``type`` statement).
"""

from pydantic import BaseModel, Field

MIN_SCORE = 0
MAX_SCORE = 100

# A student record as stored in the list: {"name": str, "score": float}
type StudentRecord = dict[str, str | float]


class Student(BaseModel):
    """A validated student record.

    Attributes:
        name: The student's name (must not be empty).
        score: The exam score, a number between MIN_SCORE and MAX_SCORE.
            ``strict=True`` rejects strings such as ``"90"``.
    """

    name: str = Field(min_length=1)
    score: float = Field(ge=MIN_SCORE, le=MAX_SCORE, strict=True)


def default_students() -> list[StudentRecord]:
    """Return a fresh copy of the sample student data."""
    return [
        {"name": "James", "score": 45},
        {"name": "Deborah", "score": 82},
        {"name": "Aisha", "score": 67},
        {"name": "Chinedu", "score": 91},
        {"name": "Tunde", "score": 58},
    ]


# Shared list used by the demo application.
students: list[StudentRecord] = default_students()


def average_score(data: list[StudentRecord]) -> float:
    """Return the mean score of ``data``, or 0.0 for an empty list.

    Args:
        data: List of student records.

    Returns:
        The arithmetic mean of all scores.
    """
    if not data:  # Guard against division by zero
        return 0.0
    return sum(s["score"] for s in data) / len(data)


def add_student(
    name: str, score: float, data: list[StudentRecord] | None = None
) -> StudentRecord:
    """Validate a new student and append it to ``data``.

    Args:
        name: The student's name.
        score: The student's score (0-100).
        data: The list to append to. Defaults to the shared ``students`` list.

    Returns:
        The validated record that was added.

    Raises:
        pydantic.ValidationError: If the name or score is invalid
            (a subclass of ``ValueError``).
    """
    target = students if data is None else data
    record = Student(name=name, score=score).model_dump()
    target.append(record)
    return record


if __name__ == "__main__":
    print("Current Students:", students)
    print("Average Score:", average_score(students))
