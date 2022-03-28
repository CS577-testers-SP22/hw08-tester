from subprocess import Popen, PIPE
from random import random, seed, shuffle
from tqdm import tqdm
from pprint import pprint
import json
import time

SMALL_TEST_COUNT = 100
MEDIUM_TEST_COUNT = 100
LARGE_TEST_COUNT = 10
SEED = 0
TEST_FILE = 'tests.json'

seed(SEED)

class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'{self.name}: {time.time() - self.t0:.2f}')

def generate_random_input(max_instances=500, max_elements=149, max_capacity=199, max_weight=100, max_value=199):
    '''returns a string that is valid input'''
    instances = int(random() * (max_instances)) + 1
    test = f'{instances}'

    for _ in range(instances):
        size = int(random() * (max_elements)) + 1
        capacity = int(random() * (max_capacity)) + 1

        test += f'\n{size} {capacity}'
        for i in range(size):
            weight = int(random() * max_weight) + 1
            value = int(random() * max_value) + 1
            test += f'\n{weight} {value}'

    return test + '\n'

def shell(cmd, stdin=None):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = p.communicate(input=stdin.encode() if stdin else None)
    return out.decode('utf8'), err.decode('utf8')

get_python = lambda testCase: shell('python3 knapsack.py', stdin=testCase)
get_cpp = lambda testCase: shell('./Knapsack', stdin=testCase)

print('Building:')
buildOutput, buildError = shell('make build')
if buildOutput:
    print(buildOutput)
if buildError:
    print('Error running `make build`:\n')
    print(buildError)
    exit()

tests = dict()

# manual tests
tests['given-test-0'] = {'input':'2\n1 3\n4 100\n3 4\n1 2\n3 3\n2 4\n', 'output':"0\n6\n"}

tests['edge-test-0'] = {'input':"1\n1 1\n1 20\n", 'output':"20\n"}

# random tests

for i in tqdm(range(SMALL_TEST_COUNT)):
    test = generate_random_input(max_instances=1, max_elements=10, max_capacity=10, max_weight=10, max_value=10)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'small-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(MEDIUM_TEST_COUNT)):
    test = generate_random_input(max_instances=10, max_elements=20, max_capacity=20, max_weight=50, max_value=50)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'medium-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(LARGE_TEST_COUNT)):
    test = generate_random_input(max_instances=1000, max_elements=149, max_capacity=199, max_weight=100, max_value=199)
    # test = generate_random_input(max_instances=100, max_elements=2000, max_start=1000 - 1, max_end=1000, max_value=10**4)
    # with Timer('python'):
    python, p_err = get_python(test)
    # with Timer('c'):
    cpp, c_err1 = get_cpp(test)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        # print(f'Input\n{test}')
        exit()
    tests[f'large-test-{i}'] = {'input':test, 'output':python}

# pprint(tests)
with open(TEST_FILE, 'w+') as f:
    json.dump(tests, f, indent=4)
