"""An example of how to use SyncClient & Model together."""

import json
import logging
import os
from uuid import uuid4, UUID
from typing import Any, List

from db_wrapper import SyncClient, ConnectionParameters
from db_wrapper.model import SyncModel as Model

from example.models import (
    AModel,
    ExtendedModel,
    ExtendedModelData,
)

logging.basicConfig(level=logging.INFO)


class UUIDJsonEncoder(json.JSONEncoder):
    """Extended Json Encoder to allow encoding of objects containing UUID."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)

        return obj


conn_params = ConnectionParameters(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '5432')),
    # user=os.getenv('DB_USER', 'postgres'),
    # password=os.getenv('DB_PASS', 'postgres'),
    # database=os.getenv('DB_NAME', 'postgres'))
    user=os.getenv('DB_USER', 'test'),
    password=os.getenv('DB_PASS', 'pass'),
    database=os.getenv('DB_NAME', 'dev'))
client = SyncClient(conn_params)

a_model = Model[AModel](client, 'a_model', AModel)
extended_model = ExtendedModel(client)


def create_a_model_record() -> UUID:
    """
    Show how to use a simple Model instance.

    Create a new record using the default Model.create.one method.
    """
    new_record = AModel(**{
        'id': uuid4(),
        'string': 'some string',
        'integer': 1,
        'array': ['an', 'array', 'of', 'strings'],
    })

    a_model.create.one(new_record)

    return new_record.id


def read_a_model(id_value: UUID) -> AModel:
    """Show how to read a record with a given id value."""
    # read.one_by_id expects a string, so UUID values need
    # converted using str()
    return a_model.read.one_by_id(str(id_value))


def create_extended_models() -> None:
    """Show how using an extended Model can be the same as the defaults."""
    dicts = [{
        'id': uuid4(),
        'string': 'something',
        'integer': 1,
        'data': {'a': 1, 'b': 2, 'c': True}
    }, {
        'id': uuid4(),
        'string': 'something',
        'integer': 1,
        'data': {'a': 1, 'b': 2, 'c': True}
    }, {
        'id': uuid4(),
        'string': 'something',
        'integer': 1,
        'data': {'a': 1, 'b': 2, 'c': True}
    }, {
        'id': uuid4(),
        'string': 'something',
        'integer': 1,
        'data': {'a': 1, 'b': 2, 'c': True}
    }]

    new_records: List[ExtendedModelData] = [
        ExtendedModelData(**record) for record in dicts]

    # by looping over a list of records, you can use the default create.one
    # method to create each record as a separate transaction
    for record in new_records:
        extended_model.create.one(record)


def read_extended_models() -> List[ExtendedModelData]:
    """Show how to use an extended Model's new methods."""
    # We defined read.all in ./models/extended_model.py's ExtendedRead class,
    # then replaced ExtendedModel's read property with ExtendedRead.
    # As a result, we can call it just like any other method on Model.read.
    return extended_model.read.all()


def run() -> None:
    """Show how to make a connection, execute queries, & disconnect."""
    # First, have the client make a connection to the database
    client.connect()

    # Then, execute queries using the models that were initialized
    # with the client above.
    # Doing this inside a try/finally block allows client to gracefully
    # disconnect even when an exception is thrown.
    try:
        new_id = create_a_model_record()
        created_a_model = read_a_model(new_id)
        create_extended_models()
        created_extended_models = read_extended_models()
    finally:
        client.disconnect()

    # Print results to stdout
    print(json.dumps(created_a_model.dict(), cls=UUIDJsonEncoder))
    print(json.dumps([item.dict()
          for item in created_extended_models], cls=UUIDJsonEncoder))


if __name__ == '__main__':
    run()
