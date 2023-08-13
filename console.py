#!/usr/bin/python3
""" A Program Console """


import re
import cmd
import models
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ HBNB -> The Command Interpreter """

    prompt = '(hbnb) '
    classes = {
        "BaseModel",
        "User", "Place",
        "State", "City",
        "Amenity", "Review",
    }

    def parse(input):
        """
        It takes input str as a parameter
        and uses regular expressions
        to return a list of parsed elements
        """
        curly_braces_match = re.search(r"\{(.*?)\}", input)
        brackets_match = re.search(r"\[(.*?)\]", input)

        if not curly_braces_match:
            if not brackets_match:
                return [item.strip(",") for item in input.split()]
            lexer = input[:brackets_match.span()[0]].split()
            result_list = [item.strip(",") for item in lexer]
            result_list.append(brackets_match.group())
            return result_list
        lexer = input[:curly_braces_match.span()[0]].split()
        result_list = [item.strip(",") for item in lexer]
        result_list.append(curly_braces_match.group())
        return result_list

    def do_EOF(self, input):
        """ EOF -> method in the HBNB Command """
        print("")
        return True

    def do_quit(self, input):
        """ Quit -> method in the HBNB Command """
        return True

    def emptyline(self):
        """ Empty Line -> method in the HBNB Command """
        pass

    def do_create(self, input):
        """ Create -> method in the HBNB Command """
        if not input:
            print("** class name missing **")
        elif input not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            instance = eval(input)()
            print(instance.id)
            models.storage.save()

    def do_show(self, input):
        """ Show -> method in the HBNB Command """
        argus = HBNBCommand.parse(input)
        matter = models.storage.all()

        if not argus:
            print("** class name missing **")
        elif argus[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(argus) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argus[0], argus[1]) not in matter:
            print("** no instance found **")
        else:
            print(matter["{}.{}".format(argus[0], argus[1])])

    def do_destroy(self, input):
        """ Destroy -> method in the HBNB Command """
        argus = HBNBCommand.parse(input)
        matter = models.storage.all()

        if not argus:
            print("** class name missing **")
        elif argus[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(argus) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argus[0], argus[1]) not in matter:
            print("** no instance found **")
        else:
            del matter["{}.{}".format(argus[0], argus[1])]
            models.storage.save()

    def do_all(self, input):
        """ All -> method in the HBNB Command """
        argus = HBNBCommand.parse(input)
        matter = models.storage.all()

        if argus and argus[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            objs = []
            for obj in matter.values():
                if argus and argus[0] == obj.__class__.__name__:
                    objs.append(obj.__str__())
                elif not argus:
                    objs.append(obj.__str__())
            print(objs)

    def do_update(self, input):
        """ Update -> method in the HBNB Command """
        argus = HBNBCommand.parse(input)
        matter = models.storage.all()

        if not argus:
            print("** class name missing **")
            return False
        if argus[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(argus) == 1:
            print("** instance id missing **")
            return False

        if "{}.{}".format(argus[0], argus[1]) not in matter.keys():
            print("** no instance found **")
            return False
        if len(argus) == 2:
            print("** attribute name missing **")
            return False
        if len(argus) == 3:
            try:
                type(eval(argus[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        obj = matter["{}.{}".format(argus[0], argus[1])]
        if len(argus) == 4:
            if argus[2] in obj.__class__.__dict__.keys():
                argtypes = type(obj.__class__.__dict__[argus[2]])
                obj.__dict__[argus[2]] = argtypes(argus[3])
            else:
                obj.__dict__[argus[2]] = argus[3]
        elif type(eval(argus[2])) == dict:
            for k, v in eval(argus[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    argtypes = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = argtypes(v)
                else:
                    obj.__dict__[k] = v
        models.storage.save()

    def do_count(self, input):
        """ Count -> method in the HBNB Command """
        argus = HBNBCommand.parse(input)
        count = 0

        for obj in models.storage.all().values():
            if argus[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def _precmd(self, line):
        """ _Precmd -> method in the HBNB Command """
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line

        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)

        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search
            ('^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)

            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                   1) or "") + " " + (match_attr_and_value.group(2) or "")

        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def default(self, line):
        """ Default -> method in the HBNB Command """
        self._precmd(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
