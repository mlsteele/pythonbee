import re
from collections import namedtuple
from pprint import pprint

PROBLEMS_FILE = "problems.txt"

Problem = namedtuple('Problem', ['name', 'text'])

def read_problems_file(f):
    problems = []
    strip = lambda x: x.strip()
    for line in map(strip, f.readlines()):
        if line == "":
            # skip empty lines
            continue
        elif line.startswith("PROBLEM:"):
            # start new problem
            name = re.search("PROBLEM: (\w+)", line).group(1)
            problems.append(Problem(name=name, text=[]))
            continue
        else:
            # append line of problem description
            (name, text) = problems[-1]
            problems[-1] = Problem(name, text + [line])

    problems = [Problem(name=p.name, text='\n'.join(p.text)) for p in problems]
    problems = {p.name: p for p in problems}
    return problems

def load_problems():
    with open(PROBLEMS_FILE) as f:
        return read_problems_file(f)

if __name__ == "__main__":
    problems = load_problems()
    print("bee.py implementation not finished")
