# IEEE_AU

A repository to develop code for basic tasks in IEEE student chapter of Ahmedabad University

## Requirements

- Python 3.12+ should be installed and on system path
- MySQL 8 should be installed

## Setup

- Clone the repository into your local machine

- Create a .env file in your project directory

- In the .env file set the following credentials of your database
  - HOST =
  - USER =
  - PASSWORD =
  - DATABASE =

## Setting Up the Virtual Environment

To set up the virtual environment kindly follow these steps

- Open the directory where the main.py file is stored.

- Run the following command on the command line  
  `python -m venv .venv`  
  This will create a virtual environment in your project folder.

- After .venv folder is created, run the following command
  - On windows  
    `.venv/Scripts/activate`  
  - On MacOS / Linux  
    `source .venv/Scripts/activate`

- This will activate the virtual environment and allow the project to use the packages installed within this environment. It   will look something like this  
  `(.venv) directory/in/which/.venv/is/located`

- Upon activating the virtual environment, to install all dependencies, run the following command  
  `pip install -r requirements.txt`  
  This will install all the required dependencies mentioned in the requirements.txt file into the lib folder of the virtual environment

- You can now use the environment as you please. Once you are done tinkering with the environment, to close it simply run `deactivate` on the terminal and the virtual environment will be deactivated.

## Adding a New Library

It can be that during development, a new 3rd party library might be needed. This section details the steps to add this library.

- Open the directory in which the virtual environment is located. Activate the virtual environment by running the command
  - On windows  
    `.venv/Scripts/activate`  
  - On MacOS / Linux  
    `source .venv/Scripts/activate`

- This will activate the virtual environment and allow the project to use the packages installed within this environment. It   will look something like this  
  `(.venv) directory/in/which/.venv/is/located`

- Then install the third party library using pip  
  `pip install package(s)`

- After the packages are installed, run the following command  
  `pip freeze > requirements.txt`

- This will update the requirements.txt file with any new package that might have been installed in the virtual environment and allow other people to install the same dependency when trying to tinker with the code in future.
