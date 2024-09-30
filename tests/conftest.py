import random
from dataclasses import dataclass

import pytest

import pytest_annotated

pytest_plugins = ["pytest_annotated", "pytester"]


@dataclass
class ConftestFixtureResult:
    value: int


@pytest_annotated.fixture
def conftest_fixture() -> ConftestFixtureResult:
    return ConftestFixtureResult(random.randint(0, 100000))


@pytest.fixture
def regular_fixture(conftest_fixture):
    return conftest_fixture.value
