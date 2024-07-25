import sqlite3, json, uuid
from threading import local

class odeta:
    def __init__(self, db_name):
        self.db_name = db_name
        self.local = local()

    def get_conn(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_name)
        return self.local.conn

    def get_cursor(self):
        if not hasattr(self.local, 'cursor'):
            self.local.cursor = self.get_conn().cursor()
        return self.local.cursor

    def table(self, table_name):
        return Table(self.get_conn(), self.get_cursor(), table_name)

class Table:
    def __init__(self, conn, cursor, table_name):
        self.conn = conn
        self.cursor = cursor
        self.table_name = table_name

    def fetch(self, query=None):
        if not self.table_exists():
            return []
        self.cursor.execute(f"SELECT id, data FROM {self.table_name}")
        results = self.cursor.fetchall()
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

    def put(self, data):
        id = str(uuid.uuid4())
        data_json = json.dumps(data)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data TEXT)")
        self.cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data_json))
        self.conn.commit()
        return id

    def update(self, query, id):
        data_json = json.dumps(query)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data TEXT)")        
        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE id = ?", (id,))
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data_json))
        else:
            self.cursor.execute(f"UPDATE {self.table_name} SET data = ? WHERE id = ?", (data_json, id))
        self.conn.commit()


    def delete(self, id):
        if not self.table_exists():
            return []
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
        self.conn.commit()

    def table_exists(self):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,))
        return self.cursor.fetchone() is not None

# # -------------------------------------
# import sqlite3, json, uuid

# class odeta:
#     def __init__(self, db_name):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()

#     def table(self, table_name):
#         return Table(self.conn, self.cursor, table_name)

# class Table:
#     def __init__(self, conn, cursor, table_name):
#         self.conn = conn
#         self.cursor = cursor
#         self.table_name = table_name

#     def fetch(self, query=None):
#         if not self.table_exists():
#             return []
#         self.cursor.execute(f"SELECT id, data FROM {self.table_name}")
#         results = self.cursor.fetchall()
#         parsed_results = [{'id': id, **json.loads(data)} for id, data in results]
#         if query is None:
#             return parsed_results
#         else:
#             filtered_results = []
#             for result in parsed_results:
#                 for key, value in query.items():
#                     if "?contains" in key:
#                         field = key.split("?")[0]
#                         if value.lower() in result.get(field, "").lower():
#                             filtered_results.append(result)
#                             break
#                     else:
#                         if result.get(key) == value:
#                             filtered_results.append(result)
#                             break
#             return filtered_results


#     def put(self, data):
#         id = str(uuid.uuid4())
#         data_json = json.dumps(data)
#         self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data TEXT)")
#         self.cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data_json))
#         self.conn.commit()
#         return id

#     def update(self, query, id):
#         data_json = json.dumps(query)
#         self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data TEXT)")        
#         self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE id = ?", (id,))
#         if self.cursor.fetchone() is None:
#             self.cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data_json))
#         else:
#             self.cursor.execute(f"UPDATE {self.table_name} SET data = ? WHERE id = ?", (data_json, id))
#         self.conn.commit()

#     def delete(self, id):
#         if not self.table_exists():
#             return []
#         self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
#         self.conn.commit()        

#     def table_exists(self):        
#         self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,))
#         return self.cursor.fetchone() is not None
    

# # db = odeta("my_database.db")
# # users = db.table("users")

# # print(users.fetch())
# # print(users.fetch({"name" : "Bob Johnson"}))
