import mysql.connector

class Dbhandler(object):
    """docstring for Dbhandler"""
    def __init__(self):
        self.USERNAME = "root"
        self.PASSWORD = "root"
        self.DBNAME = "mobistore"

        self.db = mysql.connector.connect(
          host = "localhost",
          user = self.USERNAME,
          password = self.PASSWORD,
          database = self.DBNAME
        )

    def __del__(self):
        self.db.close()

    """
        Executes a DML query in the database
        Params:
            - query string to execute
        Returns:
            - True for success
    """
    def execute(self, query):
        try:
            print("Executing query: {}".format(query))
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()

            cursor.close()
        except Exception as e:
            print("Exception in execute")
            print(e)
            return False
        return True

    """
        Executes a DQL query in the database
        Params:
            - query string to execute
        Returns:
            - Result set for success
    """
    def fetch(self, query):
        try:
            print("Executing query: {}".format(query))
            cursor = self.db.cursor()
            cursor.execute(query)
            cols=[x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.close()

            results = []
            for row in rows:
                result = {}
                for col, val in zip(cols, row):
                    result[col] = val
                results.append(result)
        except Exception as e:
            print("Exception in fetch")
            print(e)
            results = []

        return results