import random as rnd
import csv
from abc import ABC, abstractmethod

# csv creator, creates a csv files with a given config
roundPrecision = 3


class BoundType(ABC):
    def __init__(self, dtype, params):
        self.dType = dtype
        self.params = params

    @abstractmethod
    def generate(self):
        pass


class FixedLength(BoundType):
    # params is length
    def generate(self):
        length = self.params.get("len", 1)
        if self.dType == "int":
            return rnd.randint(10 ** (length - 1), 10 ** length - 1)
        elif self.dType == "float":
            return FixedLength("int", self.params).generate() + round(rnd.random(), roundPrecision)
        elif self.dType == "string":
            alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            word = [rnd.choice(alphabet) for _ in range(length)]
            return ''.join(word)
        else:
            return None


class FixedRange(BoundType):
    # params is range
    def generate(self):
        lo, hi = (self.params.get("lohi"))
        if self.dType == "int":
            return rnd.randint(lo, hi)
        elif self.dType == "float":
            return round(rnd.uniform(lo, hi), roundPrecision)
        else:
            return None


class FromPossibleValues(BoundType):
    # params is a list
    def generate(self):
        possibleval = self.params.get("set", set())
        return rnd.choice(possibleval)


def createcsv(rows, filename, schema):
    with open(f'./output/{filename}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(schema.keys())
        for _ in range(rows):
            writer.writerow([x.generate() for x in schema.values()])
