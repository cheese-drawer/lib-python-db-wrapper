"""An example implementation of custom object Model."""

import json
from typing import Any, List, Dict

from psycopg2 import sql
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json

from db_wrapper.model import ModelData, Model, Read, Create, Client

# tell psycopg2 to adapt all dictionaries to json instead of
# the default hstore
register_adapter(dict, Json)


class ExtendedModelData(ModelData):
    """An example Item."""

    # PENDS python 3.9 support in pylint,
    # ModelData inherits from TypedDict
    # pylint: disable=too-few-public-methods

    string: str
    integer: int
    data: Dict[str, Any]


class ExtendedCreator(Create[ExtendedModelData]):
    """Add custom json loading to Model.create."""

    # pylint: disable=too-few-public-methods

    async def one(self, item: ExtendedModelData) -> ExtendedModelData:
        """Override default Model.create.one method."""
        columns: List[sql.Identifier] = []
        values: List[sql.Literal] = []

        for column, value in item.dict().items():
            if column == 'data':
                values.append(sql.Literal(json.dumps(value)))
            else:
                values.append(sql.Literal(value))

            columns.append(sql.Identifier(column))

        query = sql.SQL(
            'INSERT INTO {table} ({columns}) '
            'VALUES ({values}) '
            'RETURNING *;'
        ).format(
            table=self._table,
            columns=sql.SQL(',').join(columns),
            values=sql.SQL(',').join(values),
        )

        result: List[ExtendedModelData] = \
            await self._client.execute_and_return(query)

        return result[0]


class ExtendedReader(Read[ExtendedModelData]):
    """Add custom method to Model.read."""

    async def all_by_string(self, string: str) -> List[ExtendedModelData]:
        """Read all rows with matching `string` value."""
        query = sql.SQL(
            'SELECT * '
            'FROM {table} '
            'WHERE string = {string};'
        ).format(
            table=self._table,
            string=sql.Identifier(string)
        )

        result: List[ExtendedModelData] = await self \
            ._client.execute_and_return(query)

        return result

    async def all(self) -> List[ExtendedModelData]:
        """Read all rows."""
        query = sql.SQL('SELECT * FROM {table}').format(
            table=self._table)

        result: List[ExtendedModelData] = await self \
            ._client.execute_and_return(query)

        return result


class ExtendedModel(Model[ExtendedModelData]):
    """Build an ExampleItem Model instance."""

    read: ExtendedReader
    create: ExtendedCreator

    def __init__(self, client: Client) -> None:
        super().__init__(client, 'extended_model')
        self.read = ExtendedReader(self.client, self.table)
        self.create = ExtendedCreator(self.client, self.table)
