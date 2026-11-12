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
    students.append({"name": name, "score": score})


print("Current Students:", students)
print("Average Score:", average_score(students))
