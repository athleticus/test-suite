#!/usr/bin/env python3

from test import *

# #############################################################################
# DEFAULT OVERRIDES #
DEFAULTS['VERSION'] = "2016s1_1.1.0"
DEFAULTS['HIDE_TRACEBACK_PATHS'] = True
# END DEFAULT OVERRIDES #
# #############################################################################

class AssignmentOneMaster(TestMaster):
    def prepare(self):
        fns = """
            make_initial_state
            make_position_string
            num_diffs
            position_of_blanks
            make_move
            show_current_state
            interact
        """.strip().split()

        # (class_name, [method, ...], super_class_1, super_class_2, ...)
        # klasses = []

        module = self._module

        # InheritanceTestCase = create_inheritance_test_case(module, classes=klasses)

        data = self._test_data

        self._tests = [
            create_io_test_case(module, "make_initial_state", data['initial_states']),
            create_io_test_case(module, "make_position_string", data['position_strings']),
            create_io_test_case(module, "num_diffs", data['diffs']),
            create_io_test_case(module, "position_of_blanks", data['blank_positions']),
            create_io_test_case(module, "make_move", data['moves']),

            create_io_test_case(module, "show_current_state", data['current_states']),
            create_io_test_case(module, "interact", data['interactions']),

            create_naming_test_case(module, functions=fns),
            create_docstring_test_case(module, functions=fns),
        ]

if __name__ == "__main__":
    t = AssignmentOneMaster()
    t.main()