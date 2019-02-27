## Pre-requisites
- Python 3.7
- Pipenv (if you're not using this, skip the init step below and roll your own with mkvirtualenv, pip install etc.)

## Steps to run:

- Initialize the virtual env etc.
```bash
make init
```

- Test that it works
```bash
make test
```

- Check performance. N.B. this does not use a good LRU use case, but it's enough to show the thing caches something.
```bash
make perf
```

- If not happy, profile it:
```bash
make profile
```
