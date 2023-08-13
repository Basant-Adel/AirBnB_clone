#!/usr/bin/python3
""" Attributes Amenity """

from models.base_model import BaseModel


class Amenity(BaseModel):
    """ Attributes Amenity """

    name = ""


def __init__(self, *args, **kwargs):
    """ INIT """

    super().__init__(*args, **kwargs)
