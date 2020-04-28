import pytest
import json
import classes_jeden

lesson = """{
    "title": "python",
    "price": 3,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
    }"""

only_title = """{
    "title": "python"  
    }"""

class_field = """{
    "title": "python",
    "class": "Advert",
    "boo": "Tr"  
    }"""

class_field_dict = {"class": "Advert", "title": "python"}


def test_mappeddict_two_points():
    md = classes_jeden.MappedDict(lesson)
    assert md.location.address == "город Москва, Лесная, 7"


def test_mappeddict_dict():
    md = classes_jeden.MappedDict(json.loads(lesson))
    assert md.location.address == "город Москва, Лесная, 7"


@pytest.mark.skip(reason="implement __setitem__")
def test_mappeddict_changing_as_dict():
    md = classes_jeden.MappedDict(lesson)
    md['title'] = 'delphi'
    assert md['title'] == md.title


@pytest.mark.skip(reason="implement __setattr__")
def test_mappeddict_changing_as_obj():
    md = classes_jeden.MappedDict(lesson)
    md.title = 'delphi'
    assert md['title'] == md.title


def test_advert_two_points():
    lesson_ad = classes_jeden.Advert(lesson)
    assert lesson_ad.location.address == "город Москва, Лесная, 7"


def test_advert_price_lower_than_0():
    lesson_ad = classes_jeden.Advert(lesson)
    with pytest.raises(ValueError):
        lesson_ad.price = -1


def test_advert_price_nonexistent():
    ad = classes_jeden.Advert(only_title)
    assert 0 == ad.price


def test_advert_nonexistent_attr():
    ad = classes_jeden.Advert(only_title)
    with pytest.raises(AttributeError):
        print(ad.nonexistent_attr)


def test_advert_price_changing():
    lesson_ad = classes_jeden.Advert(lesson)
    assert lesson_ad.price == json.loads(lesson)['price']


def test_advert_price_nonexistent_title():
    with pytest.raises(AttributeError):
        ad = classes_jeden.Advert('''{}''')


def test_mappeddict_field_class():
    with pytest.raises(KeyError):
        md = classes_jeden.MappedDict(class_field)
