import passbook
import hashlib
import pytest


def test_valid_input_hashpassword():
    pwds = ['hello', 'world', 'sample', 'hello@', 'hello$12', '']
    for pwd in pwds:
        assert passbook.hashpassword(pwd) == hashlib.sha256(
            pwd.encode('utf-8')).hexdigest()


def test_invalid_input_hashpassword():
    invalid_pwds = [{}, [], None, 10]
    for pwd in invalid_pwds:
        with pytest.raises(AttributeError):
            passbook.hashpassword(pwd)


def test_is_master_password(mocker):

    mocker.patch('passbook.getmasterpwd',
                 new=lambda pwd: pwd == hashlib.sha256(
                     'master_password'.encode('utf-8')).hexdigest())

    # correct password
    assert passbook.is_master_password('master_password')

    # incorrect password
    assert not passbook.is_master_password('hello')


def test_is_master_password_exceptions():
    invalid_pwds = [{}, [], None, 10]
    for pwd in invalid_pwds:
        with pytest.raises(AttributeError):
            passbook.is_master_password(pwd)


def test_decrypt_password(mocker):

    mocker.patch('passbook.getpassword', return_value=[
                 [passbook.encrypt_message('test_password')]])
    # correct
    assert passbook.decrypt_password('user') == 'test_password'

    # incorrect
    assert not passbook.decrypt_password('user') == 'test_password_invalid'


def test_decrypt_username(mocker):

    mocker.patch('passbook.getusername', return_value=[
                 [passbook.encrypt_message('test_username')]])
    # correct
    assert passbook.decrypt_username('user') == 'test_username'

    # incorrect
    assert not passbook.decrypt_username('user') == 'test_username_invalid'
