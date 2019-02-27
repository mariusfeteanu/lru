import cProfile
import random
import hashlib

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

my_cache = LRUCache(get_row_hash, ROWS_TO_CACHE)
def get_row_hash_cache(file_name, row_number):
    return my_cache.get(file_name, row_number)

access_rows(EXAMPLES_FILE, ROWS_TO_ACCESS, how=get_row_hash_cache)

cProfile.runctx(f'access_rows(EXAMPLES_FILE, {ROWS_TO_ACCESS}, how=get_row_hash_cache)', globals=globals(), locals=None)
