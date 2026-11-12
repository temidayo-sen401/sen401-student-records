"""Report client: prints the student and inventory reports by calling the REST API.

It runs as its own container and talks to the ``api`` service over the
Docker network, so it shows that the services communicate correctly.
It uses only the Python standard library.

Usage:  API_URL=http://localhost:8000 python3.12 client/report.py
"""

import json
import os
import time
import urllib.error
import urllib.request

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
WIDTH = 62


def get(path: str):
    """GET ``API_URL + path`` and return the decoded JSON body."""
    with urllib.request.urlopen(f"{API_URL}{path}", timeout=5) as resp:
        return json.load(resp)


def wait_for_api(retries: int = 10, delay: float = 1.0) -> None:
    """Retry /health until the API is up, so start-up order is not a problem."""
    for attempt in range(1, retries + 1):
        try:
            health = get("/health")
            print(f"Connected to {API_URL} (status: {health['status']})\n")
            return
        except (urllib.error.URLError, ConnectionError):
            print(f"Waiting for API at {API_URL} (attempt {attempt}/{retries})...")
            time.sleep(delay)
    raise SystemExit(f"API at {API_URL} is not reachable")


def heading(title: str) -> None:
    """Print a section heading."""
    print("=" * WIDTH)
    print(title.center(WIDTH))
    print("=" * WIDTH)


def print_students() -> None:
    """Print the ranked student table (GET /students/{id}) and stats (GET /students/stats)."""
    heading("STUDENT RECORDS REPORT")
    students = [get(f"/students/{s['id']}") for s in get("/students")]
    print(f"{'#':<4}{'Name':<14}{'Score':>8}{'Grade':>8}")
    for rank, s in enumerate(sorted(students, key=lambda s: s["score"], reverse=True), 1):
        print(f"{rank:<4}{s['name']:<14}{s['score']:>8.1f}{s['grade']:>8}")
    st = get("/students/stats")
    print(f"\nMean {st['mean']:.2f} | Median {st['median']:.2f} | "
          f"Std dev {st['stdev']:.2f} | Pass rate {st['pass_rate']:.1f}%")
    if st["highest"] and st["lowest"]:
        print(f"Highest: {st['highest']['name']} ({st['highest']['score']:.0f})   "
              f"Lowest: {st['lowest']['name']} ({st['lowest']['score']:.0f})")


def print_inventory() -> None:
    """Print the stock table (GET /inventory) and stats (GET /inventory/stats)."""
    heading("INVENTORY STOCK REPORT")
    print(f"{'Item':<18}{'Qty':>6}{'Unit Price (N)':>17}{'Value (N)':>21}")
    for i in get("/inventory"):
        value = i["quantity"] * i["price"]
        print(f"{i['item_name']:<18}{i['quantity']:>6}{i['price']:>17,.2f}{value:>21,.2f}")
    st = get("/inventory/stats")
    print(f"{'TOTAL STOCK VALUE':<41}{st['total_value']:>21,.2f}")
    for i in st["low_stock"]:
        print(f"LOW STOCK ALERT: {i['item_name']} has only {i['quantity']} left - reorder")


def main() -> None:
    wait_for_api()
    print_students()
    print()
    print_inventory()


if __name__ == "__main__":
    main()
