from flask import abort
import sqlite3
from argon2 import PasswordHasher
from model.database import get_db

class AdminsTable:
    
    @staticmethod
    def insert(username, password):
        """Inserts the specified user into the admins table.

            If the database operation raises a sqlite3.Error, an error messgae is printed

        Args:
            username (str): the username of the admin to be inserted; 
            password (str): the password of the admin to be inserted; 

        Returns:
            None
        """
        password_hasher = PasswordHasher()
        hashed_password = password_hasher.hash(password)
        try:
            db = get_db()
            query = """
                INSERT INTO ADMINS (Username, Password) 
                VALUES (?, ?)
            """
            data = [username, hashed_password]
            db.execute(query, data)
            db.commit()
        except sqlite3.Error as error:
            print("ERROR: " + str(error))


    staticmethod
    def update_password(username, password):
        """Updates the password of the admin with the specifiesd username

            If the database operation raises a sqlite3.Error, an error messgae is printed

        Args:
            username (str): the username of the admin;
            password (str): the password of the admin to be updated; 

        Returns:
            None
        """
        print("in update table")
        password_hasher = PasswordHasher()
        hashed_password = password_hasher.hash(password)
        try:
            db = get_db()
            query = """
                UPDATE ADMINS 
                SET password = ?
                WHERE username = ?
            """
            data = [hashed_password, username]
            db.execute(query, data)
            db.commit()
        except sqlite3.Error as error:
            print("ERROR: " + str(error))


    @staticmethod
    def get_password(username):
        """Gets the row with the specified id from the products table.

            If the database operations raise a sqlite3.Error, the method is 
            aborted with the status code 500.

        Args:
            product_id (int): the id of the product to be returned

        Returns:
            dict: the product with the specified product id; None if no such
                product exists
        """
        try:
            db = get_db()
            query = "SELECT Password FROM ADMINS WHERE Username = ?"
            data = [username]
            result = db.execute(query, data)
            password_row = result.fetchone()
            if password_row is not None:
                password = dict(password_row)["Password"]
                return password
            else:
                return None
        except sqlite3.Error as error:
            print("ERROR: " + str(error))
            abort(500)


    @staticmethod
    def isValidLogin(username, password):
        """validates the specified user credentials

        Args:
            username (str): the username
            password (str): the unencrypted password

        Returns:
            bool: True if the specified username is contained in the admin table with 
                the specified password; False, otherwise.
        """
        hashed_password = AdminsTable.get_password(username)
        if hashed_password is None:
            return False
        try:
            password_hasher = PasswordHasher()
            password_hasher.verify(hashed_password, password)
            if password_hasher.check_needs_rehash(hashed_password):
                AdminsTable.update_password(username, password)
            return True
        except:
            return False