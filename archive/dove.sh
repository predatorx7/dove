#!/usr/bin/env bash
# Dove is a tool for managing projects as a CLI based IDE.

# styles
bold=$(tput bold)
normal=$(tput sgr0)

# Globals

## local prefs
DOVE_CACHE_PATH="$(pwd)/.dove_cache"
DOVE_LOCK_FILE="$DOVE_CACHE_PATH/dove.lock"
SUPPORTED_LANGUAGE_MODES=("Auto" "Java" "C++")
CURRENT_MODE="Auto"

## A list to temporarily cache required file details
declare -a file_array
declare -a args_array

## Dove's usage
usage="Dove is a tool for managing projects as a CLI based IDE.

Usage:
    \"dove <command|option> [arguments]\"
    or
    \"dove <command> <sub-command>\"

The commands are (dove will take only 1 command at a time):

    build, -b, --build       compile packages and dependencies
    analyse, -a, --analyse   checks for any errors or warnings in file(s)
    clean, -c, --clean       remove compiled/object files and cached files
    doc, --doc               show documentation for an object in file
    env, -e, --env           print Dove's workspace environment information
    reset, -r, --reset       reset Dove's preferences & environment to default
    list, -l, --list         list project files & directories as tree
    run, -r, --run           run program and compile if required
    walk, -w, --w            compile and run program
    test, -t, --test         run tests
    extension, --extension   manage extensions
    switch, -s               check or switch Dove's current language mode
    info, --info             print Dove's information
    update, -u, --update     update dove and extensions
    fix, -f, --fix           fixes Dove's global preferences

Use \"dove help <command>\" for more information about a command.
"

# Methods
handleFile() {
    fullFilename="${args[0]}"
    filebasename=$(basename -- "$fullFilename")
    filenameWithPath="$(pwd)/$filebasename"
    extension="${filebasename##*.}"
    filename="${filebasename%.*}"
    file_array=($filenameWithPath $filebasename $filename $extension)
}

function acquire_lock() {
    mkdir -p $DOVE_CACHE_PATH
    exec 99>"$DOVE_LOCK_FILE"
    flock -n 99
    RC=$?
    if [ "$RC" != 0 ]; then
        printf "Dove is already running for locally..\n"
        exit 1
    fi
}

function clean_cache() {
    rm $DOVE_CACHE_PATH
}
# function remove_lock() {

# }
function kdev() {
    # handleFile
    # printf "File address: ${file_array[0]}\nFilebase name: ${file_array[1]}\nFile: ${file_array[2]}\nExtension: ${file_array[3]}\n"
    acquire_lock
    echo "locked"
    echo "lock in ${DOVE_LOCK_FILE}"
    askPrompt "Done?"
    echo "unlocked"
    exit $?
}

function askPrompt() {
    message=$1
    while true; do
        read -p "$message " yn
        case $yn in
        [Yy]*) break ;;
        [Nn]*) exit ;;
        *) echo "Please answer yes or no." ;;
        esac
    done
}

# Command handling
kHelp() {
    printf "${usage}"
    exit
}

kBuild() {
    echo "Building java class"
    if [ $extension == "java" ]; then
        javac $fullFilename
    elif [ $extension != "java" -o $extension == "class" ]; then
        javac "${filename}.java"
    else
        echo "Error occured."
    fi
}

# kClean() {

# }

# kDoc() {

# }

# kEnv() {

# }

# kReset() {

# }

# kInstall() {

# }

# kList() {

# }

# kRun() {

# }

# kWalk() {

# }

# kTest() {

# }

# kExtension() {

# }

kSwitch() {
    if [[ ${args_array[0]} == "" ]]; then
        for lang in "${SUPPORTED_LANGUAGE_MODES[@]}"; do
            if [ $CURRENT_MODE == $lang ]; then
                echo "*$lang"
            else
                echo " $lang"
            fi
        done
    else
        echo "lol"
        echo ${args_array[0]}
    fi
}

# kInfo() {

# }

# kUpdate() {

# }

# kHelp() {

# }
# !
# Switch based on Command
command=$1
shift
args_array=$@
case $command in
"build") kBuild ;;
"clean") kClean ;;
"doc") kDoc ;;
"env") kEnv ;;
"reset") kReset ;;
"install") kInstall ;;
"list" | "tree") kList ;;
"run") kRun ;;
"walk") kWalk ;;
"test") kTest ;;
"extension") kExtension ;;
"switch") kSwitch ;;
"info") kInfo ;;
"update") kUpdate ;;
"dev") kdev ;;
*) kHelp ;;
esac
# !

# fullFilename=$2
# filename=$(basename -- "$fullFilename")
# extension="${filename##*.}"
# filename="${filename%.*}"
# if [ $1 == "walk" ]; then
#     echo "Compiling as $extension file.."
#     javac $fullFilename
#     echo "Starting $filename"
#     echo ""
#     java $filename
# elif [ $1 == "build" ]; then
#     echo "Compiling"
#     if [ $extension == "java" ]; then
#         javac $fullFilename
#     elif [ $extension != "java" -o $extension == "class" ]; then
#         javac "${filename}.java"
#     else
#         echo "Error occured."
#     fi
# elif [ $1 == "run" ]; then
#     if [ $extension == "java" -o $extension == "class" ]; then
#         usename=$filename
#     else
#         usename=$fullFilename
#     fi

#     if [ -f "$usename.class" ]; then
#         java $usename
#     else
#         javac "$usename.java"
#         java $usename
#     fi
# elif [ $1 == "clean" ]; then
#     if [[ $2 == "" ]]; then
#         echo "Cleaning all .class files"
#         rm *.class
#     elif [ $extension == "java" -o $extension != "class" ]; then
#         rm "${filename}.class"
#     else
#         rm $fullFilename
#     fi
# elif [ $1 == "env" ]; then
#     printf "Environment & preferences"
#     echo "Managing directory: $(pwd)"
# elif [ $1 == "info" ]; then
#     printf "D.O.V.E (A tool to help developers ${bold}D${normal}evelop with l${bold}OVE${normal}\")"
#     printf "\n\nMade to manage projects faster as a CLI based IDE."
#     printf "\n\nversion 0.0.1 made by\nMushaheed Syed smushaheed@gmail.com\n"
# else
#     printf "${usage}"
# fi
