import requests
import pytest

from lesson7.task1 import Utils


class TestRunRandom:

    @pytest.mark.parametrize('index', range(5))
    def test_common(self, all_breed_sub_breeds, url_random_response, index):
        assert url_random_response.status_code == 200, 'Wrong status code'

        rec = url_random_response.json()
        assert isinstance(rec, dict), 'Response is not dict'

        for key in ('message', 'status'):
            assert key in rec, f'Wrong response structure - {key} is not found'

        link: str = rec.get('message')
        assert isinstance(link, str), 'Link is not str'
        Utils.check_img_link(link, all_breed_sub_breeds)
        Utils.check_img_by_link(link)

    def test_common_count(self, all_breed_sub_breeds, p_f_random_count):
        resp, cnt, expected_cnt = p_f_random_count
        rec = Utils.common_response_check(resp)
        links: list = rec.get('message')
        Utils.common_count_check(links, expected_cnt)
        Utils.common_links_check(all_breed_sub_breeds, links)


class TestByBreed:

    def test_common(self, all_breed_sub_breeds, random_breed_response):
        rec = Utils.common_response_check(random_breed_response)

        links: list = rec.get('message')
        assert isinstance(links, list), 'Message is not list'
        ln = len(links)
        assert ln > 0, 'Message is empty'

        Utils.common_links_check(all_breed_sub_breeds, links)

    def test_random(self, all_breed_sub_breeds, random_breed_response_single):
        rec = Utils.common_response_check(random_breed_response_single)

        link: str = rec.get('message')
        assert isinstance(link, str), 'Message is not str'
        Utils.check_img_link(link, all_breed_sub_breeds)
        Utils.check_img_by_link(link)

    def test_random_count(self, all_breed_sub_breeds, p_f_random_count_by_breed):
        resp, breed, cnt, expected_cnt, mode = p_f_random_count_by_breed
        rec = Utils.common_response_check(resp)
        links: list = rec.get('message')
        Utils.common_count_check(links, expected_cnt, mode=mode)
        Utils.common_links_check(all_breed_sub_breeds, links, breed_=breed)


class TestNegative:

    @pytest.mark.parametrize('url, status, msg, code',
                             tuple(Utils.parametrize_breed_not_found('1', '_'))
                             + tuple(Utils.parametrize_route_not_found())
    )
    def test_common(self, url, status, msg, code):
        Utils.common_wrong_response_check(requests.request('get', url), status, msg, code)


if __name__ == '__main__':
    pass