# Student Records

A small modular Python application for managing student scores, built for the
**SEN 401 Software Configuration Management & Maintenance** lab at MIVA Open University.

Author: Temidayo Omoyajowo (2025/B/SENG/0513)

**Requires Python 3.12+** (since v1.1).

## Project structure

```
sen401-student-records/
├── app.py                  # Entry point: runs the demo application
├── students.py             # Data module: Student model, sample data, average_score / add_student
├── utils/
│   ├── __init__.py
│   └── helpers.py          # highest/lowest score, pass rate, median, grade, score_summary
├── tests/                  # pytest suite (one file per maintenance type)
├── docs/release-notes/     # Release notes per baseline (v1.0, ...)
├── .github/
│   ├── workflows/ci.yml    # CI: tests + demo run on push / PR
│   └── pull_request_template.md
├── requirements.txt        # Python dependencies
└── pytest.ini              # Test configuration
```

| File | Purpose |
|------|---------|
| `app.py` | Imports the data and helpers, adds a student, and prints summary statistics. |
| `students.py` | Pydantic `Student` model, the sample student list, and functions to compute the average and add a validated student. |
| `utils/helpers.py` | Reusable utilities: highest/lowest score, pass rate, median, letter grade and a statistics summary. |
| `requirements.txt` | Dependencies to install with `pip`. |
| `tests/` | Automated tests run locally and in CI. |

## Usage

```bash
python3.12 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python app.py                    # run the demo
pytest -v                        # run the tests
```

## Branching model (SCM)

| Branch | Purpose |
|--------|---------|
| `main` | Protected. Release baselines only; changes arrive through a reviewed pull request. |
| `dev` | Integration branch for completed work. |
| `feature/*` | New features, branched from and merged back into `dev`. |
| `maint/*` | Maintenance (fixes, upgrades) against a released baseline. |
| `maintenance` | Lab 2 maintenance work (corrective, adaptive, perfective, preventive) leading to v1.1. |

Baselines are tagged (`v1.0`, `v1.1`, ...), and each has release notes in `docs/release-notes/`.
