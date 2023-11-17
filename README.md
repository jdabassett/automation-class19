# File Automation

### Author:
Jacob Bassett

### Date: 
11/16/2023

### Description:
This is a small records management commandline interface for the management of user records. It is not an exhaustive/complete application but does perform quite a few file operations.

### Testing
Run `pytest` in the terminal to test individual functions.

![unit tests](images/unit-tests.png)

### Tools
iniconfig==2.0.0
markdown-it-py==3.0.0
mdurl==0.1.2
packaging==23.2
pluggy==1.3.0
Pygments==2.16.1
pytest==7.4.3
rich==13.7.0

### Usage:
***In the terminal run `python automation/main.py` to start the application.***

![landing](images/1-landing.png)

***Navigate to the 'global' directory by typing `1` in the commandline.***

![global](images/2-global-landing.png)

***Leave the application by typing `0` in the commandline when prompted.***

![exit](images/3-exit.png)

***Entire a user's records by typing '1' in the commandline followed by a specification of the user.***

![choose user](images/4-choose-user.png)

***Delete a user's records by typing '2' in the commandline while in the 'global' directory followed by a specification of the user.***

![delete user](images/5-delete-user.png)

***Restore a user's records by typing '3' in the commandline while in the 'global' directory followed by a specification of the user.***

![restore user](images/6-restore-user.png)

***With a user's records, type '2' to create a new folder. You will be prompted for a file name.***

![create folder](images/7-new-folder.png)

***With a user's records, type '3' to delete folder. You will be prompted for a file name.***

![delete folder](images/8-delete-folder.png)

***With a user's records, type '4' to sort files into folders based on file extensions.***

![sort files](images/9-sort-files-by-extension.png)

***With a user's records, type '5' to unsort files out of folders.***

![unsort files](images/10-unsort-files-out-of-files.png)

***With a user's records, type '6' to parse log file into new error and warning log files.***

![parse log file](images/11-parse-log-file.png)