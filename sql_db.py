# import aiosqlite
# class Database:
#     def __init__(self, path_to_db="main.db"):
#         self.path_to_db = path_to_db

#     async def get_connection(self):
#         return await aiosqlite.connect(self.path_to_db)

#     async def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False):
#         if not parameters:
#             parameters = ()
#         async with await self.get_connection() as conn:
#             cursor = await conn.cursor()
#             data = None
#             await cursor.execute(sql, parameters)
#             if fetchall:
#                 data = await cursor.fetchall()
#             if fetchone:
#                 data = await cursor.fetchone()
#             await conn.commit()
#             return data

#     async def create_table_users(self):
#         sql = """
#             CREATE TABLE IF NOT EXISTS Users (
#                 id INTEGER NOT NULL,
#                 first_name TEXT NULL,
#                 last_name TEXT NULL,
#                 username TEXT NULL,
#                 added_members_count INTEGER DEFAULT 0,
#                 PRIMARY KEY (id)
#             );
#             """
#         await self.execute(sql)

#     @staticmethod
#     def format_args(sql, parameters: dict):
#         sql += " AND ".join([
#             f"{item} = ?" for item in parameters
#         ])
#         return sql, tuple(parameters.values())

#     async def add_user(self, id: int, first_name: str, last_name: str = None, username: str = None):
#         sql = """
#         INSERT INTO Users(id, first_name, last_name, username) VALUES(?, ?, ?, ?)
#         """
#         await self.execute(sql, parameters=(id, first_name, last_name, username))

#     async def select_all_users(self):
#         sql = """
#         SELECT * FROM Users
#         """
#         return await self.execute(sql, fetchall=True)

#     async def select_user(self, **kwargs):
#         sql = "SELECT * FROM Users WHERE"
#         sql, parameters = self.format_args(sql, kwargs)
#         return await self.execute(sql, parameters=parameters, fetchone=True)

#     async def count_users(self):
#         return await self.execute("SELECT COUNT(*) FROM Users", fetchone=True)

#     async def delete_users(self):
#         await self.execute("DELETE FROM Users WHERE TRUE")

#     async def get_top_member_added_users(self):
#         sql = """
#         SELECT * FROM Users
#         ORDER BY added_members_count DESC
#         LIMIT 10
#         """
#         return await self.execute(sql, fetchall=True)

#     async def add_member_count(self, id):
#         sql = """
#         UPDATE Users
#         SET added_members_count = added_members_count + 1
#         WHERE id = ?
#         """
#         await self.execute(sql, parameters=(id,))

#     async def get_or_create(self, table, defaults=None, **kwargs):
#         sql = f"SELECT * FROM {table} WHERE "
#         sql, parameters = self.format_args(sql, kwargs)

#         # Check if a record exists
#         record = await self.execute(sql, parameters=parameters, fetchone=True)

#         if not record:
#             # No record found, create a new one
#             if not defaults:
#                 defaults = {}
#             # Use f-strings for cleaner and safer string formatting
#             sql = f"""
#             INSERT INTO {table} ({', '.join(defaults.keys())})
#             VALUES ({', '.join(['?'] * len(defaults))})
#             """
#             await self.execute(sql, parameters=tuple(defaults.values()))
#             # Return the newly created record (assumed to be returned by execute)
#             new_record = await self.select_user(**kwargs)
#             return new_record, True
#         else:
#             # Record found, return it
#             return record, False




import sqlite3
class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER NOT NULL,
                first_name TEXT NULL,
                last_name TEXT NULL,
                username TEXT NULL,
                added_members_count INTEGER DEFAULT 0,
                PRIMARY KEY (id)
            );
            """
        self.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, first_name: str, last_name: str = None, username: str = None):
        sql = """
        INSERT INTO Users(id, first_name, last_name, username) VALUES(?, ?, ?, ?)
        """
        return self.execute(sql, parameters=(id, first_name, last_name, username))

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def get_top_member_added_users(self):
        sql = """
        SELECT * FROM Users
        ORDER BY added_members_count DESC
        LIMIT 10
        """
        return self.execute(sql, fetchall=True)

    def add_member_count(self, id, number=1):
        add_member_sql = """
        UPDATE Users
        SET added_members_count = added_members_count + ?
        WHERE id = ?
        """
        conn = sqlite3.connect(self.path_to_db)
        cursor = conn.cursor()
        cursor.execute(add_member_sql, (number, id))
        conn.commit()
        conn.close()

    def get_or_create(self, user):
        try:
            conn = sqlite3.connect(self.path_to_db)
            cursor = conn.cursor()
            # Insert the user if it doesn't exist
            cursor.execute("INSERT OR IGNORE INTO Users (id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                        (user['id'], user['first_name'], user['last_name'], user['username']))
            
            # Commit changes and close the connection
            conn.commit()
            conn.close()
            return "User added successfully!"
        except sqlite3.Error as e:
            return f"Error: {e}"

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")