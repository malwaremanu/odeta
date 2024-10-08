import sqlite3, json, os, uuid
from ulid import ULID
from contextlib import contextmanager

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    @contextmanager
    def get_conn(self):
        db_path = self.db_name # os.path.join(os.path.dirname(__file__), self.db_name)
        self.conn = sqlite3.connect(db_path)
        try:
            yield self.conn
        finally:
            self.conn.close()

    @contextmanager
    def get_cursor(self):
        with self.get_conn() as conn:
            self.cursor = conn.cursor()
            try:
                yield self.cursor
            finally:
                self.cursor.close()

class odeta:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def __call__(self, table_name):
        return Table(self.db, table_name)

class Table:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name

    def fetchall(self, query=None):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"SELECT id, data FROM {self.table_name}")
            results = cursor.fetchall()
            parsed_results = [{'id': id, **json.loads(data)} for id, data in results]
            if query is None:
                return parsed_results
            else:
                filtered_results = []
                for result in parsed_results:
                    for key, value in query.items():
                        if "?contains" in key:
                            field = key.split("?")[0]
                            if value.lower() in result.get(field, "").lower():
                                filtered_results.append(result)
                                break
                        else:
                            if result.get(key) == value:
                                filtered_results.append(result)
                                break
                return filtered_results

    def fetch(self, query=None):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"SELECT id, data FROM {self.table_name}")
            results = cursor.fetchall()
            parsed_results = [{'id': id, **json.loads(data)} for id, data in results]
            if query is None:
                return parsed_results
            else:
                filtered_results = []
                for result in parsed_results:
                    match = True
                    for key, value in query.items():
                        if "?contains" in key:
                            field = key.split("?")[0]
                            if value.lower() not in result.get(field, "").lower():
                                match = False
                                break
                        else:
                            if result.get(key) != value:
                                match = False
                                break
                    if match:
                        filtered_results.append(result)
                return filtered_results

    def put(self, data):
        id = str(ULID())
        data_json = json.dumps(data)
        with self.db.get_cursor() as cursor:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data TEXT)")
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data_json))
            cursor.connection.commit()
        return { "id" : id, "msg" : "success" }

    def update(self, query, id):
        data_json = json.dumps(query)
        with self.db.get_cursor() as cursor:
            cursor.execute(f"SELECT id FROM {self.table_name} WHERE id = ?", (id,))
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data_json))
            else:
                cursor.execute(f"UPDATE {self.table_name} SET data = ? WHERE id = ?", (data_json, id))
            cursor.connection.commit()

    def delete(self, id):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
            cursor.connection.commit()

    def table_exists(self, cursor):
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,))
        return cursor.fetchone() is not None

def database(db_name):
    return odeta(db_name)

# # Usage in a Flask application
# from flask import Flask, request, jsonify
# import datetime

# app = Flask(__name__)
# db = database("your_database.db")

# @app.route('/', methods=['GET'])
# def your_endpoint():
#     table = db("your_table")
    
#     # table.put({
#     #     "msg" : "success at " + str(datetime.datetime.now()),
#     #     "test" : "ok"
#     # })

#     print(table.delete("01J3SZ4C1ZYR6N8X2AZ6A6CX8K"))

#     for a in table.fetchall():
#         print(table.delete(a["id"]))

#     # print(table.fetchall())

#     results = table.fetchall()
#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(debug=True)
