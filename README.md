# Pytest Annotated

A Pytest plugin to allow the use of `Annotated` to resolve fixtures, allowing test arguments to have different names to the fixture itself.

## Usage:

#### Simple:

```
from typing import Annotated
from pytest_annotated import Fixture

class SomeThing:
    pass

@pytest.fixture
async def somefixture(someotherfixture) -> SomeThing:
    return SomeThing()

async def test_thing(st: Annotated[SomeThing, Fixture(somefixture)]):
    assert isinstance(st, SomeThing)

```

#### Aliased:

```
from typing import Annotated
from pytest_annotated import Fixture

class SomeThing:
    pass

@pytest.fixture
async def somefixture(someotherfixture) -> SomeThing:
    return SomeThing()

SomethingFixture = Annotated[SomeThing, Fixture(somefixture)]

async def test_thing(st: SomethingFixture):
    assert isinstance(st, SomeThing)
```

#### Registered Type:

Uses `@pytest_annotated.fixture` instead of `@pytest.fixture` to register the annotated return type of a fixture to always be resolved using that fixture.

```
from typing import Annotated
import pytest_annotated
from pytest_annotated import Fixture

class SomeThing:
    pass

@pytest_annotated.fixture
async def somefixture(someotherfixture) -> SomeThing:
    return SomeThing()

async def test_thing(st: SomeThing):
    assert isinstance(st, SomeThing)
```


## TODO:

 - Support `Annotated` function arguments in fixtures as well.
 - Figure out if there's a way to do this without using so many `_private` parts of pytest!
