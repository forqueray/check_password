
# -*- coding: utf-8 -*-

import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import check_password # noqa

def test_fake():
    print('This is a fake test')
    assert (1 == 1)


def test_check_data_storage_user():
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': '12345678', 'DATA_STORAGE_USER_RO': '12345678'}) is False)
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine'}) is True)
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'stephanie'}) is True)
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'geraldine'}) is False)
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': '1232345678', 'DATA_STORAGE_USER_RO': '1234567891011121214111111'}) is False)
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': '1232', 'DATA_STORAGE_USER_RO': '12345678'}) is False)
    assert(check_password.check_data_storage_user({'DATA_STORAGE_USER': '1232*RETETE', 'DATA_STORAGE_USER_RO': '12345678'}) is False)


def test_check_data_storage_password():
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': '12345678', 'DATA_STORAGE_USER_RO': '12345678'}) is False)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine'}) is True)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'stephanie'}) is True)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'geraldine'}) is False)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': '1232345678', 'DATA_STORAGE_USER_RO': '1234567891011121214111111'}) is True)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': '1232345678', 'DATA_STORAGE_USER_RO': '12345678910123456789012345678901234567890'}) is False)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': '1232', 'DATA_STORAGE_USER_RO': '12345678'}) is False)
    assert(check_password.check_data_storage_password({'DATA_STORAGE_USER': '1232*RETETE', 'DATA_STORAGE_USER_RO': '12345678'}) is False)


def test_check_password_length():
    assert(check_password.check_password_length({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'stephanie'}, 8, 20) is True)
    assert(check_password.check_password_length({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'stephanie'}, 15, 20) is False)
    assert(check_password.check_password_length({'DATA_STORAGE_USER': 'mathilda', 'DATA_STORAGE_USER_RO': 'geraldine', 'DATA_STORAGE_USERKEY': 'stephanie'}, 8, 2) is False)

def test_check_alphanumerique():
    assert(check_password.check_alphanumerique(['123']) is True)
    assert(check_password.check_alphanumerique(['ABCDEF']) is True)
    assert(check_password.check_alphanumerique(['*']) is False)
    assert(check_password.check_alphanumerique(['123*']) is False)
    assert(check_password.check_alphanumerique(['123%']) is False)
    assert(check_password.check_alphanumerique(['']) is False)
    assert(check_password.check_alphanumerique(['123', '456']) is True)
    assert(check_password.check_alphanumerique(['123', '456%']) is False)
    assert(check_password.check_alphanumerique(['123', '456', '###']) is False)
    assert(check_password.check_alphanumerique(['mathilda', 'geraldine', 'geraldine']) is True)


def test_check_identical_values():
    assert(check_password.check_identical_values(['123', '123']) is True)
    assert(check_password.check_identical_values(['123', '234']) is False)
    with pytest.raises(ValueError):
        check_password.check_identical_values(['123'])
    assert(check_password.check_identical_values(['riri', 'fifi', "loulou"]) is False)
    assert(check_password.check_identical_values(['mathilda', 'geraldine', "geraldine"]) is False)
    assert(check_password.check_identical_values(['geraldine', 'geraldine', "geraldine"]) is True)
    assert(check_password.check_identical_values(['riri', 'riri', "riri"]) is True)


def test_check_different_values():
    assert(check_password.check_different_values(['geraldine', 'geraldine', "geraldine"]) is False)
    assert(check_password.check_different_values(['riri', 'riri', "riri"]) is False)
    assert(check_password.check_different_values(['riri', 'fifi', "loulou"]) is True)


def test_check_no_quotes_and_double_quotes():
    assert(check_password.check_no_quotes_and_double_quotes(["truc", "bidule"]) is True)
    assert(check_password.check_no_quotes_and_double_quotes(["truc", "bid'ule"]) is False)
    assert(check_password.check_no_quotes_and_double_quotes(["tr'uc", "bid'ule"]) is False)
    assert(check_password.check_no_quotes_and_double_quotes(["tr'uc", "bidule"]) is False)
    assert(check_password.check_no_quotes_and_double_quotes(["truc", "bid\"ule"]) is False)
    assert(check_password.check_no_quotes_and_double_quotes(["tr\"uc", "bid\"ule"]) is False)
    assert(check_password.check_no_quotes_and_double_quotes(["tr\"uc", "bidule"]) is False)
    assert(check_password.check_no_quotes_and_double_quotes(["truc", "bidule", "machin"]) is True)
    assert(check_password.check_no_quotes_and_double_quotes(["truc", "bidule", "ma'chin"]) is False)


def test_check_content():
    assert(check_password.check_content({"riri":"1", "fifi":"2"}, {"riri":"1", "fifi":"2"}) is True)
    assert(check_password.check_content({"riri":"1", "fifi":"2"}, {"riri":"1", "fifi":"3"}) is False)
    assert(check_password.check_content({"riri":"1", "fifi":"2"}, {"riri":"1", "fifi2":"2"}) is False)
    assert(check_password.check_content({"riri":"1", "fifi":"2"}, {"ririr":"1", "fifi":"2"}) is False)
    assert(check_password.check_content(["riri", "fifi", "loulou"], ["riri", "fifi", "loulou"]) is True)
    assert(check_password.check_content(["riri", "fifi", "loulou"], ["riri", "fifi", "loulou2"]) is False)
