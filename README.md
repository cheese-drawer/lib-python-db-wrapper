# DB Wrapper Lib

A simple wrapper on [aio-libs/aiopg](https://github.com/aio-libs/aiopg).
Encapsulates connection logic & execution logic into one Client class for convenience.

## Installation

Install with `pip` from releases on this repo.
For example, you can install version 0.1.0 with the following command:

```
$ pip install https://github.com/cheese-drawer/lib-python-db-wrapper/releases/download/0.1.2/db-wrapper-0.1.2.tar.gz
```

If looking for a different release version, just replace the two instances of `0.1.2` in the command with the version number you need.

## Usage

This library uses a fairly simple API to manage asynchronously connecting to, executing queries on, & disconnecting from a PostgresQL database.
Additionally, it includes a very simple Model abstraction to help with defining queries for a given model & managing separation of concerns in your application.

### Example `Client`

Intializing a database `Client` & executing a query begins with defining a connection & giving it to `Client` on intialization:

```python
from db_wrapper import ConnectionParameters

connection_parameters = ConnectionParameters(
    host='localhost',
    user='postgres',
    password='postgres',
    database='postgres')
client = Client(connection_parameters)
```

From there, you need to tell the client to connect using `Client.connect()` before you can execute any queries.
This method is asynchronous though, so you need to supply an async/await runtime.

```python
import asyncio

# ...


async def a_query() -> None:
    # we'll come back to this part
    # just know that it usins async/await to call Client.execute_and_return
    result = await client.execute_and_return(query)

    # do something with the result...

loop = asyncio.get_event_loop()
loop.run_until_complete(client.connect())
loop.run_until_complete(a_query)
loop.run_until_complete(client.disconnect())
```

You'll see we first defined a placeholder query to use after connecting the client.
In this contrived example, we established a loop, then executed in order `client.connect`, our query, & `client.disconnect` inside the loop.
In a real world application you'll probably do something significantly more complex, but this is enough to get you started.

Finally, lets define our query to just get a list of all the tables in our database's `public` schema.

```python
import asyncio

# ...


async def a_query() -> None:
    query = 'SELECT table_name' \
            'FROM information_schema.tables' \
            'WHERE table_schema = public'
    result = await client.execute_and_return(query)

    assert result[0] == 'postgres'

```

### Example: `Model`

Using `Model` isn't necessary at all, you can just interact directly with the `Client` instance using it's `execute` & `execute_and_return` methods to execute SQL queries as needed.
`Model` may be helpful in managing your separation of concerns by giving you a single place to define queries related to a given data model in your database.
Additionally, `Model` will be helpful in defining types, if you're using mypy to check your types in development.
It has no concept of types at runtime, however, & cannot be relied upon to constrain data types & shapes during runtime.

A `Model` instance has 4 properties, corresponding with each of the CRUD operations: `create`, `read`, `update`, & `delete`.
Each CRUD property has one built-in method to handle the simplest of queries for you already (create one record, read one record by id, update one record by id, & delete one record by id).

Using a model requires defining it's expected type (using `ModelData`), initializing a new instance, then calling the query methods as needed.

To define a `Model`'s expected type, you simply need to subclass `ModelData` & specify the remaining field names & types you expect from the table this `Model` will be interacting with:

```python
from db_wrapper import ModelData


class AModel(ModelData):
    a_string_value: str
    a_number_value: int
    a_boolean_value: bool
```

Subclassing `ModelData` is important because `Model` expects all records to be constrained to a dictionary containing at least one field labeled `_id` & constrained to the UUID type. This means the above `AModel` will contain records that look like the following dictionary in python:

```python
a_model_result = {
    _id: UUID(...),
    a_string_value: 'some string',
    a_number_value: 12345,
    a_boolean_value: True
}
```

Then to initialize your `Model` with your new expected type, simply initialize `Model` by passing `AModel` as a type parameter, a `Client` instance, & the name of the table this `Model` will be represented on:

```python
from db_wrapper import (
    ConnectionParameters,
    Client,
    Model,
    ModelData,
)

connection_parameters = ConnectionParameters(...)
client = Client(...)


class AModel(ModelData):
    # ...

a_model = Model[AModel](client, 'a_table_name')
```

From there, you can query your new `Model` by calling CRUD methods on the instance:

```python
from typing import List

# ...


async get_some_record() -> List[AModel]:
    return await a_model.read.one_by_id('some record id')  # NOTE: in reality the id would be a UUID
```

Of course, just having methods for creating, reading, updating, or deleting a single record at a time often won't be enough.
Adding additional queries is accomplished by extending Model's CRUD properties.

For example, if you want to write an additional query for reading any record that that has a value of `'some value'` in the field `a_field`, you would start by subclassing `Read`, the class that `Model.read` is an instance of:

```python
from db_wrapper import ModelData
from db_wrapper.model import Read
from psycopg2 import sql

# ...


class AnotherModel(ModelData):
    a_field: str


class ExtendedReader(Read[AnotherModel]):
    """Add custom method to Model.read."""

    async def all_with_some_string_value(self) -> List[AnotherModel]:
        """Read all rows with 'some value' for a_field."""

        # Because db_wrapper uses aiopg under the hood, & aiopg uses
        # psycopg2, we can define our queries safely using psycopg2's
        # sql module
        query = sql.SQL(
            'SELECT * '
            'FROM {table} '  # a Model knows it's own table name, no need to specify it manually here
            'WHERE a_field = 'some value';'
        ).format(table=self._table)

        result: List[AnotherModel] = await self \
            ._client.execute_and_return(query)

        return result
```

Then, you would subclass `Model` & redefine it's read property to be an instance of your new `ExtendedReader` class:

```python
from db_wrapper import Client, Model, ModelData

# ...

class ExtendedModel(Model[AnotherModel]):
    """Build an AnotherModel instance."""

    read: ExtendedReader

    def __init__(self, client: Client) -> None:
        super().__init__(client, 'another_model_table')  # you can supply your table name here
        self.read = ExtendedReader(self.client, self.table)
```

Finally, using your `ExtendedModel` is simple, just initialize the class with a `Client` instance & use it just as you would your previous `Model` instance, `a_model`:

```python
# ...

another_model = AnotherModel(client)

async def read_some_value_from_another_model() -> None:
    return await another_model.all_with_some_string_value()
```
