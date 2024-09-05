from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Now db is imported from extensions
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beer_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and login manager
db.init_app(app)  # Initialize db here
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Flask-Migrate for handling migrations
migrate = Migrate(app, db)

# User loader for login manager
@login_manager.user_loader
def load_user(manager_id):
    return Manager.query.get(int(manager_id))

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        manager = Manager.query.filter_by(username=username).first()

        if manager and check_password_hash(manager.password, password):
            login_user(manager)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    items = Item.query.all()
    return render_template('dashboard.html', items=items)

# Route to create a bill
@app.route('/create_bill', methods=['POST'])
@login_required
def create_bill():
    customer_name = request.form['customer_name']
    items_str = request.form['items']  # Comma-separated items (e.g., "Beer1,Beer2")
    total_amount = float(request.form['total_amount'])

    items_list = items_str.split(',')
    insufficient_stock = []

    # Update inventory
    for item_name in items_list:
        item = Item.query.filter_by(name=item_name).first()
        if item:
            if item.quantity > 0:
                item.quantity -= 1  # Decrease stock by 1 for each sale
            else:
                insufficient_stock.append(item_name)
        else:
            flash(f"Item '{item_name}' not found in inventory.")
        db.session.commit()

    if insufficient_stock:
        flash(f"Insufficient stock for: {', '.join(insufficient_stock)}")
        return redirect(url_for('dashboard'))

    # Create a new bill
    new_bill = Bill(customer_name=customer_name, items=items_str, total_amount=total_amount)
    db.session.add(new_bill)
    db.session.commit()

    flash("Bill created successfully!")
    return redirect(url_for('dashboard'))

# Route to add a new item to the inventory
@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    new_item = Item(name=name, price=price, quantity=quantity)
    db.session.add(new_item)
    db.session.commit()

    flash("Item added successfully!")
    return redirect(url_for('dashboard'))

# Route to logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# Import models AFTER initializing db to avoid circular import issues
from models import Manager, Item, Bill

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
