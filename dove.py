#!/usr/bin/env python3

"""Dove v0.0.1

Dove is a tool for quickly managing projects in a shell like an IDE.

Usage:
    `dove [flags] <command or option> [arguments]`

Commands:
    build, -b, --build       compile packages and dependencies
    analyse, -a, --analyse   checks for any errors or warnings in file(s)
    clean, -c, --clean       remove compiled/object files and cached files
    doc, -d, --doc           show documentation for an object in file
    run, -r, --run           run program and compile if required
    walk, -w, --walk         compile and run program
    test, -t, --test         run tests
    env, -e, --env           print Dove's workspace environment information
    reset, -r, --reset       reset Dove's preferences & environment to default
    tree, -l, --tree, --list list project files & directories as tree
    ext, -ext, --ext         manage extensions
    info, -i, --info         print Dove's information
    update, -u, --update     update dove and extensions
    switch, -s, --switch     check or switch Dove's current language mode
    fix, -f, --fix           fixes Dove's preferences
    -v, --verbose            increase output verbosity

Use \"dove help <command>\" for more information about a command."""

from os import mkdir, path, getcwd, environ
import fcntl
import argparse
import yaml
from sys import argv
from functools import partial

# Globals
DOVE_CACHE_PATH = "{}/.dove".format(getcwd())
DOVE_LOCK_FILE = "{}/dove.lock".format(DOVE_CACHE_PATH)
DOVE_CONFIG_FILE = "{}/dove_config.yaml".format(DOVE_CACHE_PATH)
SUPPORTED_LANGUAGE_MODES = ("Auto", "Java", "C++")
CURRENT_MODE = "Auto"
DEBUG_MODE = False
VERBOSE_ON = False
PCLI = (None, None)
command_args = {'build': '   build, -b, --build       compile packages and dependencies', 'analyse': '    analyse, -a, --analyse   checks for any errors or warnings in file(s)', 'clean': '    clean, -c, --clean       remove compiled/object files and cached files', 'doc': '    doc, -d, --doc           show documentation for an object in file', 'run': '    run, -r, --run           run program and compile if required', 'walk': '    walk, -w, --walk         compile and run program', 'test': '    test, -t, --test         run tests', 'env': "    env, -e, --env           print Dove's workspace environment information",
                'reset': "    reset, -r, --reset       reset Dove's preferences & environment to default", 'tree': '    tree, -l, --tree, --list list project files & directories as tree', 'extensions': '    ext, -ext, --ext         manage extensions', 'info': "    info, -i, --info         print Dove's information", 'update': '    update, -u, --update     update dove and extensions', 'switch': "    switch, -s, --switch     check or switch Dove's current language mode", 'fix': "    fix, -f, --fix                fixes Dove's preferences", 'help': __doc__}
__usage__ = """\n    `dove [flags] <command or option> [arguments]`

Commands:
    build, -b, --build       compile packages and dependencies
    analyse, -a, --analyse   checks for any errors or warnings in file(s)
    clean, -c, --clean       remove compiled/object files and cached files
    doc, -d, --doc           show documentation for an object in file
    run, -r, --run           run program and compile if required
    walk, -w, --walk         compile and run program
    test, -t, --test         run tests
    env, -e, --env           print Dove's workspace environment information
    reset, -r, --reset       reset Dove's preferences & environment to default
    tree, -l, --tree, --list list project files & directories as tree
    ext, -ext, --ext         manage extensions
    info, -i, --info         print Dove's information
    update, -u, --update     update dove and extensions
    switch, -s, --switch     check or switch Dove's current language mode
    fix, -f, --fix           fixes Dove's preferences
    -v, --verbose            increase output verbosity

Use \"dove help <command>\" for more information about a command."""

# Actions


class DoveAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(DoveAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        dprint('namespace: %r, values: %r, option_string: %r' %
               (namespace, values, option_string))
        setattr(namespace, self.dest, values)


class HelpAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(HelpAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, val, option_string=None):
        # print('2: %r %r %r' % (namespace, values, option_string))
        if val == 'help':
            print(command_args[val])
        elif val in command_args.keys():
            help_info = command_args[val]
            help_message = "{0}'s usage:\n    \"dove [flags] {0} [arguments if required]\ninfo:\n{1}".format(
                val, help_info)
            print(help_message)
            exit(0)
        else:
            print(__doc__)
            print("{}: error: unrecognized argument(s): {}".format(
                argv[0], val))
            exit(1)
        setattr(namespace, self.dest, val)
# !


def debug_state():
    if DEBUG_MODE:
        state_vars = {"DOVE_CACHE_PATH": DOVE_CACHE_PATH,
                      "DOVE_LOCK_FILE": DOVE_LOCK_FILE,
                      "DOVE_CONFIG_FILE": DOVE_CONFIG_FILE,
                      "SUPPORTED_LANGUAGE_MODES": SUPPORTED_LANGUAGE_MODES,
                      "CURRENT_MODE": CURRENT_MODE,
                      "DEBUG_MODE": DEBUG_MODE,
                      "VERBOSE_ON": VERBOSE_ON,
                      "PCLI": PCLI}
        for i in state_vars.keys():
            dprint('{}: {}'.format(i, state_vars[i]),)


def print_help(val):
    if val == 'help':
        print(__doc__)
    elif val in command_args.keys():
        help_info = command_args[val]
        help_message = "{0}'s usage:\n    \"dove [flags] {0} [arguments if required]\ninfo:\n{1}".format(
            val, help_info)
        print(help_message)
        exit(0)
    else:
        print(__doc__)
        exit(1)


def vprint(*args, senderDef=[]):
    """Prints only when verbose output is on"""
    sender = ''
    if senderDef != []:
        sender = "[{}]".format('.'.join(senderDef))
    if VERBOSE_ON:
        try:
            print(sender, ''.join(args))
        except TypeError:
            print(sender, args)


def dprint(*args):
    """Prints only in debug mode"""
    if DEBUG_MODE:
        try:
            print(''.join(args))
        except TypeError:
            print(args)


class EnVars:
    def getEnv(key):
        value, sign = environ.get(key, 'UNSET'), 1
        if value.startswith('-'):
            value, sign = value[1:], -1
        if value.isdigit():
            return sign * int(value)
        else:
            try:
                return sign * float(value)
            except ValueError:
                if sign == -1:
                    return "-"+value
                else:
                    return value

    def setEnv(key, value):
        environ[key] = str(value)


def acquireLock():
    with open(DOVE_LOCK_FILE, 'r+') as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            dprint("[acquireLock] Lock acquired")
            # Do stuff
        except BlockingIOError:
            print("Dove is already running locally..\nexiting")
            exit(1)


def handle_commands():
    """
    add -- before commands for argparser
    """

    i = 0
    while i < len(argv):
        if argv[i] in ["--help", "-h", "--h"]:
            argv[i] = "help"
        if argv[i] in command_args.keys():
            argv[i] = "--"+argv[i]
            i += 2
            continue
        i += 1


class YamlControl():
    def create_config():
        comment1 = "# Specifies Dove's language mode\n"
        config1 = {
            'current mode': 'auto',
        }
        comment2 = "# Main file to load automatically (if blank then it'll be chosen\n# based on language or parameters)\n"
        config2 = {
            'main file': None,
        }
        comment3 = "# Project directory\n"
        config3 = {
            'project directory': '.',
            'project name': None,
        }
        with open(DOVE_CONFIG_FILE, 'w+') as fstreamW:
            fstreamW.write(comment1)
            yaml.dump(config1, fstreamW, default_flow_style=False,
                      allow_unicode=True)
            fstreamW.write(comment2)
            yaml.dump(config2, fstreamW, default_flow_style=False,
                      allow_unicode=True)
            fstreamW.write(comment3)
            yaml.dump(config3, fstreamW, default_flow_style=False,
                      allow_unicode=True)

    def handle_config():
        isEmpty = False
        if path.exists(DOVE_CONFIG_FILE):
            with open(DOVE_CONFIG_FILE, 'r') as fstreamR:
                # if empty then write config in config.yaml
                try:
                    data_loaded = yaml.safe_load(fstreamR)
                except yaml.YAMLError as exc:
                    isEmpty = True
                if data_loaded == None or data_loaded == '':
                    isEmpty = True
            if isEmpty:
                YamlControl.create_config()
            with open(DOVE_CONFIG_FILE, 'r') as fstreamR:
                # if not empty then replace config in memory
                data_loaded = yaml.safe_load(fstreamR)
                dprint(data_loaded)
        else:
            YamlControl.create_config()
            YamlControl.handle_config()
        vprint('configs loaded', senderDef=["YamlControl", "handle_config"])


def askPrompt(message, onYes, onNo) -> None:
    """
    # askPrompt

    ## Asks for yes or no prompts

    For prameters `onYes` and `onNo`, either pass exit, or a method with no arguments or a partial application of method
    """
    while True:
        yn: str = input(message)
        fyn = yn[0]
        if fyn in ["Y", "y"]:
            return ifYes()
        elif fyn in ["N", "n"]:
            return ifNo()
        else:
            print("Please answer yes or no (Y/n). ")


def cli_args() -> tuple:
    """
    # cli_args

    # Parses the command-line arguments
    """
    handle_commands()
    # using argparse
    parser = argparse.ArgumentParser(usage=__usage__, add_help=False)
    parser.add_argument("-b", "--build", dest="build", metavar="build",
                        help="compile packages and dependencies", action=DoveAction)
    parser.add_argument("-a", "--analyse", "-check", "--check", dest="analyse", metavar="analyse",
                        help="checks for any errors or warnings in file(s)", action=DoveAction)
    parser.add_argument("-c", "--clean", dest="clean", metavar="clean",
                        help="remove compiled/object files and cached files", action=DoveAction)
    parser.add_argument("-doc", "--doc", dest="doc", metavar="doc",
                        help="show documentation for an object in file", action=DoveAction)
    parser.add_argument("-e", "--env", dest="env",
                        help="print Dove's workspace environment information", action='store_true')
    parser.add_argument("-reset", "--reset", dest="reset", metavar="reset",
                        help="reset Dove's preferences & environment to default", action=DoveAction)
    parser.add_argument("-l", "--list", "-tree", "--tree", dest="list", metavar="list",
                        help="list project files & directories as tree", action=DoveAction)
    parser.add_argument("-r", "--run", dest="run", metavar="run",
                        help="run program and compile if required", action=DoveAction)
    parser.add_argument("-w", "--walk", dest="walk", metavar="walk",
                        help="compile and run program", action=DoveAction)
    parser.add_argument("-t", "--test", dest="test",
                        metavar="test", help="run tests", action=DoveAction)
    parser.add_argument("-p", "--profile", dest="profile", metavar="profile",
                        help="run program in profile mode", action=DoveAction)
    parser.add_argument("-ext", "--ext", dest="extension",
                        help="manage extensions", action='store_true')
    parser.add_argument("-s", "--switch", dest="switch", metavar="switch",
                        help="check or switch Dove's current language mode", action=DoveAction)
    parser.add_argument("-i", "--info", dest="info",
                        help="print Dove's information", action='store_true')
    parser.add_argument("-u", "--update", dest="update",
                        help="update Dove", action='store_true')
    parser.add_argument("-f", "--fix", dest="fix",
                        help="fixes Dove's global & workspace preferences", action='store_true')
    parser.add_argument("-v", "--verbose", dest="verbose",
                        help="increase output verbosity", action='store_true')
    parser.add_argument("-dev", dest="dev",
                        help="run developer's test", action='store_true')
    parser.add_argument("--help", metavar="help", dest="help",
                        help="show this message", default='help', action=HelpAction)
    args = parser.parse_args()
    dprint(args)
    if args.verbose:
        global VERBOSE_ON
        VERBOSE_ON = True
    return (parser, args)


def main():
    # Tab completion & Parsing arguments
    global PCLI
    global VERBOSE_ON
    global DEBUG_MODE
    PCLI = cli_args()
    VERBOSE_ON = PCLI[1].verbose
    DEBUG_MODE = PCLI[1].dev
    # Check if dove temp folder exists, if not then creates one
    if not path.exists(DOVE_CACHE_PATH):
        mkdir(DOVE_CACHE_PATH)
    # Check if config file exists, if doesn't then add one
    YamlControl.handle_config()
    # getting and setting environment & global variables based on config


if __name__ == "__main__":
    main()
    debug_state()
