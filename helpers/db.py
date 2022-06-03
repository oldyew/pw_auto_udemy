import sqlite3

class DataBase:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)

    def list_test_cases(self):
        c = self.connection.cursor()
        c.execute('select * from tcm_testcase')
        return c.fetchall()

    def delete_test_case(self, test_name: str):
        c = self.connection.cursor()
        c.execute('delete from tcm_testcase where name=?', (test_name,))
        self.connection.commit()

    def close(self):
        self.connection.close()