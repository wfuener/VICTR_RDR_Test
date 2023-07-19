"""This modules holds all falcon middleware and extras"""
import logging
import os
import time
import json
from datetime import datetime
from functools import partial

import falcon
import rapidjson
from falcon import media

from common.postgres_access import PostgresAccess
# only import the middleware and extra handlers


__all__ = [
    'RequestLoggerMiddleware',
    'DBMiddleware',
    'AuthMiddleware',
    'extra_handlers',
    'handle_uncaught_exception',
]

logger = logging.getLogger("events_app")


class RequestLoggerMiddleware(object):
    """Logging debug statement for every request"""

    async def process_request(self, req, resp):
        """Add debug logs for every request. Making it a bit eaiser to read"""
        logger.debug(f"-----------------------------------------------------------------\n")
        logger.debug(f"Request: {req.method} {req.relative_uri}""")


class DBMiddleware:
    """Attach database access instance to every request"""

    def __init__(self):
        self.pg = None

    async def process_startup(self, scope, event):
        """At app start create connection pool"""
        self.pg = PostgresAccess()
        await self.pg.create_pool()


    async def process_request(self, req, resp):
        """Add postgress access object to all incoming requests"""
        req.context.pg = self.pg


class AuthMiddleware:
    """Mock authorization to all incoming requests"""

    async def process_request(self, req, resp):
        logger.debug("Request validated")


# override default falcon json handler which uses python's default json library
# Decimal and datetime are not apart of default json so they need to be defined explicitly.

json_handler = media.JSONHandler(
    dumps=partial(
        rapidjson.dumps,
        ensure_ascii=False,
        sort_keys=True,
        uuid_mode=rapidjson.UM_CANONICAL,
        datetime_mode=rapidjson.DM_ISO8601,
        number_mode=rapidjson.NM_DECIMAL
    ),
    loads=partial(
        rapidjson.loads,
        uuid_mode=rapidjson.UM_CANONICAL,
        datetime_mode=rapidjson.DM_ISO8601,
        number_mode=rapidjson.NM_DECIMAL
    ),
)
extra_handlers = {
    'application/json': json_handler,
}


async def handle_uncaught_exception(req, resp, ex, params):
    """All errors that aren't caught will be logged and 500 response will be thrown"""
    logger.exception(f'Unhandled error. {resp.data}', exc_info=True)
    raise falcon.HTTPInternalServerError(title="Something went wrong on the server.")

