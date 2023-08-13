#!/usr/bin/python3
""" First User """

from models.base_model import BaseModel


class User(BaseModel):
    """ First User """

    email = ""
    password = ""
    first_name = ""
    last_name = ""


def __init__(self, *args, **kwargs):
    """ INIT """

    super().__init__(*args, **kwargs)
