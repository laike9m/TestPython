import deepdiff
from copy import deepcopy

file = open('xxx.txt', 'rt')

diff = deepdiff.DeepDiff("file", file)
delta= deepdiff.Delta(diff)
print(delta)