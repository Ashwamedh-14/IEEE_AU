# IEEE_AU

A repository to develop code for basic tasks in IEEE student chapter of Ahmedabad University

## Requirements

- Python 3.12+ should be installed
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
  > - On windows  
    `.venv/Scripts/activate`  
  > - On MacOS / Linux  
    `source .venv/Scripts/activate`

- This will activate the virtual environment and allow the project to use the packages installed within this environment. It   will look something like this  
  `(.venv) directory/in/which/.venv/is/located`

- Upon activating the virtual environment, to install all dependencies, run the following command  
  `pip install -r requirements.txt`  
  This will install all the required dependencies mentioned in the requirements.txt file into the lib folder of the virtual environment

- You can now use the environment as you please. Once you are done tinkering with the environment, to close it simply run `deactivate` on the terminal and the virtual environment will be deactivated.
