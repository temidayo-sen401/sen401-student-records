"""Student Records demo application (entry point)."""

from students import students, add_student, average_score
from utils.helpers import highest_score, lowest_score, pass_rate


def main():
    print("=== Student Records Demo ===")

    add_student("Ngozi", 74)
    print("Added new student: Ngozi (74)")

    print("Total students:", len(students))
    print("Average score:", round(average_score(students), 2))

    top = highest_score(students)
    bottom = lowest_score(students)
    print("Highest score:", top["name"], "-", top["score"])
    print("Lowest score:", bottom["name"], "-", bottom["score"])
    print("Pass rate:", round(pass_rate(students), 1), "%")


if __name__ == "__main__":
    main()
