import pytest
import os
from automation.main import create_dir, delete_dir, delete_user, restore_user

# @pytest.mark.skip("TODO")
def test_functions_exist():
    assert (create_dir and delete_dir and delete_user and restore_user)


# @pytest.mark.skip("TODO")
def test_create_and_delete_dir_functions():
    str_dir = "delete_dir_for_testing"
    create_dir("delete_dir_for_testing")
    list_contents = os.listdir(".")
    bool_exists = False
    if str_dir in list_contents:
        bool_exists = True
    delete_dir(str_dir)
    assert bool_exists

# @pytest.mark.skip("TODO")
def test_delete_user():
    str_cwd = os.getcwd()
    create_dir("user-docs/userTest")
    delete_dir("temp-user-docs/userTest")
    delete_user("userTest")
    list_root = os.listdir(str_cwd)
    list_temp = os.listdir(os.path.join(str_cwd, "temp-user-docs"))
    list_users = os.listdir(os.path.join(str_cwd, "user-docs"))
    delete_dir("temp-user-docs/userTest")
    if "temp-user-docs" not in list_root or "userTest" not in list_temp or "userTest" in list_users:
        assert False
    else:
        assert True


# @pytest.mark.skip("TODO")
def test_restore_user():
    str_cwd = os.getcwd()
    create_dir("temp-user-docs/userTest")
    delete_dir("user-docs/userTest")
    restore_user("userTest")
    list_root = os.listdir(str_cwd)
    list_temp = os.listdir(os.path.join(str_cwd, "temp-user-docs"))
    list_users = os.listdir(os.path.join(str_cwd, "user-docs"))
    delete_dir("user-docs/userTest")
    if "temp-user-docs" not in list_root or "userTest" in list_temp or "userTest" not in list_users:
        assert False
    else:
        assert True





