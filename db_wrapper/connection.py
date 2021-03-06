"""Interface & function for defining & establishing connection to Postgres."""

import asyncio
from dataclasses import dataclass
import logging
from typing import Optional

from psycopg2.extras import RealDictCursor  # type: ignore
from psycopg2 import OperationalError  # type: ignore

# no stubs available, starting out by just determining correct return
# types & annotating in my wrappers here
import aiopg  # type: ignore

#
# Postgres Connection helper
#

LOGGER = logging.getLogger(__name__)


@dataclass
class ConnectionParameters:
    """Defines connection parameters for database."""

    host: str
    port: int
    user: str
    password: str
    database: str


async def _try_connect(
    connection_params: ConnectionParameters,
    retries: int = 1
) -> aiopg.Connection:
    database = connection_params.database
    user = connection_params.user
    password = connection_params.password
    host = connection_params.host
    port = connection_params.port

    dsn = f'dbname={database} user={user} password={password} host={host} port={port}'

    # PENDS python 3.9 support in pylint
    # pylint: disable=unsubscriptable-object
    connection: Optional[aiopg.Connection] = None

    LOGGER.info(
        f'Attempting to connect to database {database} as {user}@{host}:{port}...')

    while connection is None:
        try:
            connection = await aiopg.connect(
                dsn,
                cursor_factory=RealDictCursor)
        except OperationalError as err:
            print(type(err))
            if retries > 12:
                raise ConnectionError(
                    'Max number of connection attempts has been reached (12)'
                ) from err

            LOGGER.info(
                f'Connection failed ({retries} time(s))'
                'retrying again in 5 seconds...')

            await asyncio.sleep(5)
            return await _try_connect(connection_params, retries + 1)

    return connection


# PENDS python 3.9 support in pylint
# pylint: disable=unsubscriptable-object
async def connect(
    connection_params: ConnectionParameters
) -> aiopg.Connection:
    """Establish database connection."""
    return await _try_connect(connection_params)
