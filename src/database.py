import sqlite3 as sql
from sqlite3 import Error
import pandas as pd
import logging

# initialise logger for this script
logger = logging.getLogger()

class SQLDatabase:
    # class to initialise and create a sqllite3 db for our data
    # input: path to data and database name and table name
    def __init__(self, data_path, data_basename, table_name):
        self.data_path = data_path
        self.data_basename = data_basename
        self.table_name = table_name

    def create_database(self):
        # function to create sqllite3 db and table
        # no output
        try:
            # read data from file and ensure that dates are read correctly
            my_date_parser = lambda x: pd.datetime.strptime(x, "%d/%m/%Y")
            data = pd.read_csv(self.data_path, parse_dates=['Date'], date_parser=my_date_parser)

            # create weekday column
            data['Weekday'] = data.Date.apply(lambda x: x.strftime('%A'))

            # connect to database
            conn = sql.connect(self.data_basename)

            # upload data to databse
            data.to_sql(self.table_name, conn)

            # log success
            logger.info("Database {0} and table {1} have been successfully created.".format(self.data_basename, self.table_name))

        except Error as e:
            # log error
            logger.error("The following database error has occurred: {0}.".format(e))

    def create_connection(self):
        # function to connect to created db
        # output: sqllite3 db object
        try:
            # connect to database
            conn = sql.connect(self.data_basename)

            # log success
            logger.info("Connection to database {0} was successful.".format(self.data_basename))

            return conn

        except Error as e:
            # log error
            logger.error("The following database error has occurred: {0}.".format(e))
