from dataclasses import dataclass

import pytest

import pytest_annotated


@dataclass
class RandomFixtureResult:
    value: int


@pytest_annotated.fixture
def random_fixture() -> RandomFixtureResult:
    return RandomFixtureResult(1)


@pytest.fixture
def random_fixture2() -> RandomFixtureResult:
    return RandomFixtureResult(2)
