#!/usr/bin/env python3

VERSION = "1.1.0"

##############################################################################
# DEFAULTS #
CSSE7030 = False
SCRIPT = "assign1"
TEST_DATA = "assign1_testdata"
TEST_DATA_RAW = ''
SHOW_VERSION = True
# END DEFAULTS #
##############################################################################

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("script",
    help="The script you want to run the tests against.",
    nargs="?",
    default=SCRIPT)
parser.add_argument("test_data",
    help="The file containing test data to use.",
    nargs="?",
    default=TEST_DATA)
parser.add_argument("-m", "--masters",
    help="Whether or not to utilize master's tests.",
    action='store_true',
    default=CSSE7030)
parser.add_argument('unittest_args', nargs='*')

args = parser.parse_args()

import unittest

if args.test_data:
    data = __import__(args.test_data.rstrip('.py'))
else:
    import imp
    data = imp.new_module('data')
    exec(TEST_DATA_RAW, data.__dict__)


try:
    assignment = __import__(args.script.rstrip('.py'))
except SyntaxError as e:
    print("/-----------------------------------\\")
    print("| Tests not run due to syntax error |")
    print("\\-----------------------------------/")
    traceback.print_exception(SyntaxError, e, None, file=sys.stdout)
    sys.exit(0)

from io import StringIO
import sys
import collections
import contextlib
import warnings
import traceback

class CsseTestResult(unittest.TextTestResult):
    def startTest(self, test):
        super(unittest.TextTestResult, self).startTest(test)
        self.runbuffer = StringIO()
        self.runbuffer.write(test.id().split('.')[-1].strip().lstrip('test_'))
        self.runbuffer.write(": {} \n")
        self.stream.flush()
        self._stcount = 0
        self._stpass = 0

    def addSubTest(self, test, subtest, err):
        self._stcount += 1
        super().addSubTest(test,subtest,err)
        if err:
            self.runbuffer.write("  - ")
        else:
            self._stpass += 1
            self.runbuffer.write("  + ")
        self.runbuffer.write(subtest.id().lstrip(test.id()).strip()[1:-1] + "\n")

    def addFailure(self, test, err):
        self.stream.write("\t" + test.id().lstrip("test_"))
        self.stream.writeln("... FAIL")
        super(unittest.TextTestResult, self).addFailure(test, err)

    def addSuccess(self, test):
        super(unittest.TextTestResult, self).addSuccess(test)
        if self.dots:
            self.stream.write('.')
            self.stream.flush()

    def printErrors(self):
        if self.errors or self.failures:
            self.stream.writeln("\n/--------------\\")
            self.stream.writeln("| Failed Tests |")
            self.stream.writeln("\\--------------/")
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)

    def stopTest(self, test):
        super().stopTest(test)
        self.runbuffer.seek(0)
        self.stream.writeln(self.runbuffer.read().format("{}/{}".format(self._stpass,self._stcount)))
        del self.runbuffer

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        if exctype is test.failureException:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
            msgLines = traceback.format_exception_only(exctype, value)
        else:
            msgLines = traceback.format_exception(exctype, value, tb)

        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(STDOUT_LINE % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(STDERR_LINE % error)
        return ''.join(msgLines)


class Csse1001TestCase(unittest.TestCase):
    def id(self):
        return super().id().split('.')[-1].strip()

    class CsseSubtest(unittest.case._SubTest):
        def id(self):
            return super(Csse1001TestCase.CsseSubtest, self).id().split('test_')[-1].strip()

    maxDiff = None
    def __str__(self):
        return "Test "+self._testMethodName[5:]

    @contextlib.contextmanager
    def subTest(self, msg=None, **params):
        """Return a context manager that will return the enclosed block
        of code in a subtest identified by the optional message and
        keyword parameters.  A failure in the subtest marks the test
        case as failed but resumes execution at the end of the enclosed
        block, allowing further test code to be executed.
        """
        if not self._outcome.result_supports_subtests:
            yield
            return
        parent = self._subtest
        if parent is None:
            params_map = collections.ChainMap(params)
        else:
            params_map = parent.params.new_child(params)
        self._subtest = Csse1001TestCase.CsseSubtest(self, msg, params_map)
        try:
            with self._outcome.testPartExecutor(self._subtest, isTest=True):
                yield
            if not self._outcome.success:
                result = self._outcome.result
                if result is not None and result.failfast:
                    raise unittest.case._ShouldStop
            elif self._outcome.expectedFailure:
                # If the test is expecting a failure, we really want to
                # stop now and register the expected failure.
                raise unittest.case._ShouldStop
        finally:
            self._subtest = parent


def addGetTestCases(fnname,dataname, f=lambda x: x):
    def fn(self):
        for i, item in eval("data.{}".format(dataname)):
            with self.subTest(i):
                fail = 0
                try:
                    fn = eval("assignment." + fnname)
                except AttributeError:
                    fail = 1
                if fail:
                    self.fail("No function named '" +fnname +"'")
                self.assertEqual(f(fn(*item[0])),f(item[1]))
    setattr(Csse1001TestCase, "test_{}".format(fnname),fn)


def addIOTestCases(fnname, dataname, fout = lambda x: x, fret = lambda x: x):
    d = eval("data.{}".format(dataname))
    def fn(self):
        self._in = sys.stdin
        self._out = sys.stdout
        for i, item in d:
            sys.stdin = StringIO()
            sys.stdout = StringIO()
            with self.subTest(i):
                fail = 0
                try:
                    fn = eval("assignment." + fnname)
                except AttributeError:
                    fail = 1
                if fail:
                    self.fail("No function named '" +fnname +"'")
                sys.stdin.write(item[1][0])
                sys.stdin.seek(0)
                self.assertEqual(fret(fn(*item[0][0])),fret(item[0][1]))
                sys.stdout.seek(0)
                self.assertEqual(fout(sys.stdout.read()), fout(item[1][1]))
        sys.stdin = self._in
        sys.stdout = self._out

    setattr(Csse1001TestCase, "test_{}".format(fnname),fn)

def addDocstringTests(data):
    def fn(self):
        for fnname in data:
            with self.subTest(fnname):
                fail = 0
                try:
                    fn = eval("assignment." + fnname)
                except AttributeError:
                    fail = 1
                if fail:
                    self.fail("No function named '" +fnname +"'")
                self.assertTrue(fn.__doc__,
                                     "Function "+fnname+" should have a docstring")
    setattr(Csse1001TestCase, "test_docstrings",fn)


loads_sorting = lambda x: [(k,list(sorted(map(lambda x:float(round(x,10)),v)))) for k,v in x]

def fix_floats(data):
    return [(x,) +tuple(map(lambda x:float(round(x,10)),y)) for x,*y in data]

addGetTestCases("get_ranges","ranges")
addGetTestCases("get_mean","means")
addGetTestCases("get_median","medians")
addGetTestCases("get_std_dev","stddevs",lambda x:float(round(x,10)))
addGetTestCases("load_data","loads")


old_load_test = Csse1001TestCase.test_load_data
def fn(self):
    old_load_test(self)
    fail = 0
    with self.subTest("file closed"):
        try:
            fn = eval("assignment.load_data")
        except AttributeError:
            fail = 1
        if fail:
            self.fail("No function named 'load_data'")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            fn("animal_heights.csv")
            for warn in w:
                if issubclass(warn.category, ResourceWarning):
                    self.fail("Files should be closed in load_data")
            warnings.simplefilter("ignore")
Csse1001TestCase.test_load_data = fn

addGetTestCases("data_summary","summaries", fix_floats)

import re
def table_strip(string):
    string = string.replace("Set Summaries","\nSet Summaries")
    string = string.replace("Unknown command","\nUnknown command")
    vals = [re.split(" {2,}|\t+",x.strip()) for x in string.strip().split('\n')]
    return "\n".join("".join(map("{0: <15}".format,x)) for x in vals if x != [''])

addIOTestCases("display_set_summaries","sets",table_strip)
addIOTestCases("interact","interactions",table_strip)

if args.masters:
    addGetTestCases("data_comparison","comparisons")
    addIOTestCases("display_comparison","comp_io",table_strip)
    addIOTestCases("interact","interactions7030",table_strip)
fns = [
    "load_data",
    "get_ranges",
    "get_mean",
    "get_median",
    "get_std_dev",
    "data_summary",
    "display_set_summaries",
    "interact",
]


if args.masters:
    fns +=["data_comparison", "display_comparison"]
addDocstringTests(fns)

def methodCmp(a, b):
    global fns
    As = [i for i,x in enumerate(fns+["docstrings"]) if x in a]
    Bs = [i for i,x in enumerate(fns+["docstrings"]) if x in b]
    return As[0] - Bs[0]

if __name__=="__main__":
    if SHOW_VERSION:
        print("Version {}\n".format(VERSION))

    sys.argv[1:] = args.unittest_args
    runner = unittest.TextTestRunner(verbosity=9, resultclass=CsseTestResult, stream=sys.stdout)
    loader = unittest.defaultTestLoader
    loader.sortTestMethodsUsing=methodCmp
    print("/--------------------\\")
    print("| Summary of Results |")
    print("\\--------------------/")
    unittest.main(testRunner=runner, testLoader=loader)
