import timeit
import random
import hashlib
import functools

from lru import cache, LRUCache

EXAMPLES_FILE = 'data/pageviews'

# randomly access the first n rows, ten times each, and calculate a hash of the content
# the more innefficient the better
def get_row(file_name, row_number):
    with open(file_name, 'rt') as f:
        for line in f:
            if row_number == 0:
                return line
            row_number -= 1

def get_row_hash(file_name, row_number):
    row_content = get_row(file_name, row_number)
    return hashlib.md5(row_content.encode('utf-8')).hexdigest()

def access_rows(file_name, n, how):
    iter_count = n*10
    while iter_count > 0:
        iter_count -= 1
        row_number = random.randint(0, n-1)
        how(file_name, row_number)

ROWS_TO_ACCESS = 500
ROWS_TO_CACHE = int(.50*ROWS_TO_ACCESS)
PASSES = 20

print('>> No cache: ')
raw_perf = timeit.timeit(f'access_rows(EXAMPLES_FILE, {ROWS_TO_ACCESS}, how=get_row_hash)', number=PASSES, globals=globals())
print(f'{raw_perf*1000:.{3}f} miliseconds.')


@functools.lru_cache(ROWS_TO_CACHE)
def get_row_hash_python_cache(file_name, row_number):
    return get_row_hash(file_name, row_number)

print('>> Python libs cache: ')
raw_perf_cache = timeit.timeit(f'access_rows(EXAMPLES_FILE, {ROWS_TO_ACCESS}, how=get_row_hash_python_cache)', number=PASSES, globals=globals())
print(f'{raw_perf_cache*1000:.{3}f} miliseconds.')


my_cache = LRUCache(get_row_hash, ROWS_TO_CACHE)
def get_row_hash_cache(file_name, row_number):
    return my_cache.get(file_name, row_number)

print('>> This cache (raw): ')
raw_perf_cache = timeit.timeit(f'access_rows(EXAMPLES_FILE, {ROWS_TO_ACCESS}, how=get_row_hash_cache)', number=PASSES, globals=globals())
print(f'{raw_perf_cache*1000:.{3}f} miliseconds.')


@cache(ROWS_TO_CACHE)
def get_row_hash_cache_dec(file_name, row_number):
    return get_row_hash(file_name, row_number)

print('>> This cache (decorator): ')
raw_perf_cache = timeit.timeit(f'access_rows(EXAMPLES_FILE, {ROWS_TO_ACCESS}, how=get_row_hash_cache_dec)', number=PASSES, globals=globals())
print(f'{raw_perf_cache*1000:.{3}f} miliseconds.')
