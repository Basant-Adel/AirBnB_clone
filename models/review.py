#!/usr/bin/python3
""" Attributes Review """

from models.base_model import BaseModel


class Review(BaseModel):
    """ Attributes Review """

    place_id = ""

    user_id = ""

    text = ""


def __init__(self, *args, **kwargs):
    """ INIT """

    super().__init__(*args, **kwargs)
