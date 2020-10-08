#!/usr/bin/env python3

import os, subprocess, sys

if len(sys.argv) == 2:
    if str(sys.argv[1]) == "finish":
        subprocess.call(["rm", "-rf", "outputs", "diffs", "result"])
        exit()
if len(sys.argv) > 2:
    print("usage: ./test42sh.py [0 or 1 whether leakcheck is needed]")
    exit()
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

binary_name = "./42sh"

arglist_student = [binary_name]

valgrind = ["valgrind", "--leak-check=full", "--error-exitcode=1"]
subprocess.call(["mkdir", "-p", "diffs", "outputs"])
for subdir, dir, files in os.walk("inputs"):
    for file in files:
        with open("./inputs/" + file, "r") as stdinput:
            output_file = "./outputs/" + file + "_output"
            correct_output_file = "./correct_outputs/" + file
            diffarg = ["diff", output_file, correct_output_file]
            filediff = "./diffs/" + file + "_diff"
            with open(output_file, "w+") as student_output:
                subprocess.call(arglist_student, stdout=student_output, stdin=stdinput)
            with open(filediff, "w+") as fdiff:
                subprocess.call(diffarg, stdout=fdiff)
            logname = "result"
            if os.path.getsize(filediff) == 0:
                print(file + ": " + OKGREEN + "OK" + ENDC, end= " ")
                with open(logname, "a+") as log:
                    log.write(file + ": OK\n")
                if int(sys.argv[1]) == 1:
                    valgrind += arglist_student
                    leakname = "./leakchecks/" + file
                    with open(leakname, "w+") as leakfile:
                        exitcode = subprocess.call(valgrind, stdout=leakfile, stderr=leakfile)
                    print("leakcheck: ", end="")
                    with open(logname, "a+") as log:
                        if exitcode == 0:
                            print(OKGREEN + "OK" + ENDC, end= " ")
                            log.write("leakcheck: OK\n")
                        else:
                            print(FAIL + "FAILED" + ENDC, end="")
                            log.write("leakcheck: FAILED: see the" + leakname + "for information\n")
            else:
                with open(logname, "a+") as log:
                    log.write(file + ": FAILED: see the " + filediff + " for information\n")
                print(file + ": " + FAIL + "FAILED: see the " + filediff + "for information" + ENDC, end="")
            print('\n')
