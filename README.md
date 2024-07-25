# OdetA

A simple NoSQL-like interface for SQLite.

## Installation

```bash
pip install odeta
'''

## Usages

'''
from odeta import NoSqlite

db = NoSqlite("my_database.db")
users = db.table("users")

print(users.fetch())
print(users.fetch({"name" : "Bob Johnson"}))
'''
