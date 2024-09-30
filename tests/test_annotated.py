from typing import Annotated

from pytest import ExitCode, Pytester

from pytest_annotated import Fixture
from tests.conftest import ConftestFixtureResult
from tests.random_module import RandomFixtureResult, random_fixture2


def test_annotated(
    c: Annotated[ConftestFixtureResult, Fixture()],
):
    assert isinstance(c, ConftestFixtureResult)


def test_annotated_without_explicit_fixture(
    c: Annotated[ConftestFixtureResult, ""],
):
    assert isinstance(c, ConftestFixtureResult)


def test_annotated_only_type(
    c: ConftestFixtureResult,
):
    assert isinstance(c, ConftestFixtureResult)


def test_use_annotated_as_regular(conftest_fixture):
    assert isinstance(conftest_fixture, ConftestFixtureResult)


def test_use_regular_that_uses_annotated(regular_fixture):
    assert isinstance(regular_fixture, int)


def test_use_from_random_module(
    r: Annotated[RandomFixtureResult, Fixture()],
):
    assert isinstance(r, RandomFixtureResult)
    assert r.value == 1


def test_use_from_random_module_with_explicit_func(
    r: Annotated[RandomFixtureResult, Fixture(random_fixture2)],
):
    assert isinstance(r, RandomFixtureResult)
    assert r.value == 2


def test_fixture_with_missing_annotation(pytester: Pytester):
    pytester.makeconftest(
        """
        import pytest
        import pytest_annotated

        @pytest_annotated.fixture
        def name(request):
            return request.param
        """
    )

    pytester.makepyfile(
        """
        def test_thing(name):
            assert name is not None
        """
    )

    result = pytester.runpytest()
    assert result.ret is ExitCode.USAGE_ERROR
    assert any(
        "Cannot use pytest_annotated.fixture without specifying the return type in the signature"
        in line
        for line in result.stderr.lines
    )
