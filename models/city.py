#!/usr/bin/python3
""" Attributes City """

from models.base_model import BaseModel


class City(BaseModel):
    """ Attributes City """

    state_id = ""
    name = ""


def __init__(self, *args, **kwargs):
    """ INIT """

    super().__init__(*args, **kwargs)
