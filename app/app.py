from flask import Flask, request, redirect, render_template, url_for, session
from model.database import close_db
from model.categories_table import CategoriesTable
from model.products_table import ProductsTable
from model.customers_table import CustomersTable
from model.admins_table import AdminsTable


app = Flask(__name__)
app.config["SECRET_KEY"] = "this is the secret string"


@app.errorhandler(404)
def page_not_found(error):
    """Returns a 404-error message page

    Args:
        error (werkzeug.exception.NotFound): error object

    Returns:
        Response: 404-error message page
    """
    return render_template("errors/404.jinja"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Returns a 500-error message page

    Args:
        error (werkzeug.exceptions.InternalServerError): error object

    Returns:
        Response: 500-error message page
    """
    return render_template("errors/500.jinja"), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    """ "Handles GET and POST requests for login
        GET: Returns the login page
        POST: Authenticates the user data specified in the JSON payload

    Returns:
        Response: the homepage if the user is successfully authenticated.
            Otherwise, the login page.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not AdminsTable.isValidLogin(username, password):
            error = "Invalid username or password."
            return render_template("login.jinja", error=error)
        session["logged_in"] = True
        return redirect(url_for("home"))
    else:
        return render_template("login.jinja")


@app.route("/logout")
def logout():
    """Logs the user out

    Returns:
        Response: the homepage
    """
    session["logged_in"] = False
    return redirect(url_for("home"))


@app.route("/")
@app.route("/index")
def home():
    """Returns the homepage

    Returns:
        Response: the homepage
    """
    return render_template("index.jinja")


@app.route("/product")
def product_list():
    """Returns a page listing all products of the category specified
        as query string parameter

    Returns:
        Response: the product page
    """
    if "logged_in" not in session or not session["logged_in"]:
        return app.redirect(url_for("login"))

    # determine the selected category
    category_id_string = request.args.get("category_id")
    categories = CategoriesTable.get()
    if category_id_string and category_id_string.isdigit():
        category_id = int(category_id_string)
        if CategoriesTable.get_by_id(category_id) is None:
            category_id = categories[0]["CategoryID"]
    else:
        category_id = categories[0]["CategoryID"]

    products = ProductsTable.get_by_category_id(category_id)
    category = CategoriesTable.get_by_id(category_id)
    category_name = category["CategoryName"]

    return render_template(
        "product_list.jinja",
        category_name=category_name,
        categories=categories,
        products=products,
    )


@app.route("/delete_category", methods=["POST"])
def delete_category():
    """Removes a category from the database

    Returns:
        Response: an error message if the category cannot be deleted because it contains products.
    """
    if "logged_in" not in session or not session["logged_in"]:
        return redirect(url_for("login"))

    category_id = request.form["category_id"]
    products = ProductsTable.get_by_category_id(category_id)
    if products:
        error = "The category cannot be deleted since it contains products."
        categories = CategoriesTable.get()
        return render_template(
            "category_list.jinja", categories=categories, error=error
        )

    CategoriesTable.delete(category_id)
    return redirect(url_for("category_list"))


@app.route("/delete_product", methods=["POST"])
def delete_product():
    """Removes the product specified in the JSON payload

    Returns:
        Response: the product page
    """
    if "logged_in" not in session or not session["logged_in"]:
        return redirect(url_for("login"))

    category_id = request.form["category_id"]
    product_id = request.form["product_id"]
    ProductsTable.delete(product_id)
    return redirect(url_for("product_list", category_id=category_id))


@app.route("/category", methods=["GET", "POST"])
def category_list():
    """Handles GET and POST requests for category
        GET: Returns a page listing all categories
        POST: Adds the category specified in the JSON payload

    Returns:
        Response: the category page
    """
    if "logged_in" not in session or not session["logged_in"]:
        return redirect(url_for("login"))

    if request.method == "POST":
        category_name = request.form["category_name"]
        if not category_name:
            emptyError = "Category name cannot be empty."
            categories = CategoriesTable.get()
            return render_template(
                "category_list.jinja", categories=categories, emptyError=emptyError
            )
        elif CategoriesTable.get_by_name(category_name):
            existsError = "Category name exists already."
            categories = CategoriesTable.get()
            return render_template(
                "category_list.jinja", categories=categories, existsError=existsError
            )
        else:
            category_data = {"category_name": category_name}
            CategoriesTable.insert(category_data)
            return redirect(url_for("category_list"))

    categories = CategoriesTable.get()
    error = request.args.get("error")
    return render_template("category_list.jinja", categories=categories, error=error)


@app.route("/customer")
def customer_list():
    """Returns a page listing all customers

    Returns:
        Response: the customer page
    """
    if "logged_in" not in session or not session["logged_in"]:
        return app.redirect(url_for("login"))

    customers = CustomersTable.get()
    return render_template("customer_list.jinja", customers=customers)


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection

    Args:
        exception (sqlite3.Error): The error raised if the close operation fails;
            Otherwise, None.
    """
    close_db()
