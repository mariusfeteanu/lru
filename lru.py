def _make_key(*args, **kwargs):
    all_args = [str(arg) for arg in args]
    all_args += [str(arg) + '=' + str(value) for arg, value in kwargs.items()]
    return '|'.join(all_args)


class DoubleLinked:
    def __init__(self, prv, nxt, key):
        self.prv = prv
        self.nxt = nxt
        self.key = key


class CacheEntry:
    def __init__(self, value, position):
        self.value = value
        self.position = position


class LRUCache:
    def __init__(self, get_from_origin, max_size=1024):
        if max_size == 0:
            raise NotImplementedError()
        if max_size < 0:
            raise ValueError()

        # keep separate size counter, to save going over the list
        self.size = 0
        self.max_size = max_size
        # the function to call
        self._get_from_origin = get_from_origin

        # the values to cache
        self._cache = {}
        self._most_recent = None
        self._least_recent = None

    @property
    def full(self):
        return self.size == self.max_size

    def get(self, *args, **kwargs):
        if not args and not kwargs:
            raise ValueError()

        key = _make_key(*args, **kwargs)
        if key in self._cache:
            return self._hit(key)
        return self._miss(key, *args, **kwargs)

    def _hit(self, key):
        self._bump_cached(key)
        return self._cache[key].value

    def _miss(self, key, *args, **kwargs):
        value = self._get_from_origin(*args, **kwargs)

        if not self._most_recent:
            self._bump_init(key)
        else:
            self._bump_new(key)

        self._set(key, value)

        return value

    def _bump_init(self, key):
        self._most_recent = DoubleLinked(nxt=None, prv=None, key=key)
        self._least_recent = self._most_recent
        self.size = 1

    def _bump_new(self, key):
        self._bump(key)

        # remove oldest entry
        # this is the entire reason for the linked list business
        if self.full:
            old_last = self._least_recent
            new_last = old_last.prv
            new_last.nxt = None
            self._least_recent = new_last
            self._remove(old_last.key)
        else:
            self.size += 1

    def _bump_cached(self, key):
        self._bump(key)
        self._remove_old_position(key)

    def _remove_old_position(self, key):
        old_position = self._cache[key].position

        if not old_position.prv:
            return  # we are already the most recent

        old_position.prv.nxt = old_position.nxt

        if old_position.nxt:  # if we're not the last
            old_position.nxt.prv = old_position.prv
        else:
            self._least_recent = old_position.prv

        self._cache[key].position = self._most_recent

    def _bump(self, key):
        old_first = self._most_recent
        new_first = DoubleLinked(nxt=old_first, prv=None, key=key)
        old_first.prv = new_first
        self._most_recent = new_first

    def _set(self, key, value):
        self._cache[key] = CacheEntry(value, self._most_recent)

    def _remove(self, key):
        del self._cache[key]

    def __repr__(self):
        if not self._most_recent:
            return '[ | ]'
        current = self._most_recent
        keys = [current.key]
        while current.nxt:
            current = current.nxt
            keys.append(current.key)
        return '[ ' + (' | '.join(keys)) + ' ]'

    def __len__(self):
        return self.size


class cache:  # pylint: disable=invalid-name
    def __init__(self, max_size):
        assert isinstance(max_size, int)
        self.max_size = max_size

    def __call__(self, func):
        lru = LRUCache(func, max_size=self.max_size)

        def cached_f(*args, **kwargs):
            return lru.get(*args, **kwargs)
        return cached_f
