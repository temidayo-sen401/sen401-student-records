"""Regression tests for corrective maintenance (issue #3)."""

import pytest

from students import add_student
from utils.helpers import highest_score, lowest_score, pass_rate


def test_helpers_handle_empty_list():
    assert highest_score([]) is None
    assert lowest_score([]) is None
    assert pass_rate([]) == 0.0


@pytest.mark.parametrize("bad_score", ["90", None, -5, 101, True])
def test_add_student_rejects_invalid_score(bad_score):
    with pytest.raises(ValueError):
        add_student("Bola", bad_score)


def test_import_has_no_side_effects(capsys):
    import importlib

    import students

    importlib.reload(students)
    assert capsys.readouterr().out == ""
