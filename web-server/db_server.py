import sqlite3

con = sqlite3.connect('web_server.db')

cur = con.cursor()

# cur.execute('''DROP TABLE users''')
# cur.execute('''DROP TABLE roles''')
# cur.execute('''CREATE TABLE users (user_id integer, username char, password char, user_role integer)''')
# cur.execute('''CREATE TABLE roles (role_id integer, role_name char)''')

# s3cr3t, password, qwerty
# values = [(1, 'admin', '4e738ca5563c06cfd0018299933d58db1dd8bf97f6973dc99bf6cdc64b5550bd', 1),
#           (2, 'user_1', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 2),
#           (3, 'user_2', '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5', 2)]
#
# cur.executemany('''INSERT INTO users VALUES (?,?,?,?)''', values)

# roles = [(1, 'Administrator'), (2, 'User')]
# cur.executemany('''INSERT INTO roles VALUES(?, ?)''', roles)

for row in cur.execute('''SELECT * FROM roles'''):
    print(row)

# con.commit()
