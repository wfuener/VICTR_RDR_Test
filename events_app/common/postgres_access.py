import os
import asyncpg
from common.utils import logger
from falcon import HTTPInternalServerError
import time


class PostgresAccess:

    def __init__(self, pool=None):
        # initialise object level variables
        self.pool: asyncpg.pool.Pool = None


    async def create_pool(self):
        """ Create A connection to the database via asyncpg library.
        sets class level connection variable.
        """
        db_config = {
            'database': os.environ.get("PG_NAME"),
            'port': os.environ.get("PG_PORT"),
            'host': os.environ.get("PG_HOSTNAME"),
            'user': os.environ.get("PG_USER"),
            'password': os.environ.get("PG_PW"),
        }

        try:
            conn = await asyncpg.connect(**db_config)
            if conn.is_closed():
                raise Exception("Database connection not open!")

            # one connection can be made so make a pool of connections
            pool_options = {"max_size": 10, "min_size": 10}
            pool = await asyncpg.create_pool(**db_config, **pool_options)

            logger.info("Postgres connection successfully made.")
            self.pool = pool
        except (ConnectionResetError, ConnectionRefusedError) as exc:
            logger.error("Postgres connection failed. It might not be set up yet. Waiting 5 seconds and trying again ")
            time.sleep(5)
            await self.create_pool()
        except Exception as exc:
            logger.error(f"Error getting database: {exc.__class__.__name__} - {str(exc)} ")


    async def query(self, query, data=[]):
        """Query the postgres database via asyncpg

        Args:
            query (str): sql query
            data (list): parameterized values list

        Returns:
            List(tuple): results data
        """

        try:
            # get a connection from the pool of connections
            async with self.pool.acquire() as conn:
                stmt = await conn.prepare(query)    # use prepared statements to guard against sql injection
                logger.debug(f"{data}{query}")

                records = await stmt.fetch(*data)
                # if no records are returned by the query, None will be returned
                if records:
                    records = [dict(record) for record in records]

                return records
        except Exception as exc:
            logger.error(f"ERROR ON QUERY:{query} {data}")
            # Log error type and error message
            logger.error(f"{exc.__class__.__name__} - {str(exc)}")

            # if there is an issue while querying raise 500 internal server error
            raise HTTPInternalServerError("Error occurred while querying database.")
