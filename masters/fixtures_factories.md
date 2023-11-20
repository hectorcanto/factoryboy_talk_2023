## Fixtures and factories
<!-- .element: style="color:#DDD;background-color:#3336" -->
#### by Hector Canto
<!-- .element: style="color:#DDD;background-color:#3336" -->

## Test fixtures - Hector Canto<!-- .element: style="visibility:hidden" -->


[comment]: # (!!! data-state="no-title-footer" data-background-image="../assets/denis_doukan_607002_pixabay_snake-1285354_1920.jpg")


## We will talk about

- **fixture** concept
- How to build fixtures with:
  - **factoryboy**: Mother pattern
  - **faker*: data generator
- Make it work in **pytest**

![](../assets/clouds.jpg)<!-- .element: style="display:inline; float:right; width:270px" -->


[comment]: # (|||)


### What is a fixture


"""A test fixture is a device used to consistently test some item, device, or piece of software.
Test fixtures are used in the testing of electronics, software and physical devices."""

- [wikipedia.com/en/Test_fixture](wikipedia.com/en/Test_fixture)

[comment]: # (|||)


### Why is this important

- Testing should be a big chunk of our daily work
- Testing is hard and costly
- Let's make it easier
- Making new tests should become easier with time

[comment]: # (|||)


### Testing structure: AAA

- **Arrange**
- Act - Execute
- Assert

[comment]: # (|||)

### Arranging

- In arrange phase we prepare the test
  - data to input
  - data to be "there"
  - the system to act
  - secondary systems to interact

[comment]: # (|||)


### Data fixtures

We are going to focus on data fixtures for
- inputs
- expectancies

[comment]: # (|||)


### AAA in python unitest

```python
class TestExample(unittest.Case):

    def setUp(self):
        ...

    def test_one(self):
        dummy_user = ExampleUserFactory()
        self.db.save(dummy_user)
        ...
        result = SystemUnderTest()
        ...
        self.assertTrue(result)

    def tearDown(self):
        ...
```

[comment]: # (|||)


### In pytest

Any test dependency<br/>
usually set as parameter or decorator

```python
import pytest

@pytest.fixture(autouse=True, scope="session")
def global_fixture():
    ...

pytestmark = pytest.mark.usefixtures("module_fixture")

@pytest.mark.usefixtures("fixture_as_decorator")
def test_one(fixture_as_param):
    ...
```

[comment]: # (|||)


## AAA in pytest

```python
@pytest.fixture(scope="module", name="arranged", autouse=False)
def arrange_fixtures():
    ... # set up
    yield "value"
    ... # tear down

def test_using_fixture_explicitly(arranged):
    result = SystemUnderTest(arranged)
    assert result is True
    ...
```

[comment]: # (|||)

### Pytest over Unittest

- More compressed code
- Great plugins
- More reusability
- Less verbose but more magical
- More pythonic syntax

[comment]: # (!!! data-visibility="hidden")


### Data fixtures can be

- Inputs
- Configuration
- Data present in DB, cache files,
- Params to query
- A dependency to inject

[comment]: # (|||)

## Data fixtures can be (II)

- A mock or dummy to use or inject
- Set the application's state
- Ready the system under test
- The system under test ready for assertion
- Revert or clean-up procedures

[comment]: # (|||)

### Where to put fixtures:

- in the same place as the test
  - but it makes the IDE angry
- in the closest `conftest.py`
  - `conftest` is pytest's `__init__.py`
  - makes fixture globally available downstream

[comment]: # (|||)

### Fixture example

```python
import random

@pytest.fixture(name="cool_fixture")
def this_name_is_just_for_the_function():
    yield random.randint()

def test_using_fixture(cool_fixture):
    system_under_test(param=cool_fixture)
```

[comment]: # (|||)

### Test name fixture

```python
def test_one(request):
   test_name = request.node.name
   result = system_under_test(test_name)
   assert result == test_name
```


[comment]: # (!!!)


### Anti-patterns

- Copy-paste the same dict for each test
- Have a thousand JSON files

###
### Recommendations

- Generate them programmatically
- In the test, highlight the difference
- Use Mother pattern and data generators

[comment]: # (|||)


### Enter factory-boy

```python
import factory

class UserMother(factory.DictFactory):
    firstname = "Hector"
    lastname = "Canto"
    address = "Praza do Rei, 1, Vigo CP 36000"
```

[comment]: # (|||)

### Enter faker

```python
class UserMother(factory.DictFactory):
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    address = factory.Faker('address')

random_user = UserMother()
random_user == {
    'firstname': 'Rebecca',
    'lastname': 'Sloan',
    'address': '52097 Daniel Ports Apt. 689\nPort Jeffrey, NM 55289'
}
```

[comment]: # (|||)

### More faker

```python
random_user = UserMother(firstname="Guido)
random_user == {
   'firstname': 'Guido',
   'lastname': 'Deleon',
    'address': '870 Victoria Mills\nWilliamville, CA 44946'
}
```

[comment]: # (|||)


### Batch generation

```python
UserMother.create_batch(size=5)
```

###
### Iterated generation

```python
UserMother.create_batch(size=10, firstname=factory.Iterator(["One", "Two", Thee]))
```


[comment]: # (!!!)

## FactoryBoy with ORMs

- DjangoORM
- SQLAlchemy
- Mogo and MongoEngine
- not hard to create your own

[comment]: # (|||)

### Example

```python
class UserMother(factory.orm.SQLAlchemyFactory):
    class Meta:
        model = User
        sqlalchemy_session_factory = lambda: common.TestSession()

def test_with_specific_db(test_session):
    UserMother._meta.sqlalchmey_session = test_session
    # You can also set the live DB and populate it for demos
```

<aside class="notes">
Session can be configured prior to use the Factory
</aside>


[comment]: # (!!!)

## Set up for SQLA

```python
import factory
from sqlalchemy import orm

TestSession = orm.scoped_session(orm.sessionmaker())
"""Global scoped session (thread-safe) for tests"""

class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = TestSession
        sqlalchemy_session_persistence = "flush"

class UserFactory(BaseFactory):
      class Meta:
          model = User
```

[comment]: # (|||)


## Get or Create Fixture

```python
# Create user once, use everywhere
class UserFactory(BaseUserFactory):
    class Meta:
        sqlalchemy_get_or_create = ('id',)

user1 = UserFactory(id=1, firstname="Dennis", lastname="Ritchie")
user2 = UserFactory(id=1)
user1 == user2
```

[comment]: # (|||)


### Good things about factory-boy

- Highly customizable
- Related factories
- Works with ORM

[comment]: # (|||)


### Bad things

- Inner Faker is weird
- Documentation gaps (as usual)
- A bit hard to work with relationships

[comment]: # (|||)


### For the future

- polyfactory
- make your own providers
- check out Maybe, Traits, post_gen hooks
- random seed fixing
- sequence resetting
- user `random.sample` and others

### Tactical tips

- Add factories to your libraries
- Specially in serverless and microservices

[comment]: # (|||)

### Real case example

- 3 libraries: common models, common APIs, common 3rd party services
- On each we have factories to create
  - DB data
  - API callback bodies
  - event message payloads

[comment]: # (|||)

### Code samples

- `tests/user_factories.py`
  - Params
  - Related
  - Fuzzy
  - Lazy
- `/tests/conftest.py`

[comment]: # (|||)


### Register fixtures

```python
# tests/conftest/py
register(AdminFactory, "admin")
register(DbUserFactory, "user1", email="user1@hello.es")
register(DbUserFactory, "user2", status=0)
register(DbProfileFactory2, "profile")

# usage
def test_with_reg_fx(admin):
    assert admin.first_name == "Admin"
```



[comment]: # (!!!)


### TODO Pending examples

- Temp files
- factory Traits (params that modify fixture fields directly)
- Maybe (decider)
- post generation hooks
- `__sequence=10` and `reset_sequence`
- `factory.build(dict, FACTORY_CLASS=UserFactory)`
- `cat_key = FuzzyChoice(User.ENUM_CATEGORY_CHOICES, getter=lambda c: c[0])`

[comment]: # (||| data-visibility="hidden")
