#!/usr/bin/python3
""" represents a file"""

import json
import os


class FileStorage:
    """" a class representing a model"""

    def __init__(self):
        """ initializes a thing"""
        self.__file_path = ""
        self.__objects = {}

    def all(self):
        """Returns the dictionary"""
        return self.__objects

    def new(self, obj):
        """"set in object"""
        self.__objects[obj.__class__.__name__ + "." + str(obj.id)] = obj

    def save(self):
        """serializes __objects"""
        with open(self.__file_path, "w") as file:
            json.dump(self.__objects, file)

    def reload(self):
        """deserializes the JSON file"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r") as file:
                self.__objects = json.load(file)
