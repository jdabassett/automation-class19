import os
import shutil
import re
from rich.console import Console
from rich.theme import Theme

automation_theme = Theme({
    'good': "green",
    'okay': "bold yellow",
    "bad": "bold underline red",
})

console = Console(theme=automation_theme)


def create_dir(str_directory: str):
    """"""
    try:
        str_cwd = os.getcwd()
        str_dir_path = os.path.join(str_cwd, "user-docs", str(str_directory))
        os.makedirs(str_dir_path)
    # error handling inspired by chatgpt
    except OSError as e:
        if os.path.exists(str_directory):
            console.print(f"Directory '{str_directory}' exists already.", style="bad")
        else:
            console.print(f"Error creating directory '{str_directory}': {e}", style='bad')


def delete_dir(str_directory: str):
    """"""
    try:
        str_cwd = os.getcwd()
        str_dir_path = os.path.join(str_cwd, str(str_directory))
        if os.path.exists(str_dir_path):
            shutil.rmtree(str_dir_path)
        else:
            print(f"Target directory '{str_directory}' doesn't exists.")
    except OSError as e:
        console.print(f"Error, deleting directory '{str_directory}': {e}", style='bad')


def delete_user(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs", str(str_directory))
    str_dir_dest = os.path.join(str_cwd, "temp-user-docs", str(str_directory))
    if os.path.exists(str_dir_curr):
        shutil.copytree(str_dir_curr, str_dir_dest)
        if os.path.exists(str_dir_dest):
            delete_dir("user-docs/"+str_directory)
    else:
        console.print(f"Error, user not found.", style='bad')


def restore_user(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "temp-user-docs", str(str_directory))
    str_dir_dest = os.path.join(str_cwd, "user-docs", str(str_directory))
    if os.path.exists(str_dir_curr):
        shutil.copytree(str_dir_curr, str_dir_dest)
        if os.path.exists(str_dir_dest):
            delete_dir("temp-user-docs/"+str_directory)
    else:
        console.print(f"Error, cannot restore deleted user.", style='bad')


def sort_dir(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs", str(str_directory))
    if os.path.exists(str_dir_curr):
        list_curr = os.listdir(str_dir_curr)
        set_ext = {os.path.splitext(item)[1][1:] for item in list_curr}
        # if they don't exist already, create files for each extension
        for ext in set_ext:
            if not os.path.exists(os.path.join(str_dir_curr, ext)):
                create_dir(os.path.join(str_directory, ext))
        # move each file based on extension
        for item in list_curr:
            str_ext = os.path.splitext(item)[1][1:]
            str_item_curr = os.path.join(str_dir_curr, item)
            str_item_dest = os.path.join(str_dir_curr, str_ext, item)
            if not os.path.exists(str_item_dest):
                shutil.move(str_item_curr, str_item_dest)
    else:
        console.print(f"Error, cannot find directory '{str_dir_curr}'", style="bad")


def unsort_dir(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs", str(str_directory))
    if os.path.exists(str_dir_curr):
        for item in os.listdir(str_dir_curr):
            str_item_curr = os.path.join(str_dir_curr, item)
            if os.path.isdir(str_item_curr):
                for item_nest in os.listdir(str_item_curr):
                    str_item_nest = os.path.join(str_item_curr, item_nest)
                    if os.path.isfile(str_item_nest):
                        shutil.move(str_item_nest, str_dir_curr)
                    if os.path.isdir(str_item_nest):
                        shutil.copytree(str_item_nest, str_dir_curr)
                        shutil.rmtree(str_item_nest)
                shutil.rmtree(str_item_curr)
    else:
        console.print(f"Error, cannot find directory '{str_dir_curr}'", style="bad")


def parse_log_file(str_directory):
    """"""
    list_curr = os.listdir(str_directory)
    for item in list_curr:
        if bool(re.search(f"\.log$",item)) and "errors" not in item and "warnings" not in item:
            list_error_lines = []
            list_warning_lines = []
            # open file extract lines with warnings and errors
            with open(os.path.join(str_directory, item), "r") as file:
                for line in file:
                    if "ERROR:" in line:
                        list_error_lines.append(line)
                    elif "WARNING:" in line:
                        list_warning_lines.append(line)
            # create log of errors
            str_filename_errors = f"{os.path.splitext(item)[0]}_errors.log"
            with open(os.path.join(str_directory, str_filename_errors), "w") as file:
                for line in list_error_lines:
                    file.write(line)
            # create log of warnings
            str_filename_warnings = f"{os.path.splitext(item)[0]}_warnings.log"
            with open(os.path.join(str_directory, str_filename_warnings), "w") as file:
                for line in list_warning_lines:
                    file.write(line)


def find_log_files(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs", str_directory)
    if os.path.exists(str_dir_curr):
        list_curr = os.listdir(str_dir_curr)
        # if the log files are nested directory, call parse function inside that nested directory
        for item in list_curr:
            if item == "log" and os.path.isdir(os.path.join(str_dir_curr, item)):
                parse_log_file(os.path.join(str_dir_curr, item))
        # if there are any log files in this directory, all parse function on this directory
        if any([True if bool(re.search(f"\.log$",item)) else False for item in list_curr]):
            parse_log_file(str_dir_curr)

    else:
        console.print(f"Error, cannot find directory '{str_dir_curr}'", style="bad")


if __name__ == "__main__":
    pass
    # testing creating directory
    # create_dir("delete_me")
    # delete_dir("delete_me")

    # testing deleting user
    # delete_user('user1')
    # restore_user('user1')

    # testing sorting of directory
    # sort_dir("user2")
    # unsort_dir("user2")

    # test parsing of log files
    # find_log_files("user2")