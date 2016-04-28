#!/usr/bin/env python3

import os
import argparse

def build_test(test_runner, executable, options):
    """
    Builds a standalone test executable based upon test configuration.

    :param test_runner: The test runner to use (i.e. suite.py)
    :param executable: The name of the output file (i.e. assign1_sample_tests.py)
    :param options: A dictionary whose keys override the given defaults in test_runner.

    :return: None
    """

    if options['TEST_DATA_RAW']:
        with open(options['TEST_DATA_RAW'], 'r') as fd:
            options['TEST_DATA_RAW'] = repr(fd.read())

    output = []
    started = False
    stopped = False
    with open(test_runner, 'r') as fd:
        for line in fd:
            if not stopped and line.startswith("# DEFAULTS #"):
                started = True

            if started and line.startswith("# END DEFAULTS #"):
                stopped = True

            if started:
                key = line.split('=')[0].strip()
                if key in options:
                    line = "{key} = {value}\n".format(
                        key=key,
                        value=options[key])

            output.append(line)

    with open(executable, 'w') as fd:
        fd.writelines(output)

def clear_test(executable):
    """
    Deletes the executable for a given test.

    :param executable: The executable to delete.

    :return: None
    """
    try:
        os.remove(executable)
    except OSError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest",
                        help="The build manifest.",
                        nargs="?",
                        default="manifest.py")
    parser.add_argument("-r", "--remove",
                        help="Removes the executables.",
                        action="store",
                        type=bool,
                        default=False)

    args = parser.parse_args()

    manifest = __import__(args.manifest.rstrip('.py').replace("/","."))

    # Work from the manifest file's directory
    os.chdir('./' + os.path.dirname(args.manifest))

    for test in manifest.tests:
        if args.remove:
            clear_test(test['executable'])
        else:
            build_test(**test)


