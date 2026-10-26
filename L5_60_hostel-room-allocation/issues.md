# Lab 5 Static Code Analysis Issues

Name: Aniyath Amrita Pradeep

Section: H

SRN: PES2UG24CS919

File analysed: hostel_allocation.py


## Summary of results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.84/10 | 10.00/10 (update with your actual score) |
| Bandit | 5 issues (1 High, 2 Medium, 2 Low) | No issues identified |
| Flake8 | 20 warnings | 0 warnings |

Reports are stored in `reports/before/` and `reports/after/`.

## Bandit issues (commit 1)

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---|---|---|
| Unsafe YAML load (B506) | Security, High | 21 | `yaml.load` with `yaml.Loader` can instantiate arbitrary objects | Switched to `yaml.safe_load` |
| Flask debug=True (B201) | Security, High | 80 | Exposes the Werkzeug debugger, which allows arbitrary code execution | Set `debug=False` |
| Insecure logging listen (B612) | Security, Medium | 72 | `logging.config.listen` executes configs received over a socket | Removed the unused function and the `logging.config` import |
| Hardcoded password (B106) | Security, Low | 66 | Database password written in source | Read from the `WARDEN_DB_PASSWORD` environment variable |
| Weak PRNG (B311) | Security, Low | 56 | `random.sample` is not cryptographically secure | Used `secrets.SystemRandom().sample` |
| Reflected XSS in `/room` | Security, found manually | 76-77 | Query parameter concatenated straight into HTML | Escaped with `markupsafe.escape` |

## Pylint issues (commit 2)

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---|---|---|
| Mutable default argument (W0102) | Bug | 29 | `preferred=[]` is shared across calls | Default to `None` and build the list inside the function |
| Capacity check off by one | Bug | 34 | `>` let a third student into a capacity 2 room | Changed to `>=` |
| Unused argument gender (W0613) | Bug | 29 | Gender was ignored, so a female student got a male block room | Skip rooms whose gender does not match |
| Duplicate allocation | Bug | 29-38 | S1 was allocated a second room | Return the existing room if already allocated |
| Vacate leaves bed occupied | Bug | 41-45 | Student removed from allocations but not from room occupants | Also remove the student from `occupants` |
| Wrong priority order | Bug | 53 | Juniors came first | Added `reverse=True` |
| Vacant beds undercount | Bug | 58-63 | Only fully empty rooms were counted | Sum capacity minus occupants for every room |
| Missing waitlist return | Bug | 39 | Function fell through without an explicit return | Added `return None` |
| Type comparison (C0123) | Style | 30 | `type(year) != int` | Used `isinstance` |
| Unused imports (W0611) | Style | 1-2 | `os` and `sys` imported but unused | Removed `sys`; `os` is now used for the environment variable |
| Naming (C0103) | Style | 20-79 | camelCase function names | Renamed to snake_case |
| Missing docstrings (C0114, C0116) | Style | 1 and every function | No documentation | Added module and function docstrings |
| Dict iteration (C0206) | Style | 60 | Looping over keys then indexing | Used `.values()` and `.items()` |
| Line too long (C0301) | Style | 95 | 116 characters | Moved the sorted result into a variable |

## Flake8 issues (commit 3)

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---|---|---|
| E302 expected 2 blank lines | Style | 20, 29, 41, 47, 52, 55, 58, 65, 68, 71, 74, 79, 82 | One blank line between top-level definitions | Two blank lines before each definition |
| E305 blank lines after definition | Style | 101 | Top-level code directly after a function | Two blank lines before the `__main__` guard |
| E501 line too long | Style | 25, 66, 95 | Lines over 79 characters | Wrapped the dict literal and shortened the print line |
| E721 type comparison | Style | 30 | Comparing types directly | Used `isinstance` (done in commit 2) |
| F401 unused imports | Style | 1, 2 | `os` and `sys` unused | Handled in commits 1 and 2 |

## Commits

1. Fix Bandit findings
2. Fix Pylint findings
3. Fix Flake8 findings
4. Add issues documentation
