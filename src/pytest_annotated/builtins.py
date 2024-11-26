from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any

from pytest import (
    Cache,
    Config,
    FixtureRequest,
    LogCaptureFixture,
    MonkeyPatch,
    TempPathFactory,
    TempdirFactory,
    Testdir,
    WarningsRecorder,
    fixture,
    CaptureFixture,
)

from pytest_annotated import Fixture


__all__ = [
    "CapfdFixture",
    "CapfdbinaryFixture",
    "CaplogFixture",
    "CapsysFixture",
    "CapsysbinaryFixture",
    "CacheFixture",
    "DoctestNamespaceFixture",
    "MonkeypatchFixture",
    "PytestconfigFixture",
    "RecordPropertyFixture",
    "RecordTestsuitePropertyFixture",
    "RecwarnFixture",
    "RequestFixture",
    "TestdirFixture",
    "TmpPathFixture",
    "TmpPathFactoryFixture",
    "TmpdirFactoryFixture",
    # Pytester is not reexported as it is conditional on the pytester plugin
]


@fixture
def reexport_capfd(capfd) -> CaptureFixture[str]:
    return capfd


@fixture
def reexport_capfdbinary(capfdbinary) -> CaptureFixture[bytes]:
    return capfdbinary


@fixture
def reexport_caplog(caplog) -> LogCaptureFixture:
    return caplog


@fixture
def reexport_capsys(capsys) -> CaptureFixture[str]:
    return capsys


@fixture
def reexport_capsysbinary(capsysbinary) -> CaptureFixture[bytes]:
    return capsysbinary


@fixture
def reexport_cache(cache) -> Cache:
    return cache


@fixture
def reexport_doctest_namespace(doctest_namespace) -> dict[str, Any]:
    return doctest_namespace


@fixture
def reexport_monkeypatch(monkeypatch) -> MonkeyPatch:
    return monkeypatch


@fixture
def reexport_pytestconfig(pytestconfig) -> Config:
    return pytestconfig


@fixture
def reexport_record_property(record_property) -> Callable[[str, object], None]:
    return record_property


@fixture
def reexport_record_testsuite_property(
    record_testsuite_property,
) -> Callable[[str, object], None]:
    return record_testsuite_property


@fixture
def reexport_recwarn(recwarn) -> WarningsRecorder:
    return recwarn


@fixture
def reexport_request(request) -> FixtureRequest:
    return request


@fixture
def reexport_testdir(testdir) -> Testdir:
    return testdir


@fixture
def reexport_tmp_path(tmp_path) -> Path:
    return tmp_path


@fixture
def reexport_tmp_path_factory(tmp_path_factory) -> TempPathFactory:
    return tmp_path_factory


# Do not export this legacy fixtures as that would require us to
# pull in py.path as a dependency or import private pytest internals.
#
# from _pytest.compat import LEGACY_PATH
#
# @fixture
# def reexport_tmpdir(tmpdir) -> LEGACY_PATH:
#     return tmpdir


@fixture
def reexport_tmpdir_factory(tmpdir_factory) -> TempdirFactory:
    return tmpdir_factory


CapfdFixture = Annotated[CaptureFixture[str], Fixture(reexport_capfd)]
CapfdbinaryFixture = Annotated[CaptureFixture[bytes], Fixture(reexport_capfdbinary)]
CaplogFixture = Annotated[LogCaptureFixture, Fixture(reexport_caplog)]
CapsysFixture = Annotated[CaptureFixture[str], Fixture(reexport_capsys)]
CapsysbinaryFixture = Annotated[CaptureFixture[bytes], Fixture(reexport_capsysbinary)]
CacheFixture = Annotated[Cache, Fixture(reexport_cache)]
DoctestNamespaceFixture = Annotated[dict[str, Any], Fixture(reexport_doctest_namespace)]
MonkeypatchFixture = Annotated[MonkeyPatch, Fixture(reexport_monkeypatch)]
PytestconfigFixture = Annotated[Config, Fixture(reexport_pytestconfig)]
RecordPropertyFixture = Annotated[
    Callable[[str, object], None], Fixture(reexport_record_property)
]
RecordTestsuitePropertyFixture = Annotated[
    Callable[[str, object], None], Fixture(reexport_record_testsuite_property)
]
RecwarnFixture = Annotated[WarningsRecorder, Fixture(reexport_recwarn)]
RequestFixture = Annotated[FixtureRequest, Fixture(reexport_request)]
TestdirFixture = Annotated[Testdir, Fixture(reexport_testdir)]
TmpPathFixture = Annotated[Path, Fixture(reexport_tmp_path)]
TmpPathFactoryFixture = Annotated[TempPathFactory, Fixture(reexport_tmp_path_factory)]
TmpdirFactoryFixture = Annotated[TempdirFactory, Fixture(reexport_tmpdir_factory)]
