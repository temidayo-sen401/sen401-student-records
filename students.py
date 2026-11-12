"""Student data module.

Holds the in-memory list of students and basic operations on it.
"""

students = [
    {"name": "James", "score": 45},
    {"name": "Deborah", "score": 82},
    {"name": "Aisha", "score": 67},
    {"name": "Chinedu", "score": 91},
    {"name": "Tunde", "score": 58},
]


def average_score(data):
    if len(data) == 0:
        return 0  # Preventive maintenance: avoid division by zero
    total = 0
    for d in data:
        total += d["score"]
    return total / len(data)


def add_student(name, score):
    # Corrective fix: reject non-numeric or out-of-range scores so they
    # cannot break average_score() later with a TypeError.
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ValueError(f"score must be a number, got {score!r}")
    if not 0 <= score <= 100:
        raise ValueError(f"score must be between 0 and 100, got {score}")
    students.append({"name": name, "score": score})


# Corrective fix: only print when run directly, not on import.
if __name__ == "__main__":
    print("Current Students:", students)
    print("Average Score:", average_score(students))
