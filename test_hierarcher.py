import argparse
import io
import locale
import sys
import unittest

import hierarcher
from validations import ALLOWED_FILE_EXTENSIONS


class TestHierarcher(unittest.TestCase):

    def setUp(self) -> None:
        locale.setlocale(locale.LC_ALL, 'en_US')
        self.args = {}
        self.captured_output = io.StringIO()

    def test_should_raise_ValueError_when_both_args_are_not_passed(self):
        # GIVEN
        self.args['input_file'] = None
        self.args['input_text'] = None

        # WHEN
        with self.assertRaises(ValueError) as ex:
            hierarcher.main(self.args)

        # THEN
        self.assertEqual(str(ex.exception),
                         "Either file path or direct text must be provided as argument, but not both.")

    def test_should_raise_ValueError_when_both_args_are_passed(self):
        # GIVEN
        self.args['input_text'] = '{"employer": {"name": "Nerijus"}}'
        self.args['input_file'] = 'hi.json'

        # WHEN
        with self.assertRaises(ValueError) as ex:
            hierarcher.main(self.args)

        # THEN
        self.assertEqual(str(ex.exception),
                         "Either file path or direct text must be provided as argument, but not both.")

    def test_should_raise_ArgumentTypeError_from_incorrect_text_input(self):
        # GIVEN
        self.args['input_text'] = "something something something"
        self.args['input_file'] = None

        # WHEN
        with self.assertRaises(argparse.ArgumentTypeError) as ex:
            hierarcher.main(self.args)

        # THEN
        self.assertEqual(str(ex.exception), "Sorry, this does not seem like a valid input format. See README.")

    def test_should_raise_ArgumentTypeError_on_provided_not_supported_file_extension(self):
        # GIVEN
        self.args['input_text'] = None
        self.args['input_file'] = "input.txt"

        # WHEN
        with self.assertRaises(argparse.ArgumentTypeError) as ex:
            hierarcher.main(self.args)

        # THEN
        self.assertEqual(str(ex.exception), "Only {} file extensions are allowed.".format(ALLOWED_FILE_EXTENSIONS))

    def test_should_calculate_correct_total_salary(self):
        # GIVEN
        self.args['input_text'] = {
            "employer": {
                "name": "Jeff",
                "salary": 100000,
                "reports": [{
                    "employer": {
                        "name": "Dave",
                        "salary": 85000,
                        "reports": [{
                            "employer": {
                                "name": "Anna",
                                "salary": 70000,
                                "reports": []
                            }
                        }]
                    }
                },
                    {
                        "employer": {
                            "name": "Cory",
                            "salary": 65000,
                            "reports": []
                        }
                    }
                ]
            }
        }

        # WHEN
        total_salary = hierarcher.get_total_salary(self.args['input_text'])

        # THEN
        self.assertEqual(total_salary, 320000)

    def test_should_print_correct_hierarchy(self):
        # GIVEN
        self.args['input_text'] = {
            "employer": {
                "name": "Jeff",
                "salary": 100000,
                "reports": [{
                    "employer": {
                        "name": "Dave",
                        "salary": 85000,
                        "reports": [{
                            "employer": {
                                "name": "Anna",
                                "salary": 70000,
                                "reports": []
                            }
                        }]
                    }
                },
                    {
                        "employer": {
                            "name": "Cory",
                            "salary": 65000,
                            "reports": []
                        }
                    }
                ]
            }
        }

        expected_hierarchy = ("Jeff\n"
                              "Employees of: Jeff\n"
                              "    Cory\n"
                              "    Dave\n"
                              "    Employees of: Dave\n"
                              "        Anna\n"
                              )
        sys.stdout = self.captured_output

        # WHEN
        hierarcher.print_employers(self.args['input_text'])
        sys.stdout = sys.__stdout__

        # THEN
        self.assertEqual(expected_hierarchy, self.captured_output.getvalue())

    def test_should_print_correct_sorted_hierarchy_with_correct_total_salary(self):
        # GIVEN
        self.args['input_text'] = {
            "employer": {
                "name": "Jeff",
                "salary": 100000,
                "reports": [{
                    "employer": {
                        "name": "Dave",
                        "salary": 85000,
                        "reports": [{
                            "employer": {
                                "name": "Zach",
                                "salary": 60000,
                                "reports": []
                            }
                        }, {
                            "employer": {
                                "name": "Anna",
                                "salary": 70000,
                                "reports": []
                            }
                        }]
                    }
                },
                    {
                        "employer": {
                            "name": "Cory",
                            "salary": 65000,
                            "reports": []
                        }
                    }
                ]
            }
        }

        expected_hierarchy = ("Jeff\n"
                              "Employees of: Jeff\n"
                              "    Cory\n"
                              "    Dave\n"
                              "    Employees of: Dave\n"
                              "        Anna\n"
                              "        Zach\n"
                              "Total salary: $380,000.00\n"
                              )
        sys.stdout = self.captured_output

        # WHEN
        hierarcher.print_hierarchy(self.args['input_text'])
        sys.stdout = sys.__stdout__

        # THEN
        self.assertEqual(expected_hierarchy, self.captured_output.getvalue())
