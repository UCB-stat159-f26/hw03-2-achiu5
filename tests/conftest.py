"""Shared pytest fixtures: the mock career JS files from the assignment."""

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def female_js() -> str:
    """Text of a three-match women's career file (opponent dates of birth)."""
    return (FIXTURES / "FemalePlayerCareer.js").read_text()


@pytest.fixture
def male_js() -> str:
    """Text of a three-match men's career file (opponent ages)."""
    return (FIXTURES / "MalePlayerCareer.js").read_text()
