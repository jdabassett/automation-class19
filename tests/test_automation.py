import pytest
import os
from automation.main import create_dir, delete_dir




# @pytest.mark.skip("TODO")
def test_create_dir_exists():
    assert create_dir

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


