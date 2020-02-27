#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import argparse


# - Attention, les valeurs doivent être différentes pour :
# - DATA_STORAGE_ACCESS_KEY <> DATA_STORAGE_USER <> DATA_STORAGE_USER_RO
# - DATA_STORAGE_SECRET_KEY <> DATA_STORAGE_PASSWORD <> DATA_STORAGE_PASSWORD_RO


def check_alphanumerique(items):
    # test_alphanumerique = re.compile(r"(?i)[a-zA-Z0-9_]+")  # ne prends que les caractères alpha numerique
    test_alphanumerique = re.compile(
        r"^\w+$"
    )  # ne prends que les caractères alpha numerique
    for item in items:
        if test_alphanumerique.search(item) is None:
            print("Item with non alphanumeric char: {}".format(item))
            return False
    return True


def check_no_quotes_and_double_quotes(items):
    test_quotes = re.compile(r"('|\")")
    for item in items:
        if test_quotes.search(item) is not None:
            print("Item with quote or double quote: {}".format(item))
            return False
    return True


def check_content(item, expected_item):
    if item == expected_item:
        return True
    else:
        return False


def check_identical_values(items):
    if len(items) < 2:
        raise ValueError("Values should be at least 2")
    for index in range(1, len(items)):
        if not items[index] == items[index - 1]:
            return False
    return True


def check_different_values(items):
    values = {}
    for item in items:
        values.update({item: ""})
    if len(items) == len(values.keys()):
        return True
    else:
        return False


def check_data_storage_user(keys):
    return check_data_storage(keys, 20)


def check_data_storage_password(keys):
    return check_data_storage(keys, 40)


def check_data_storage(keys, max_length):
    if (
        check_password_length(keys, 8, max_length)
        and check_alphanumerique(keys.values())
        and check_different_values(list(keys.values()))
    ):
        return True
    else:
        return False


def check_password_length(keys, min_length, max_length):
    result = True
    for (key, value) in keys.items():
        if min_length <= (len(value.rstrip())) <= max_length:
            pass
        else:
            print(
                "Key {} failed, number of char is not beween {} and {}".format(
                    key, min_length, max_length
                )
            )
            result = False

    return result


def parse_input_file(file):

    data = {}

    try:
        with open(file, "r") as fp:  # ouvre fichier
            content = fp.readlines()
            for item in content:
                match = re.search(r"^(.+)=(.+)$", item)
                if match:
                    data.update({match.group(1): match.group(2)})

            return data

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_full_path_name")
    args = parser.parse_args()

    data = parse_input_file(args.file_full_path_name)

    # import pprint
    # pprint.pprint(data)

    if not check_data_storage_user(
        {
            "DATA_STORAGE_ACCESS_KEY": data["DATA_STORAGE_ACCESS_KEY"],
            "DATA_STORAGE_USER": data["DATA_STORAGE_USER"],
            "DATA_STORAGE_USER_RO": data["DATA_STORAGE_USER_RO"],
        }
    ):
        sys.exit(4)

    if not check_data_storage_password(
        {
            "DATA_STORAGE_SECRET_KEY": data["DATA_STORAGE_SECRET_KEY"],
            "DATA_STORAGE_PASSWORD": data["DATA_STORAGE_PASSWORD"],
            "DATA_STORAGE_PASSWORD_RO": data["DATA_STORAGE_PASSWORD_RO"],
        }
    ):
        sys.exit(3)

    if not check_content(data["CAMUNDA_ADMIN_PASSWORD"], "admin"):
        print("CAMUNDA_ADMIN_PASSWORD is not equal to 'admin'")
        sys.exit(2)

    if not check_no_quotes_and_double_quotes(data.values()):
        print("A secret value contains a quote or double quote")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
