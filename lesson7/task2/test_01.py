import requests
import pytest

from lesson7.task2 import Utils, Response


class TestRunByCity:

    @pytest.mark.parametrize('f_by_city, expected', (
            ('san_diego', 'san diego'),
            ('san%20diego', 'san diego'),
            ('SAN_DIEGO', 'san diego'),
            ('Alameda', 'alameda')
    ), indirect=['f_by_city'])
    def test_common(self, f_by_city: requests.Response, expected):
        assert f_by_city.status_code == 200, 'Wrong status code'

        breweries = f_by_city.json()
        assert isinstance(breweries, list), 'Response is not list'
        assert len(breweries) > 0, 'List is empty'

        for brewery in breweries:
            assert isinstance(brewery, dict), f'Brewery is not dict'
            city_: str = brewery.get('city')
            assert expected.lower() in city_.lower(), 'Wrong city'

    @pytest.mark.parametrize('ind', range(10))
    def test_by_examples(self, f_random_city: str, ind: int):
        r = Response.by_city(Utils.normalize(f_random_city))
        assert r.status_code == 200, 'Wrong status code'

        breweries = r.json()
        assert isinstance(breweries, list), 'Response is not list'
        assert len(breweries) > 0, 'List is empty'

        f_random_city = f_random_city.lower()
        found = False
        for brewery in breweries:
            assert isinstance(brewery, dict), f'Brewery is not dict'
            city_: str = brewery.get('city')
            if city_.lower() == f_random_city:
                found = True
                break

        assert found, 'City is not found'

    @pytest.mark.parametrize('f_by_city', 'sandiegoSANDIEGO', indirect=['f_by_city'])
    def test_sun_diego(self, f_by_city: requests.Response):
        assert f_by_city.status_code == 200, 'Wrong status code'

        breweries = f_by_city.json()
        assert isinstance(breweries, list), 'Response is not list'
        assert len(breweries) > 0, 'List is empty'

        found = False
        for brewery in breweries:
            assert isinstance(brewery, dict), f'Brewery is not dict'
            city_: str = brewery.get('city')
            if city_.lower() == 'san diego':
                found = True
                break

        assert found, 'San diego is not found'


class TestRunByDist:

    @pytest.mark.xfail(reason='Результат не отсортирован в порядке удаленности', raises=(AssertionError,))
    @pytest.mark.parametrize('ind', range(5))
    def test_common(self, f_random_dist, ind: int):
        longitude, latitude = f_random_dist
        r = Response.by_dist(longitude, latitude)
        assert r.status_code == 200, 'Wrong status code'

        breweries = r.json()
        assert isinstance(breweries, list), 'Response is not list'
        assert len(breweries) > 0, 'List is empty'

        in_order = True
        prev_dist = 0
        for brewery in breweries:
            assert isinstance(brewery, dict), f'Brewery is not dict'
            dist = Utils.calc_dist(longitude, latitude, brewery.get('longitude'), brewery.get('latitude'))
            if dist > prev_dist and prev_dist:
                in_order = False
                break

            prev_dist = dist

        assert in_order, 'Dist is not in order'


class TestRunByType:

    @pytest.mark.parametrize('ind', range(5))
    def test_common(self, f_random_type, ind: int):
        r = Response.by_type(f_random_type)
        assert r.status_code == 200, 'Wrong status code'

        breweries = r.json()
        assert isinstance(breweries, list), 'Response is not list'
        if len(breweries) > 0:
            return

        for brewery in breweries:
            assert isinstance(brewery, dict), f'Brewery is not dict'
            assert brewery.get('brewery_type') == f_random_type, f'Wrong type'

    @pytest.mark.parametrize('wrong_type', ('micr', '1', 'x'))
    def test_wrong_type(self, f_types_set, wrong_type: str):
        r = Response.by_type(wrong_type)
        assert r.status_code == 400, 'Wrong status code'

        rec = r.json()
        assert isinstance(rec, dict), 'Response is not dict'

        errors: list = rec.get('errors')
        assert isinstance(errors, list), 'Errors is not list'
        assert len(errors) == 1, 'Many errors'

        err: str = errors[0]
        err_start = 'Brewery type must include one of these types: ['
        err_end = ']'
        assert err.startswith(err_start) and err.endswith(err_end), 'Wrong error'
        types_ = set((s.strip().strip('"') for s in err[len(err_start): -len(err_end)].split(',')))
        assert types_ == f_types_set, 'Wrong type set'


if __name__ == '__main__':
    pass
