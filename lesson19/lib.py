import re
from collections import defaultdict
from typing import Optional

import parse


class Arguments:
    ip: str = None
    user: str = None
    tm: str = None
    r_type: str = None
    r_contain: str = None
    r_version: str = None
    code: str = None
    bites: str = None
    url: str = None
    agent: str = None
    lng: int = None
    __err__ = []

    def __handle__(self, arg_name: str, arg_val: str):
        arg_val = arg_val.strip()

        if arg_name == 'ip':
            res = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", arg_val)
            if res is not None:
                self.ip = res.group()
            else:
                msg = 'Can\'t parse "ip"'
                self.__err__.append(msg)
                raise Exception(msg)

        elif arg_name == 'r_type':
            res = re.search(r"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", arg_val.upper())
            if res is not None:
                self.r_type = res.group()

            else:
                self.r_type = 'UNKNOWN'
                msg = 'Can\'t parse correct "r_type"'
                self.__err__.append(msg)
                raise Exception(msg)

        elif arg_name == 'lng':
            res = re.search(r"\d+", arg_val)
            if res is not None:
                self.lng = int(res.group())
            if arg_val != '"-"' and re.search(r"\D+", arg_val):
                msg = 'Can\'t parse "lng" as int'
                self.__err__.append(msg)
                raise Exception(msg)

        else:
            setattr(self, arg_name, arg_val)

    def to_dict(self) -> dict:
        return {
            key: val for key, val in self.__dict__.items() if not key.startswith('_')
        }

    def __str__(self):
        return str(self.to_dict())


class Matcher:
    PATTERN = '{ip} - {user} [{tm}] "{r_type} {r_contain} {r_version}" {code} {bites} "{url}" "{agent}" {lng}'

    def __init__(self):
        self.parser = parse.Parser(self.PATTERN)
        self.errors: dict[Arguments, set] = defaultdict(set)

    def match(self, matching: str) -> Optional[Arguments]:
        matching2 = matching.strip().replace(' "" ', ' "-" ')
        matching1 = matching2.replace('\\"', "'")

        for m in (matching1, matching2):
            arguments = Arguments()
            if result := self.parser.parse(m):
                err = None
                for name, value in result.named.items():
                    try:
                        arguments.__handle__(name, value)
                    except Exception as e:
                        err = e
                        self.errors[arguments].add(str(e))
                if err:
                    self.errors[arguments].add(m)
            else:
                continue

            return arguments
