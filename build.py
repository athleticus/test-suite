#!/usr/bin/env python3

import os
import argparse
import imp
import sys

from test import relative_import

MODULE_EMBED = """
import imp
import sys
sys.modules['{module}'] = imp.new_module('{module}')
exec({code}, sys.modules['{module}'].__dict__)
""".strip()

def embed_module(module_name, file_path):
    """
    Generates python code for embedding the given module.

    :param module_name: The name of the module.
    :param file: The file containing the module data.
    :return: A string that can be embedded into a given file that imports the module.
    """

    with open(file_path, "r") as fd:
        return MODULE_EMBED.format(module=module_name, code=repr(fd.read()))




def build_test(test_runner, executable, options, library_path="test.py"):
    """
    Builds a standalone test executable based upon test configuration.

    :param test_runner: The test runner to use (i.e. suite.py)
    :param executable: The name of the output file (i.e. assign1_sample_tests.py)
    :param options: A dictionary whose keys override the given defaults in test_runner.
    :param library_path: The path to the test library to be embedded.

    :return: None
    """

    if options['TEST_DATA_RAW']:
        with open(options['TEST_DATA_RAW'], 'r') as fd:
            options['TEST_DATA_RAW'] = fd.read()

    output = []

    first_line = False
    started = False
    stopped = False

    with open(test_runner, 'r') as fd:
        for line in fd:
            if not first_line and not line.strip().startswith("#"):
                first_line = True

                embed_code = embed_module("test", library_path)
                output.append("\n" + embed_code + "\n")


            if not started and line.startswith("# DEFAULT OVERRIDES #"):
                started = True

            if started and line.startswith('DEFAULTS['):
                key = line.split('[', 1)[1].split(']')[0].strip()[1:-1]
                if key in options:
                    continue

            if line.startswith("# END DEFAULT OVERRIDES #"):
                for key, value in options.items():
                    override = "DEFAULTS[{key!r}] = {value!r}".format(key=key, value=value)
                    output.append(override + "\n")

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
                        help="The build manifest.")
    parser.add_argument("-r", "--remove",
                        help="Removes the executables.",
                        action="store",
                        type=bool,
                        default=False)

    args = parser.parse_args()

    # import manifest file
    manifest = relative_import(args.manifest, "manifest")

    library_path = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.py"))

    # Work from the manifest file's directory
    os.chdir('./' + os.path.dirname(args.manifest))

    for test in manifest.tests:
        if args.remove:
            clear_test(test['executable'])
        else:
            build_test(library_path = library_path, **test)


