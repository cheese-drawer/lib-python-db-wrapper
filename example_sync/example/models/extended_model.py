"""An example implementation of custom object SyncModel."""

import json
from typing import Any, List, Dict

from psycopg2 import sql
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json

from db_wrapper import SyncClient
from db_wrapper.model import ModelData, SyncModel, SyncRead, SyncCreate

# tell psycopg2 to adapt all dictionaries to json instead of
# the default hstore
register_adapter(dict, Json)


class ExtendedModelData(ModelData):
    """An example Item."""

    string: str
    integer: int
    data: Dict[str, Any]


class ExtendedCreator(SyncCreate[ExtendedModelData]):
    """Add custom json loading to SyncModel.create."""

    # pylint: disable=too-few-public-methods

    def one(self, item: ExtendedModelData) -> ExtendedModelData:
        """Override default SyncModel.create.one method."""
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
            self._client.execute_and_return(query)

        return result[0]


class ExtendedReader(SyncRead[ExtendedModelData]):
    """Add custom method to Model.read."""

    def all_by_string(self, string: str) -> List[ExtendedModelData]:
        """Read all rows with matching `string` value."""
        query = sql.SQL(
            'SELECT * '
            'FROM {table} '
            'WHERE string = {string};'
        ).format(
            table=self._table,
            string=sql.Identifier(string)
        )

        result: List[ExtendedModelData] = self \
            ._client.execute_and_return(query)

        return result

    def all(self) -> List[ExtendedModelData]:
        """Read all rows."""
        query = sql.SQL('SELECT * FROM {table}').format(
            table=self._table)

        result: List[ExtendedModelData] = self \
            ._client.execute_and_return(query)

        return result


class ExtendedModel(SyncModel[ExtendedModelData]):
    """Build an ExampleItem SyncModel instance."""

    read: ExtendedReader
    create: ExtendedCreator

    def __init__(self, client: SyncClient) -> None:
        super().__init__(client, 'extended_model')
        self.read = ExtendedReader(self.client, self.table)
        self.create = ExtendedCreator(self.client, self.table)
