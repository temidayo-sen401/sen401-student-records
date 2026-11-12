# Lab 4 — Reverse Engineering Notes

**Subject systems:**
- Student Records v1.1 (`sen401-student-records`, Labs 1–2)
- Inventory v1.0 (`sen401-inventory-csa`, Lab 3)

**Method:** Static analysis with `tools/analyze.py`, which parses every module with
Python's `ast` module and reports classes, functions, docstrings, project
imports, module-level side effects and use of global state. Its output was then
checked by reading the code by hand.

```bash
python3.12 tools/analyze.py . ../sen401-inventory-csa
```

## 1. Inventory of functions and classes

### Student Records v1.1

| Module | Element | Kind | Responsibility |
|--------|---------|------|----------------|
| `app` | `print_table` | function | Presentation: ranked table of students |
| `app` | `print_summary` | function | Presentation: statistics summary |
| `app` | `main` | function | Entry point; also **adds a student** (business action) |
| `students` | `Student` | class (Pydantic) | Validation model |
| `students` | `StudentRecord` | type alias | `dict[str, str \| float]` |
| `students` | `default_students` | function | Hard-coded sample data |
| `students` | `students` | module variable | Shared mutable in-memory list |
| `students` | `average_score` | function | Statistic |
| `students` | `add_student` | function | Validate and append (writes to the global list by default) |
| `utils.helpers` | `highest_score`, `lowest_score`, `pass_rate`, `median_score`, `grade`, `score_summary` | functions | Statistics |

### Inventory v1.0

| Module | Element | Kind | Responsibility |
|--------|---------|------|----------------|
| `app` | `print_stock_table`, `print_stock_levels`, `main` | functions | Presentation and entry point |
| `inventory` | `InventoryItem` | type alias | `dict[str, str \| int \| float]` |
| `inventory` | `inventory` | module variable | Hard-coded in-memory list |
| `inventory` | `export_to_csv` | function | File input/output |
| `utils.helpers` | `item_value`, `total_stock_value`, `highest_stock_item`, `lowest_stock_item`, `low_stock_items` | functions | Calculations |

## 2. Module dependency diagrams (current state)

```mermaid
graph TD
    subgraph "Student Records v1.1"
        SA["app.py<br/>(presentation + entry)"] -->|students, add_student| SS["students.py<br/>(model + data + logic)"]
        SA -->|grade, highest_score,<br/>lowest_score, score_summary| SH["utils/helpers.py<br/>(statistics)"]
        SH -->|StudentRecord| SS
        SS -->|BaseModel, Field| PYD(["pydantic"])
        SH --> STAT(["statistics"])
    end
    subgraph "Inventory v1.0"
        IA["app.py<br/>(presentation + entry)"] -->|inventory, export_to_csv,<br/>InventoryItem| II["inventory.py<br/>(data + types + CSV I/O)"]
        IA -->|item_value, total_stock_value,<br/>highest/lowest, low_stock| IH["utils/helpers.py<br/>(calculations)"]
        IH -->|InventoryItem| II
        II --> CSV(["csv, pathlib"])
    end
```

## 3. UML class diagram (current state)

```mermaid
classDiagram
    class Student {
        <<pydantic BaseModel>>
        +str name
        +float score  [0..100, strict]
    }
    class students_module {
        <<module>>
        +list~StudentRecord~ students
        +default_students() list
        +average_score(data) float
        +add_student(name, score, data) StudentRecord
    }
    class student_helpers {
        <<module utils.helpers>>
        +highest_score(data)
        +lowest_score(data)
        +pass_rate(data, pass_mark)
        +median_score(data)
        +grade(score) str
        +score_summary(data) dict
    }
    class inventory_module {
        <<module>>
        +list~InventoryItem~ inventory
        +export_to_csv(items, path) Path
    }
    class inventory_helpers {
        <<module utils.helpers>>
        +item_value(item)
        +total_stock_value(items)
        +highest_stock_item(items)
        +lowest_stock_item(items)
        +low_stock_items(items, threshold)
    }
    students_module ..> Student : validates with
    student_helpers ..> students_module : imports StudentRecord
    inventory_helpers ..> inventory_module : imports InventoryItem
```

## 4. Coupling and code smells found

| # | Finding | Where | Impact | Planned refactoring |
|---|---------|-------|--------|---------------------|
| 1 | **Utility layer depends on the data layer:** `utils.helpers` imports its type from `students` / `inventory` | both apps | Helpers can't be reused without the data module; dependencies point the wrong way | Move the types into `models.py`; helpers depend only on models |
| 2 | **Mixed responsibilities:** `students.py` holds the model, data and logic; `inventory.py` holds the data, types and CSV I/O | both apps | Changing storage means editing business code | Separate `models`, `repository` (storage) and `services` (logic) |
| 3 | **Duplicated logic (DRY):** `highest_score`/`highest_stock_item` and `lowest_score`/`lowest_stock_item` are the same algorithm on different keys | across apps | Same fix needed in two places | One generic `highest_by(items, key)` / `lowest_by(items, key)` in `utils.py` |
| 4 | **Shared mutable global state:** `students` list is changed by `add_student` | `students.py` | Hidden coupling; state lost on exit; not safe with multiple users | Persist in SQLite and access through a repository |
| 5 | **Hard-coded data:** sample lists in source code | both apps | Changing data needs a code change and a release | Migrate data to SQLite (`scripts/migrate.py`) |
| 6 | **Presentation mixed with business actions:** `main()` adds a student while printing a report | student `app.py` | The report has a side effect | Expose actions as REST endpoints; the report becomes a separate client |
| 7 | **Untyped records:** records are plain `dict`s with string keys | both apps | Typos in keys only fail at runtime; no editor support | Pydantic models for input and output |
| 8 | **No external interface:** console only | both apps | Can't be used by other systems | FastAPI REST API with OpenAPI docs |

## 5. Target architecture (after re-engineering)

```mermaid
graph TD
    CLIENT["report service<br/>client/report.py"] -->|HTTP JSON| MAIN
    subgraph "api service (FastAPI)"
        MAIN["app/main.py<br/>(FastAPI app)"] --> CS["controllers/students.py"]
        MAIN --> CI["controllers/inventory.py"]
        CS --> SVC["services.py<br/>(business rules)"]
        CI --> SVC
        CS --> REPO["repository.py<br/>(SQL data access)"]
        CI --> REPO
        SVC --> UT["utils.py<br/>(generic helpers)"]
        SVC --> MOD["models.py<br/>(Pydantic schemas)"]
        CS --> MOD
        CI --> MOD
        REPO --> MOD
        REPO --> DBM["database.py<br/>(connection, schema)"]
    end
    DBM --> DB[("SQLite<br/>school_ops.db<br/>(Docker volume)")]
    MIG["migrate service<br/>scripts/migrate.py"] -->|reads| SRC["data/students.json<br/>data/inventory.csv"]
    MIG -->|writes| DB
```

The dependencies now point one way: controllers → services/repository → models/database.
`utils.py` and `models.py` depend on nothing else in the project.
