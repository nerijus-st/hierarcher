import argparse
import json

ALLOWED_FILE_EXTENSIONS = ('.yaml', '.json')


def validate_file_argument(value):
    if not value.lower().endswith(ALLOWED_FILE_EXTENSIONS):
        raise argparse.ArgumentTypeError("Only {} file extensions are allowed.".format(ALLOWED_FILE_EXTENSIONS))


def validate_text_argument(value):
    try:
        json.loads(value)
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError("Sorry, this does not seem like a valid input format. See README.")


def validate_args(args):
    if not any(args.values()) or all(args.values()):
        raise ValueError("Either file path or direct text must be provided as argument, but not both.")

    if args['input_file'] is not None:
        validate_file_argument(args['input_file'])
    elif args['input_text'] is not None:
        validate_text_argument(args['input_text'])
