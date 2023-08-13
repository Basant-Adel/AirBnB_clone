#!/usr/bin/python3
""" represents a file"""

import uuid
import datetime
from models import storage



class BaseModel:
    """" a class representing a model"""
    def __init__(self):
        """ initializes a thing"""
        self.my_number = 0
        self.name = ""
        self.updated_at = datetime.datetime.now()
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at
        storage.new(self)

    def __init__(self, *args, **kwargs):
        """ initializes a thing"""
        if len(kwargs) == 0:
            self.my_number = 0
            self.name = ""
            self.updated_at = datetime.datetime.now()
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at
        else:
            self.my_number = kwargs["my_number"]
            self.name = kwargs["name"]
            self.updated_at = datetime.datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            self.id = kwargs["id"]
            self.created_at = datetime.datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        storage.new(self)
    def save(self):
        """ update the model """
        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
        """ return a dictionary"""
        dict = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "created_at" or key == "updated_at":
                    dict[key] = value.isoformat()
                else:
                    dict[key] = value
        dict["__class__"] = self.__class__.__name__
        return dict

    def __str__(self):
        """" print"""
        print(f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")
        return ""
