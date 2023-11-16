import pytest
import os
import shutil
from automation.main import create_dir, delete_dir, delete_user, restore_user, sort_dir, unsort_dir, find_log_files


# @pytest.mark.skip("TODO")
def test_functions_exist():
    assert (create_dir and delete_dir and delete_user and restore_user and sort_dir and unsort_dir)


# @pytest.mark.skip("TODO")
def test_create_and_delete_dir_functions():
    str_cwd = os.getcwd()
    str_dir = "delete_dir_for_testing"
    create_dir("delete_dir_for_testing")
    list_contents = os.listdir(os.path.join(str_cwd, 'user-docs'))
    bool_exists = False
    if str_dir in list_contents:
        bool_exists = True
    delete_dir(os.path.join("user-docs", str_dir))
    assert bool_exists


# @pytest.mark.skip("TODO")
def test_delete_user():
    str_cwd = os.getcwd()
    create_dir("userTest")
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
    os.makedirs(os.path.join("temp-user-docs/userTest"))
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


# @pytest.mark.skip("TODO")
def test_sort_user():
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs/userTest")
    create_dir("userTest")
    with open(os.path.join(str_dir_curr, "file.txt"), "w") as file:
        file.write("")
    with open(os.path.join(str_dir_curr, "file.log"), "w") as file:
        file.write("")
    with open(os.path.join(str_dir_curr, "file.mail"), "w") as file:
        file.write("")
    sort_dir("userTest")
    list_curr = os.listdir(str_dir_curr)
    shutil.rmtree(str_dir_curr)
    if "txt" in list_curr and "mail" in list_curr and "log" in list_curr and len(list_curr) == 3:
        assert True
    else:
        assert False


# @pytest.mark.skip("TODO")
def test_unsort_user():
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs/userTest")
    create_dir("userTest")
    create_dir("userTest/txt")
    create_dir("userTest/log")
    create_dir("userTest/mail")
    with open(os.path.join(str_dir_curr, "txt", "file.txt"), "w") as file:
        file.write("")
    with open(os.path.join(str_dir_curr, "log", "file.log"), "w") as file:
        file.write("")
    with open(os.path.join(str_dir_curr, "mail", "file.mail"), "w") as file:
        file.write("")
    unsort_dir("userTest")
    list_curr = os.listdir(str_dir_curr)
    shutil.rmtree(str_dir_curr)
    if "file.txt" in list_curr and "file.log" in list_curr and "file.mail" in list_curr and len(list_curr) == 3:
        assert True
    else:
        assert False


# @pytest.mark.skip("TODO")
def test_find_parse_user_logs():
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs/userTest")
    create_dir("userTest")
    create_dir("userTest/log")
    shutil.copy(os.path.join(str_cwd,"tests","test.log"),os.path.join(str_dir_curr, "log"))
    find_log_files("userTest")
    bool_errors = os.path.exists(os.path.join(str_dir_curr, "log", "test_errors.log"))
    bool_warnings = os.path.exists(os.path.join(str_dir_curr, "log", "test_warnings.log"))
    shutil.rmtree(str_dir_curr)
    assert bool_errors and bool_warnings

