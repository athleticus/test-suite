#!/usr/bin/env python3

TEST_RUNNER = "assign1_tests.py"

tests = [
    (TEST_RUNNER, "assign1_sample_tests_1001.py", {
        "CSSE7030": False,
        "TEST_DATA": None,
        "TEST_DATA_RAW": "assign1_sample_testdata.py",
        "MAXDIFF": 300,
        "SHOW_VERSION": True
    }),
    (TEST_RUNNER, "assign1_sample_tests_7030.py", {
        "CSSE7030": True,
        "TEST_DATA": None,
        "TEST_DATA_RAW": "assign1_sample_testdata.py",
        "MAXDIFF": 300,
        "SHOW_VERSION": True
    }),
    (TEST_RUNNER, "assign1_marking_tests.py", {
        "CSSE7030": False,
        "TEST_DATA": None,
        "TEST_DATA_RAW": "assign1_testdata.py",
        "MAXDIFF": 300,
        "SHOW_VERSION": False
    })
]

for inFile, outFile, opts in tests:
    if opts['TEST_DATA_RAW']:
        with open(opts['TEST_DATA_RAW'], 'r') as fd:
            opts['TEST_DATA_RAW'] = repr(fd.read())

    output = []
    started = False
    stopped = False
    with open(inFile, 'r') as fd:
        for line in fd:
            if not stopped and line.startswith("# DEFAULTS #"):
                started = True

            if started and line.startswith("# END DEFAULTS #"):
                stopped = True

            if started:
                key = line.split('=')[0].strip()
                if key in opts:
                    line = "{key} = {value}\n".format(
                        key=key,
                        value=opts[key])

            output.append(line)

    with open(outFile, 'w') as fd:
        fd.writelines(output)


