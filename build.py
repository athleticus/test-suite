#!/usr/bin/env python3

import os
import argparse

def build_test(test):
    """
    Builds a standalone test executable based upon test configuration.

    :param test: A dictionary containing the test's configuration. Has keys:
        test_runner: The test runner to use (i.e. suite.py)
        executable: The name of the output file (i.e. assign1_sample_tests.py)
        options: A dictionary whose keys override the given defaults in test_runner.
    """

    test_runner = test['test_runner']
    executable = test['executable']
    options = test['options']

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest",
                        help="The build manifest.",
                        nargs="?",
                        default="manifest.py")

    args = parser.parse_args()

    manifest = __import__(args.manifest.rstrip('.py').replace("/","."))

    # Work from the manifest file's directory
    os.chdir('./' + os.path.dirname(args.manifest))

    for test in manifest.tests:
        build_test(test)


