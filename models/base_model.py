#!/usr/bin/python3
""" Base Model """

import uuid
import models
from datetime import datetime


class BaseModel:
    """ Base Model """

    def __init__(self, *args, **kwargs):
        """ INIT """

        timef = '%Y-%m-%dT%H:%M:%S.%f'

        if kwargs:

            for key, val in kwargs.items():

                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(val, timef))

                elif key == '__class__':
                    continue

                else:
                    setattr(self, key, val)

        else:

            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

            models.storage.new(self)

    def save(self):
        """ Save """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ Return Dictionary """

        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()

        return obj_dict

    def __str__(self):
        """ Return String """

        cname = self.__class__.__name__
        return "[{}] ({}) {}".format(cname, self.id, self.__dict__)
