"""
Python Bee

Usage:
  bee.py list
  bee.py start <player> [<problem>]
  bee.py test <player> <problem>
  bee.py test <file>
  bee.py test (-l | --last)
  bee.py wipe --all

Options:
  -h --help  Show this screen.
  start      List all available problems.
  start      Create a template for a contestant entry.
  test       Test a contestant entry.
  wipe       Delete all existing solutions
"""

import re
from collections import namedtuple
from pprint import pprint
from docopt import docopt

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

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print arguments, '\n'

    problems = load_problems()

    if arguments['list']:
        print "Problems loaded from: {}".format(PROBLEMS_FILE)
        for probname in problems:
            print probname
    elif arguments['start']:
        player = arguments['<player>']
        probname = arguments['<problem>']
        if not probname:
            raise NotImplementedError("'Start' on randomized problem not implemented")
        p = problems.get(probname)
        if not p:
            print "No such problem: '{}'".format(probname)
            raise SystemExit

        entryfile = "entries/{}_{}.py".format(p.name, player)
        make_entry_file(p, entryfile)
        print "Created entry for '{}': {}".format(p.name, entryfile)
    elif arguments['test']:
        raise NotImplementedError("'Test' not implemented")
    elif arguments['wipe']:
        raise NotImplementedError("'Wipe' not implemented")
