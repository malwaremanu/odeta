from odeta import db

db = db("users.db")
users = db.table("users")

print(users.fetch())