import importlib
import inspect
from collections.abc import Callable, Iterable, Sequence
from typing import Annotated, Any, TypeGuard, TypeVar

import pytest
from _pytest.config import PytestPluginManager
from _pytest.fixtures import (
    FixtureFunction,
    FixtureManager,
    FuncFixtureInfo,
    _get_direct_parametrize_args,
    deduplicate_names,
)
from _pytest.scope import _ScopeName

_T = TypeVar("_T")

_ANNOT_TYPE = type(Annotated[int, ""])


def _is_annotated(hint: _T) -> TypeGuard[_T]:
    return (type(hint) is _ANNOT_TYPE) and hasattr(hint, "__metadata__")


class Fixture:
    def __init__(self, fixture: Callable | None = None):
        self.fixture = fixture


_GLOBAL_TYPE_TO_FIXTURE_MAPPINGS: dict[type, Callable] = {}


# TODO: can we do something better here?
def add_annotated_fixture_mapping(type_: type, fixture: Callable):
    if prev := _GLOBAL_TYPE_TO_FIXTURE_MAPPINGS.get(type_):
        assert prev == fixture
    else:
        _GLOBAL_TYPE_TO_FIXTURE_MAPPINGS[type_] = fixture


def _resolve_from_type(type_: type) -> Callable:
    if res := _GLOBAL_TYPE_TO_FIXTURE_MAPPINGS.get(type_):
        return res
    raise Exception("Unknown fixture")


def fixture(
    fixture_function: FixtureFunction | None = None,
    *,
    scope: _ScopeName | Callable[[str, pytest.Config], _ScopeName] = "function",
    params: Iterable[object] | None = None,
    autouse: bool = False,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = None,
    name: str | None = None,
) -> Callable[[FixtureFunction], FixtureFunction] | FixtureFunction:
    def wrapper(func: FixtureFunction) -> FixtureFunction:
        sig = inspect.signature(func)
        if sig.return_annotation is inspect.Signature.empty:
            raise Exception(
                "Cannot use pytest_annotated.fixture without specifying the return type in the signature"
            )
        fixture = pytest.fixture(
            func,
            scope=scope,
            params=params,
            autouse=autouse,
            ids=ids,
            name=name,
        )
        add_annotated_fixture_mapping(sig.return_annotation, fixture)
        return fixture

    if fixture_function:
        return wrapper(fixture_function)
    return wrapper


class AnnotatedFixturePlugin:
    def __init__(self, pm: PytestPluginManager):
        self.pm = pm
        self.fm: FixtureManager | None = None

    def _resolve_from_type(self, annotation: type) -> str | None:
        assert self.fm is not None
        if fixture_func := _GLOBAL_TYPE_TO_FIXTURE_MAPPINGS.get(annotation):
            fixturename = fixture_func.__name__
            if fixturename not in self.fm._arg2fixturedefs:
                # if the fixture hasn't been registered, we force the pluginmanager to import the module that contains the fixture, which will make it available (and hopefully not have any weird side effects)
                # this is required because if the function was not directly imported in the test, or in another plugin/conftest, then the fixture will not be registered as an actual fixture
                mod = importlib.import_module(fixture_func.__module__)
                self.fm.parsefactories(
                    mod,
                    None,
                )
            return fixturename
        return None

    def pytest_pycollect_makeitem(self, collector, name: str, obj):
        if self.fm is None:
            self.fm = self.pm.get_plugin("funcmanage")
            assert self.fm is not None

        if inspect.isfunction(obj) and (
            name.startswith("test_") or name.endswith("_test")
        ):
            signature = inspect.signature(obj)
            has_annotated_fixture = False
            argnames: tuple[str, ...] = ()
            replace_argnames = {}
            for param in signature.parameters.values():
                argname = param.name
                annotation = param.annotation
                if _is_annotated(annotation):
                    for anno in annotation.__metadata__:
                        if isinstance(anno, Fixture):
                            if anno.fixture is None:
                                fixturename = self._resolve_from_type(
                                    annotation.__origin__
                                )
                            elif inspect.isfunction(anno.fixture):
                                fixturename = anno.fixture.__name__
                            else:
                                raise Exception("Unknown fixture")
                            if fixturename is not None:
                                has_annotated_fixture = True
                                argnames += (fixturename,)
                                replace_argnames[fixturename] = argname
                                break
                            else:
                                raise Exception(
                                    f"No annotated fixture found for type {annotation.__origin__}"
                                )
                    else:
                        if fixturename := self._resolve_from_type(
                            annotation.__origin__
                        ):
                            has_annotated_fixture = True
                            replace_argnames[fixturename] = argname
                            argnames += (fixturename,)
                        else:
                            argnames += (argname,)
                else:
                    if annotation is not inspect.Signature.empty and (
                        fixturename := self._resolve_from_type(annotation)
                    ):
                        has_annotated_fixture = True
                        replace_argnames[fixturename] = argname
                        argnames += (fixturename,)
                    else:
                        argnames += (argname,)

            if has_annotated_fixture:
                usefixturesnames = self.fm._getusefixturesnames(collector)
                autousenames = self.fm._getautousenames(collector)
                initialnames = deduplicate_names(
                    autousenames, usefixturesnames, argnames
                )

                direct_parametrize_args = _get_direct_parametrize_args(collector)

                names_closure, arg2fixturedefs = self.fm.getfixtureclosure(
                    parentnode=collector,
                    initialnames=initialnames,
                    ignore_args=direct_parametrize_args,
                )
                argnames = tuple(
                    replace_argnames[n] if n in replace_argnames else n
                    for n in argnames
                )
                initialnames = tuple(
                    replace_argnames[n] if n in replace_argnames else n
                    for n in initialnames
                )
                names_closure = [
                    replace_argnames[n] if n in replace_argnames else n
                    for n in names_closure
                ]
                for fixturename, argname in replace_argnames.items():
                    arg2fixturedefs[argname] = arg2fixturedefs[fixturename]

                fixtureinfo = FuncFixtureInfo(
                    argnames, initialnames, names_closure, arg2fixturedefs
                )
                func = pytest.Function.from_parent(
                    name=name,
                    parent=collector,
                    callobj=obj,
                    fixtureinfo=fixtureinfo,
                )
                return func


def pytest_configure(config: pytest.Config) -> None:
    if config.pluginmanager.get_plugin("pytest_annotated_internal") is None:
        config.pluginmanager.register(
            AnnotatedFixturePlugin(config.pluginmanager), "pytest_annotated_internal"
        )
