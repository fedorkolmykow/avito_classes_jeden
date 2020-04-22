import json


class ColorizeMixin:
    repr_color_code = 32     # green
    _escape_code = '\033'
    style = 1                # normal style
    back_color = 40          # white background
    @property
    def color(self):
        return f'{self._escape_code}[{self.style};{self.repr_color_code};{self.back_color}m'


class MappedDict(dict):
    def __init__(self, json_obj):
        decoded_json = json.loads(json_obj)
        super().__init__(decoded_json)
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

    def __repr__(self):
        return f"{self.color}{self.title} | {self.price} ₽"


if __name__ == "__main__":
    lesson_ad = Advert( """{
    "title": "python",
    "price": 3,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
    }""")
    print(lesson_ad)

