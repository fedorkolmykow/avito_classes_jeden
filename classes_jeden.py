import json
import keyword


def colorize(color, back_color, style):
    def _colorize(wrapped_func):
        def wrapper(*args, **kwargs):
            code = '\033['
            default_color = f'{code}0m'
            return f'{code}{style};{color};{back_color}m' + wrapped_func(*args, **kwargs) + f'{default_color}'
        return wrapper
    return _colorize


class ColorizeMixin:
    repr_color_code = 33     # green
    _escape_code = '\033'
    style = 1                # normal style
    back_color = 40          # black background

    @property
    def default_color(self):
        return f'{self._escape_code}[0m'

    @property
    def color(self):
        return f'{self._escape_code}[{self.style};{self.repr_color_code};{self.back_color}m'

    def __repr__(self):
        return self.color + super().__repr__() + self.default_color


class MappedDict(dict):
    def __init__(self, data):
        if not isinstance(data, dict):
            data = json.loads(data)
        super().__init__(data)

        print(self.__dict__)
        keywords = [x for x in self if x in keyword.kwlist]
        if keywords:
            raise KeyError("Python's key word as attribute")

        for item in self:
            if isinstance(self[item], dict):
                self[item] = MappedDict(json.dumps(self[item]))
            self.__dict__[item] = self[item]

    def __getattribute__(self, item):
        try:
            val = super().__getattribute__(item)
        except AttributeError:
            val = None
            __dict__ = super().__getattribute__('__dict__')
            __dict__[item] = val
        return val


class BaseAdvert:
    def __init__(self, mapping):
        md = MappedDict(mapping)
        if 'title' not in md:
            raise AttributeError('Advert has to receive attribute "title"')
        if 'price' in md:
            self._price = md['price']
        else:
            self.__dict__['_price'] = 0
        self.__dict__.update(md)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError('must be >= 0')
        self._price = new_price

    #@colorize(32, 40, 1)
    def __repr__(self):
        return f"{self.title} | {self.price} ₽"


class Advert(ColorizeMixin, BaseAdvert):
    pass


if __name__ == "__main__":
    lesson_ad = Advert("""{
    "title": "python",
    "price": 3,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
    }""")
    print()
    print(lesson_ad)
    print()
