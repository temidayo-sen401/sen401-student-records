"""Student Records demo application (entry point)."""

from students import students, add_student
from utils.helpers import grade, highest_score, lowest_score, score_summary

LINE = "=" * 40


def print_table(data):
    """Print students as a formatted table, highest score first."""
    print(f"{'#':<3}{'Name':<12}{'Score':>7}{'Grade':>8}")
    print("-" * 30)
    ranked = sorted(data, key=lambda s: s["score"], reverse=True)
    for i, s in enumerate(ranked, start=1):
        print(f"{i:<3}{s['name']:<12}{s['score']:>7.1f}{grade(s['score']):>8}")


def print_summary(data):
    """Print summary statistics."""
    stats = score_summary(data)
    top, bottom = highest_score(data), lowest_score(data)
    print(f"{'Students':<16}: {stats['count']}")
    print(f"{'Mean score':<16}: {stats['mean']:.2f}")
    print(f"{'Median score':<16}: {stats['median']:.2f}")
    print(f"{'Std deviation':<16}: {stats['stdev']:.2f}")
    print(f"{'Highest':<16}: {top['name']} ({top['score']:.0f})")
    print(f"{'Lowest':<16}: {bottom['name']} ({bottom['score']:.0f})")
    print(f"{'Pass rate':<16}: {stats['pass_rate']:.1f}%")


def main():
    print(LINE)
    print("        STUDENT RECORDS REPORT")
    print(LINE)

    add_student("Ngozi", 74)
    print("Added new student: Ngozi (74)\n")

    print_table(students)
    print()
    print_summary(students)
    print(LINE)


if __name__ == "__main__":
    main()
