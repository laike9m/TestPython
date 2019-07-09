"""doc

docdoc
"""

import tokenize
from pprint import pprint
import sys
import inspect
import io
import token
import tokenize
from tokenize import TokenInfo


print(sys.version_info)


def f():
    y = {
        "longlonglonglong": 1,
        "longlonglonglonglong": 2,
        "longlonglonglonglonglong": 3,
    }


def _tokenize_string(s):
    return tokenize.tokenize(io.BytesIO(s.encode("utf-8")).readline)


source_str = inspect.getsource(f.__code__)

toks = list(_tokenize_string(source_str))  # assuming no exception.
# Note that lineno in lnotab starts at 0, while in tokens it starts at 1

# Step 1. Group toks by logical lines.
size = len(toks)
i = logical_line_start = 1  # skips first element token.ENCODING
groups = []
while i < size:
    if toks[i].type == token.NEWLINE:
        groups.append(toks[logical_line_start : i + 1])
        logical_line_start = i + 1
    i += 1

pprint(list(_tokenize_string(inspect.getsource(sys._getframe().f_code))))
