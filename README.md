# Dove

Dove is a tool for quickly managing projects in a shell like an IDE

## Usage

Use this pattern when using in a shell:

```shell
dove [options] <command> [arguments]
```

## Available Commands

1. build, -b, --build       compile packages and dependencies
1. analyse, -a, --analyse   checks for any errors or warnings in file(s)
1. clean, -c, --clean       remove compiled/object files and cached files
1. doc, -d, --doc           show documentation for an object in file
1. run, -r, --run           run program and compile if required
1. walk, -w, --walk         compile and run program
1. test, -t, --test         run tests
1. env, -e, --env           print Dove's workspace environment information
1. reset, -r, --reset       reset Dove's preferences & environment to default
1. tree, -l, --tree, --list list project files & directories as tree
1. ext, -ext, --ext         manage extensions
1. info, -i, --info         print Dove's information
1. update, -u, --update     update dove and extensions
1. switch, -s, --switch     check or switch Dove's current language mode
1. fix, -f, --fix           fixes Dove's preferences
1. -v, --verbose            increase output verbosity

## Using Wizard

Dove's installation tool.

Commands you can use: install, remove, info

### For user

`./wizard <command>`

### For all (root)

`sudo ./wizard <command>`
