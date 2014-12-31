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
import os.path
import traceback
from collections import namedtuple
from importlib import import_module
import blessings
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

def get_problem_or_die(probname, problems):
        p = problems.get(probname)
        if not p:
            print "No such problem: '{}'".format(probname)
            raise SystemExit
        return p

def make_entry_file(problem, path):
    with open(path, 'w') as f:
        f.write("# PROBLEM: {}\n".format(problem.name))
        comment = lambda line: "# {}\n".format(line)
        f.writelines(map(comment, problem.text))

def entry_filepath(probname, player):
    return "entries/{}_{}.py".format(probname, player)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    problems = load_problems()
    term = blessings.Terminal()

    if arguments['list']:
        print "Problems loaded from: {}".format(PROBLEMS_FILE)
        for probname in problems:
            print probname

    elif arguments['start']:
        player = arguments['<player>']
        probname = arguments['<problem>']
        if not probname:
            raise NotImplementedError("'Start' on randomized problem not implemented")
        p = get_problem_or_die(probname, problems)

        entryfile = entry_filepath(p.name, player)
        make_entry_file(p, entryfile)
        print "Created entry for '{}': {}".format(p.name, entryfile)

    elif arguments['test']:
        player = arguments.get('<player>')
        probname = arguments.get('<problem>')
        entryfile = arguments.get('<file>')

        if player and probname:
            entryfile = entry_filepath(probname, player)
        elif entryfile:
            raise NotImplementedError("'Test' not implemented for files")
        elif arguments['--last']:
            raise NotImplementedError("'Test' not implemented for last modified")

        # convert entryfile into entrymodule to import
        entry_module = entryfile.strip(".py").replace('/', '.')

        testfile = "tests/" + probname + ".py"
        if not os.path.isfile(testfile):
            print "No test exists for '{}'".format(probname)
            print "To add a test, create: {}".format(testfile)
            raise SystemExit

        if not os.path.isfile(entryfile):
            print "Entry file does not exist: {}".format(entryfile)
            raise SystemExit

        print "Testing:\n  {}\n  {}".format(entry_module, testfile)
        print ""

        # import test function from test file
        test = import_module("tests." + probname).test
        # import entry module (could fail for syntax)
        try:
            entry = import_module(entry_module)
        except Exception as e:
            print term.red("Syntax Error")
            print term.yellow(traceback.format_exc())
            print term.red("Test Failed")
            raise SystemExit

        # run test
        try:
            test(entry)
        except Exception as e:
            print term.red("Runtime Error")
            print term.yellow(traceback.format_exc())
            print term.red("Test Failed")
            raise SystemExit

        print term.green("Test Passed")

    elif arguments['wipe']:
        raise NotImplementedError("'Wipe' not implemented")
