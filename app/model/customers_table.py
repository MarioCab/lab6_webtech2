from flask import abort
import sqlite3
from model.database import get_db


class CustomersTable:

    @staticmethod
    def get():
        """Gets all rows from the customers table.

            If the database operations raise a sqlite3.Error, the method is 
            aborted with the status code 500.

        Returns:
            list: a list of all rows; each row is a dictionary that maps
                column names to values. An empty list is returned if the 
                table has no columns.
        """
        try:
            db = get_db()
            result = db.execute("SELECT * FROM CUSTOMERS ORDER BY LastName")
            customers = result.fetchall()
            customers = [dict(customer) for customer in customers]
            return customers
        except sqlite3.Error as error:
            print("ERROR: " + str(error))
            abort(500)


    @staticmethod
    def get_by_id(customer_id):
        """Gets the row with the specified id from the customers table
            
            If the database operations raise a sqlite3.Error, the method is 
            aborted with the status code 500.

        Args:
            customer_id (int): the id of the customer to be returned

        dict: the customer with the specified customer id; None if no such
            customer exists
        """
        try:
            db = get_db()
            query = "SELECT * FROM CUSTOMERS WHERE CustomerID = ?"
            data = [customer_id]
            result = db.execute(query, data)
            customer = result.fetchone()
            if customer is not None:
                customer = dict(customer)
            return customer
        except sqlite3.Error as error:
            print("ERROR: " + str(error))
            abort(500)
