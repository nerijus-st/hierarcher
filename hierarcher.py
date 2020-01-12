#!/usr/bin/env python3

import argparse
import json
import locale

import yaml

from validations import validate_args

# @TODO add coverage/build into travis CI
# @TODO write README
# @TODO add more tests
# @TODO handle keyErrors?


def setup():
    locale.setlocale(locale.LC_ALL, "en_US")


def get_args():
    parser = argparse.ArgumentParser(
        description="Pass text into command line or specify a json/yaml file"
    )
    parser.add_argument("-t", "--text", dest="input_text", help="Pass input directly")
    parser.add_argument(
        "-f", "--file", dest="input_file", help="Specify path of input json/yaml file",
    )
    args = vars(parser.parse_args())
    return args


def get_total_salary(data: dict) -> float:
    total_salary = data["employer"]["salary"]

    for emp in data["employer"]["reports"]:
        total_salary += get_total_salary(emp)

    return total_salary


def print_employers(data: dict, indent: int = 0):
    output = data["employer"]["name"]
    if indent > 0:
        output = " " * indent + output
    print(output)

    if data["employer"]["reports"]:
        print(" " * indent + "Employees of: {}".format(data["employer"]["name"]))
        indent += 4

        for emp in sorted(
            data["employer"]["reports"], key=lambda x: x["employer"]["name"]
        ):
            print_employers(emp, indent)


def print_total_salary(data: dict):
    salary = get_total_salary(data)
    print("Total salary: {}".format(locale.currency(salary, grouping=True)))


def print_hierarchy_from_file(file_path: str):
    with open(file_path, "r") as f:
        if "yaml" in file_path:
            data = yaml.safe_load(f)
        else:
            data = json.load(f)

        print_hierarchy(data)


def print_hierarchy(data: dict):
    print_employers(data)
    print_total_salary(data)


def main(args: dict):
    validate_args(args)

    if args["input_file"] is not None:
        print_hierarchy_from_file(args["input_file"])
    elif args["input_text"] is not None:
        data = json.loads(args["input_text"])
        print_hierarchy(data)


if __name__ == "__main__":
    setup()
    args = get_args()
    main(args)
