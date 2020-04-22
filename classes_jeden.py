import json


class ColorizeMixin:
    repr_color_code = 32     # green
    _escape_code = '\033'
    style = 1                # normal style
    back_color = 40          # black background
    default_color = f'{_escape_code}[0m'
    color = f'{_escape_code}[{style};{repr_color_code};{back_color}m'

    @staticmethod
    def colorize(wrapped_func):
        def wrapper(*args, **kwargs):
            self = args[0]
            return self.color + wrapped_func(*args, **kwargs) + self.default_color
        return wrapper


class MappedDict(dict):
    def __init__(self, data):
        if not isinstance(data, dict):
            data = json.loads(data)
        super().__init__(data)
        for item in self:
            if isinstance(self[item], dict):
                self[item] = MappedDict(json.dumps(self[item]))
            __dict__ = super().__getattribute__('__dict__')
            __dict__[item] = self[item]


class Advert(ColorizeMixin):
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

    @ColorizeMixin.colorize
    def __repr__(self):
        return f"{self.title} | {self.price} ₽"


if __name__ == "__main__":
    lesson_ad = Advert( """{
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
