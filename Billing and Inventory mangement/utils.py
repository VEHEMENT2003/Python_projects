from flask_mail import Message
from app import app, db
from models import Item, Bill
from datetime import datetime

def send_daily_report():
    bills = Bill.query.filter(Bill.date >= datetime.now().date()).all()
    items = Item.query.all()

    report = f"Today's Sales:\n"
    for bill in bills:
        report += f"Customer: {bill.customer_name}, Items: {bill.items}, Total: {bill.total_amount}\n"

    inventory = f"\nCurrent Inventory:\n"
    for item in items:
        inventory += f"Item: {item.name}, Quantity: {item.quantity}\n"

    # Code to send the report via email or any other method
