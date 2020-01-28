# Dove

Dove is a tool for quickly managing projects in a shell like an IDE

## Usage

    Use this pattern when using in a shell: `dove [flags] <command or option> [arguments]`

## Available Commands

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
