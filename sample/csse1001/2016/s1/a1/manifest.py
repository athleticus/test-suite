TEST_RUNNER = "assign1_tests.py"

tests = [
    {
        "test_runner": TEST_RUNNER,
        "executable": "assign1_sample_tests.py",
        "options": {
            "CSSE7030": False,
            "TEST_DATA": None,
            "TEST_DATA_RAW": "assign1_testdata.py",
            "SCRIPT": "assign1.py"
        }
    },
    {
        "test_runner": TEST_RUNNER,
        "executable": "assign1_marking_tests.py",
        "options": {
            "CSSE7030": False,
            "TEST_DATA": None,
            "TEST_DATA_RAW": "assign1_testdata.py",
            "SCRIPT": "assign1.py"
        }
    }
]