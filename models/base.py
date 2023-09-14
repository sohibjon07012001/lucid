import typing
from pydantic import *
from tortoise import Tortoise
from value_types import *
from tortoise.contrib.pydantic.creator import pydantic_model_creator

import config

Tortoise.init_models(
    config.Database.MODULES, "db"
)