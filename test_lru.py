# pylint: disable=protected-access,trailing-whitespace
import pytest

from lru import LRUCache, cache


EXAMPLE = {'a': 123,
           'b': 'c',
           'c': 123456,
           'd': 765432,
           'e': 7981454,
           'f': 'dnsaj34dd',
           'g': [1, 2, 3]}


def get_something(key):
    return EXAMPLE[key]


def test_base_cache():
    """
    Check basic cache behaviour:
    - new requests up to the limit increase the size
    - requests after the limit is reached do not increase the size
    """
    base_cache = LRUCache(get_something, max_size=2)

    assert base_cache.get('a') == get_something('a')
    assert base_cache.size == 1
    assert base_cache.get('b') == get_something('b')
    assert base_cache.size == 2
    assert base_cache.get('c') == get_something('c')
    assert base_cache.size == 2


def test_base_repeat():
    """
    Check that repeated access of the same key don't count towards the limit
    """
    base_cache = LRUCache(get_something, max_size=2)

    base_cache.get('a')
    base_cache.get('a')
    base_cache.get('a')
    assert base_cache.size == 1


def test_common_cases_1():
    base_cache = LRUCache(get_something, max_size=3)
    base_cache.get('a')
    base_cache.get('b')
    base_cache.get('c')
    base_cache.get('a')
    base_cache.get('a')

    assert str(base_cache) == '[ a | c | b ]'


def test_common_cases_2():
    base_cache = LRUCache(get_something, max_size=3)
    base_cache.get('a')
    base_cache.get('b')
    base_cache.get('c')
    base_cache.get('a')
    base_cache.get('a')
    base_cache.get('b')
    base_cache.get('d')

    assert str(base_cache) == '[ d | b | a ]'


def test_common_cases_3():
    base_cache = LRUCache(get_something, max_size=3)
    base_cache.get('a')
    base_cache.get('b')
    base_cache.get('g')
    base_cache.get('f')
    base_cache.get('c')
    base_cache.get('a')
    base_cache.get('a')
    base_cache.get('b')
    base_cache.get('d')

    assert str(base_cache) == '[ d | b | a ]'


def test_empty_cache():
    base_cache = LRUCache(get_something, max_size=3)
    assert str(base_cache) == '[ | ]'
    assert not base_cache


def test_invalid_cache():
    with pytest.raises(NotImplementedError):
        LRUCache(get_something, max_size=0)

    with pytest.raises(ValueError):
        LRUCache(get_something, max_size=-1)


def test_decorator_single_key():
    @cache(10)
    def increment(i):
        return i + 1

    assert increment(3) == 4
    assert increment(2) == 3


def test_decorator_multiple_key():
    @cache(10)
    def add(i, j):
        return i + j

    assert add(3, 2) == 5
    assert add(2, 1) == 3


def test_decorator_no_key():
    @cache(10)
    def nothing():
        return 'nope'

    with pytest.raises(ValueError):
        nothing()


def test_decorator_check_actual_cache():
    things = []
    @cache(2)
    def append_side_effect(i):
        things.append(i)

    append_side_effect(3)
    assert things == [3]

    append_side_effect(2)
    assert things == [3, 2]

    append_side_effect(1)
    assert things == [3, 2, 1]

    append_side_effect(1)
    assert things == [3, 2, 1]

    append_side_effect(2)
    assert things == [3, 2, 1]

    append_side_effect(4)
    assert things == [3, 2, 1, 4]

    append_side_effect(3)
    assert things == [3, 2, 1, 4, 3]


def test_base_cache_limits():
    @cache(5)
    def c5fib(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return c5fib(n-1) + c5fib(n-2)

    c5fib(20)
