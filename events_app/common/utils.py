"""This module holds commonly used items that are shared across
the app. Like the logger and the json schema validator"""

from jsonschema import validators, Draft4Validator
import logging
import sys


validator = validators.create(
    meta_schema=Draft4Validator.META_SCHEMA,
    validators=dict(
        Draft4Validator.VALIDATORS,
    )
)

# get and name logger
logger = logging.getLogger("events_app")
logger.setLevel('DEBUG')    # This change this level in production to INFO
logger.addHandler(logging.StreamHandler(sys.stdout))  # write to sys.out
