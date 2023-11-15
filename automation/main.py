import os
import shutil
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
        str_dir_path = os.path.join(str_cwd, str(str_directory))
        os.makedirs(str_dir_path)
        # console.print(f"Directory '{str_directory}' was created", style="good")
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
            # console.print(f"Directory '{str_directory}' was deleted.", style="good")
        else:
            print(f"Target directory '{str_directory}' doesn't exists.")
    except OSError as e:
        console.print(f"Error deleting directory '{str_directory}': {e}", style='bad')


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
        console.print(f"Error user not found.", style='bad')


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
        console.print(f"Error cannot restore deleted user.", style='bad')



if __name__ == "__main__":
    # create_dir("delete_me")
    # delete_dir("delete_me")
    # console.print(os.listdir("."))
    # delete_user('user1')
    restore_user('user1')