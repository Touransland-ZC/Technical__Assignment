# Technical__Assignment
Implementing option 1: a command-line program for File Organizer
It organizes files in a folder into Images, Documents, Videos, Audio, Archives, eBooks, and Others based on extension
The categories include Images, Documents, Videos, Audio, Archives, eBooks, and Others based on extension, handling the no extension files and the multi-extension files.

It shows a summary with counts per category.
It shows an optional pie chart.
It has a simulation-only mode.
It shows each file name is moved to which category.
There is a safe destination name that prevents overwrites.
Test coverage ≈ 99%.




HOW TO RUN:
You can find a Colab Notebook, named FileOrganizer.ipynb, which includes the project code & the test coverage, both with their outputs, and you can find comments explaining each function

The function Run() is for running the file organizer.
1) It asks the user about the folder source, whether from Google Drive or the PC.
Note: Google Colab can't modify folders on the pc directly; hence, you will upload your files to the VM storage, then organize them.
2) After choosing the source, enter its path.
3) You will be asked if you want to simulate only or organize your folder.
4) You will be asked if you want a pie chart representing the ratio between the categories.
5) There will be a summary representing the number of files per category.
6) If you select to move the files, then after each move, you will know each file name will be at which category folder.


Language and tools
Python 3.11
Matplotlib
Pytest, pytest-cov
Google Colab
