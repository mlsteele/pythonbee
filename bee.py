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

    problems = {p.name: p for p in problems}
    return problems

def load_problems():
    with open(PROBLEMS_FILE) as f:
        return read_problems_file(f)

def make_entry_file(problem, path):
    with open(path, 'w') as f:
        f.write("# PROBLEM: {}\n".format(problem.name))
        comment = lambda line: "# {}\n".format(line)
        f.writelines(map(comment, problem.text))

if __name__ == "__main__":
    problems = load_problems()
    p = problems.values()[0]
    make_entry_file(p, "entry_{}.py".format(p.name))
    print("bee.py implementation not finished")
