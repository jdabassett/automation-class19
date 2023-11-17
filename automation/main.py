import os
import shutil
import re
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.table import Table

automation_theme = Theme({
    'good': "green",
    'okay': "bold yellow",
    "bad": "bold underline red",
    "prompt":"bold green"
})

console = Console(theme=automation_theme)

dict_prompts = {
    "global": {
        "prompts": ['\nThere are several actions that you could make.','0: Exit Application.', '1: Choose a user records to move into.', '2: Delete user records.', '3: Restore user records.','Select action by number only'],
        "inputs": ['0', '1', '2', '3'],
        "default": "1",
    },
    "user": {
        "prompts": ['\nThere are several actions that you could make.','0: Exit application.', '1: Choose a user records to move into.', '2: Create a folder in user records.', '3: Delete a folder in user records.', '4: Sort user files into folders by extensions.', '5: Unsort user files out of folders.', '6: Parse user logs into user error and warning logs.', 'Select action by number only'],
        "inputs": ['0', '1', '2', '3', '4', '5', '6'],
        "default": "0",
    },
    "restore": {
        "prompts": ['\nThese are the deleted user records we have on standby. Which would you like to restore?', 'Select action by number only'],
        "default": "0",
    },
    "users": {
        "prompts": ["\nWhat directory do you want select?",'Select action by number only'],
        "default": "0",
    },
}


def create_dir(str_directory: str):
    """"""
    try:
        str_cwd = os.getcwd()
        str_dir_path = os.path.join(str_cwd, "user-docs", str(str_directory))
        os.makedirs(str_dir_path)
        console.print(f"Directory '{str_directory}' created.", style="good")
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
        str_dir_path = os.path.join(str_cwd, "user-docs", str(str_directory))
        if os.path.exists(str_dir_path):
            shutil.rmtree(str_dir_path)
            console.print(f"\nDirectory '{str_directory}' was deleted.", style="good")
        else:
            console.print(f"\nTarget directory '{str_directory}' doesn't exists.", style="bad")
    except OSError as e:
        console.print(f"\nError, deleting directory '{str_directory}': {e}", style='bad')


def delete_user(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "user-docs", str(str_directory))
    str_dir_dest = os.path.join(str_cwd, "temp-user-docs")
    if os.path.exists(str_dir_curr):
        if os.path.exists(os.path.join(str_dir_dest, str_directory)):
            delete_dir(os.path.join(str_dir_dest, str_directory))
        shutil.move(str_dir_curr, str_dir_dest)
        console.print(f"\nUser '{str_directory}' was deleted.", style="good")
    else:
        console.print(f"\nError, user not found.", style='bad')


def restore_user(str_directory: str):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, "temp-user-docs", str(str_directory))
    str_dir_dest = os.path.join(str_cwd, "user-docs")
    if os.path.exists(str_dir_curr):
        if os.path.exists(os.path.join(str_dir_dest, str_directory)):
            console.print(f"\nError, cannot restore {str_directory}, current user already exists with same name.", style='yellow')
        else:
            shutil.move(str_dir_curr, str_dir_dest)
            console.print(f"\nDirectory '{str_directory}' was restored.", style="good")
    else:
        console.print(f"\nError, cannot restore deleted user.", style='bad')


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
        console.print(f"\nDirectory '{str_directory}' was properly sorted.", style="good")
    else:
        console.print(f"\nError, cannot find directory '{str_dir_curr}'", style="bad")


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
        console.print(f"\nDirectory '{str_directory}' was properly unsorted.", style="good")
    else:
        console.print(f"\nError, cannot find directory '{str_dir_curr}'", style="bad")


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
        console.print(f"\nDirectory '{str_directory}' log files were properly parsed and new ERROR and WARNING files created.",
                      style="good")
    else:
        console.print(f"\nError, cannot find directory '{str_dir_curr}'", style="bad")


def prompt_user(list_options, list_inputs, str_default) -> str:
    """"""
    str_command = Prompt.ask("\n".join(list_options), choices=list_inputs, default=str_default, show_choices=False, show_default=False)
    return str_command


def choose_user(str_type: str = "") -> str:
    """"""
    str_cwd = os.getcwd()
    if str_type == "delete":
        list_users = ["cancel", *sorted(os.listdir(os.path.join(str_cwd, "user-docs")))]
    else:
        list_users = ["global", *sorted(os.listdir(os.path.join(str_cwd, "user-docs")))]
    list_users_display = [f"{index}: {item}" for index, item in enumerate(list_users)]
    list_users_input = [f"{index}" for index, item in enumerate(list_users)]
    dict_users = dict_prompts['users']
    list_prompts = [dict_users['prompts'][0], *list_users_display, dict_users['prompts'][-1]]
    str_number = prompt_user(list_prompts, list_users_input, dict_users['default'])
    return list_users[int(str_number)]


def prompt_restore_user() -> str:
    """"""
    str_cwd = os.getcwd()
    list_temp = ["cancel", *sorted(os.listdir(os.path.join(str_cwd, "temp-user-docs")))]
    list_temp_display = [f"{index}: {item}" for index, item in enumerate(list_temp)]
    list_temp_input = [f"{index}" for index, item in enumerate(list_temp)]
    dict_restore = dict_prompts['restore']
    list_prompts = [dict_restore['prompts'][0], *list_temp_display, dict_restore['prompts'][-1]]
    str_number = prompt_user(list_prompts, list_temp_input, dict_restore["default"])
    return list_temp[int(str_number)]


def display_table(str_user_or_temp: str = "user-docs", str_directory: str = ""):
    """"""
    str_cwd = os.getcwd()
    str_dir_curr = os.path.join(str_cwd, str_user_or_temp, str_directory)
    list_curr = sorted(os.listdir(str_dir_curr))
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Type", style="green", width=20)
    table.add_column("Name", style="green", width=30)
    for item in list_curr:
        str_item_type = "folder" if os.path.isdir(os.path.join(str_dir_curr, item)) else "file"
        table.add_row(str_item_type, item)
    console.print(table)


def main():
    """"""
    console.print("Welcome to the User Management Application Mainline Interface (UMAMI).", style="good")
    console.print("With this app, you will be able to manage our user records.", style="good")
    str_user = choose_user()
    while True:
        # choosing one action
        console.print(f"\nCurrently in the {str_user} directory, here are its contents.", style="good")
        if str_user == "global":
            display_table()
            dict_user = dict_prompts['global']
            str_command = prompt_user(dict_user['prompts'], dict_user['inputs'], dict_user['default'])
        else:
            display_table("user-docs", str_user)
            dict_user = dict_prompts['user']
            str_command = prompt_user(dict_user['prompts'], dict_user['inputs'], dict_user['default'])

        # if exiting
        if str_command == "0":
            console.print("\nLeaving UMAMI!", style="good")
            str_command = 'break'

        # moving from user to user
        elif str_command == "1":
            str_user = choose_user()

        # delete user records
        elif str_command == "2" and str_user == "global":
            str_delete_user = choose_user("delete")
            if str_delete_user == "cancel":
                str_delete_user =""
                continue
            else:
                str_confirmation = prompt_user([f"\nAre you sure that you want to delete {str_delete_user}.", "0: No", "1: Yes", "Select action by number only"],["0", "1"], "0")
                if str_confirmation == "1":
                    delete_user(str_delete_user)

        # restoring user records
        elif str_command == "3" and str_user == "global":
            console.print(f"\nCurrently in the disabled user directory.", style="good")
            display_table("temp-user-docs", "")
            str_restore_user = prompt_restore_user()
            if str_restore_user == "cancel":
                str_restore_user = ""
                continue
            else:
                restore_user(str_restore_user)

        # allow user to create folder
        elif str_command == "2" and str_user != "global":
            print("\n")
            str_create_folder = Prompt.ask(r'What is the folder name? (illegal characters: \ / : * ? " < > |)')
            if bool(re.search(r'[^/\\:*?"<>|]', str_create_folder)):
                create_dir(f"{str_user}/{str_create_folder}")
            else:
                console.print(f"Sorry {str_create_folder} name not allows. Please try again.", style='bad')

        # allow user to delete folder
        elif str_command == "3" and str_user != "global":
            str_cwd = os.getcwd()
            list_curr = ["cancel", *sorted(os.listdir(os.path.join(str_cwd, "user-docs", str_user)))]
            list_curr_display = [f"{index}: {item}" for index, item in enumerate(list_curr)]
            list_curr_input = [f"{index}" for index, item in enumerate(list_curr)]
            list_display = ["\nWhat folder would you like to delete?", *list_curr_display, "elect action by number only"]

            str_delete_folder = prompt_user(list_display, list_curr_input, "0")

            print("delete directory", str_delete_folder)

            if str_delete_folder == "0":
                str_delete_user = ""
                continue
            else:
                delete_dir(f"{str_user}/{list_curr[int(str_delete_folder)]}")

        # allow user to nest files into directories based on extension
        elif str_command == "4" and str_user != "global":
            sort_dir(str_user)

        # allow user to unnest files into directories based on extension
        elif str_command == "5" and str_user != "global":
            unsort_dir(str_user)

        # allow user to parse log files into error and warning log files
        elif str_command == "6" and str_user != "global":
            find_log_files(str_user)

        # break out of application or continue
        if str_command == "break":
            break
        else:
            str_command = ""


if __name__ == "__main__":
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

    # testing main application
    main()