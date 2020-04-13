from enum import Enum


class Level(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class Fuzz():
    def __init__(self):
        pass


class Fuzzifier():
    @staticmethod
    def to_level(s, m, l):
        return Level([s, m, l].index(max([s, m, l])))

    @staticmethod
    def fl(input_):
        f = Fuzzifier()
        s = f.side_small(input_)
        m = f.side_medium(input_)
        l = f.side_large(input_)
        return Fuzzifier.to_level(s, m, l)

    @staticmethod
    def fr(input_):
        f = Fuzzifier()
        s = f.side_small(input_)
        m = f.side_medium(input_)
        l = f.side_large(input_)
        return Fuzzifier.to_level(s, m, l)

    @staticmethod
    def f(input_):
        f = Fuzzifier()
        s = f.front_small(input_)
        m = f.front_medium(input_)
        l = f.front_large(input_)
        return Fuzzifier.to_level(s, m, l)

    def side_small(self, input_):
        if input_ < 5:
            return 1
        elif input_ < 7:
            return (7 - input_)/2
        else:
            return 0

    def side_medium(self, input_):
        if 4 < input_ and input_ <= 8:
            return (input_-4)/4
        elif 8 < input_ and input_ <= 12:
            return (12-input_)/4
        else:
            return 0

    def side_large(self, input_):
        if 8 < input_ and input_ <= 16:
            return (input_-8)/8
        elif input_ > 16:
            return 1
        else:
            return 0

    def front_small(self, input_):
        if input_ < 5:
            return 1
        elif input_ < 10:
            return (10 - input_)/5
        else:
            return 0

    def front_medium(self, input_):
        if 14 < input_ and input_ <= 16:
            return (input_-14)/16
        elif 16 < input_ and input_ <= 18:
            return (18-input_)/16
        else:
            return 0

    def front_large(self, input_):
        if input_ > 30:
            return 1
        else:
            return 0


class Rules():
    def __init__(self):
        pass

    @staticmethod
    def apply(fl, f, fr):
        if fr == Level.SMALL:
            return -40
        if fl == Level.SMALL:
            return 40
        if fr == Level.MEDIUM and f == Level.SMALL:
            return -30
        if fl == Level.MEDIUM and f == Level.SMALL:
            return 30
        return 0
