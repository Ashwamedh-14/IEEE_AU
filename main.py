from mysql.connector import  errors, cursor, connect
from pickle import load
def main():
    with open("cred.dat", 'rb') as myfile:
        data: dict = load(myfile)
        con = connect(host = data['host'],
                      user = data['user'],
                      password = data['password'],
                      database = data['database'])
    con.close()


if __name__ == '__main__':
    main()