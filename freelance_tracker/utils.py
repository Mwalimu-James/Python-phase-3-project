from datetime import datetime
from database import session
from models import User, Project, Invoice

def validate_date(date_str):
    """Validate and parse date input (YYYY-MM-DD)"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("❌ Invalid date format! Use YYYY-MM-DD.")

def validate_user(user_id):
    """Ensure the user exists in the database"""
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError(f"❌ User with ID {user_id} not found!")
    return user

def validate_project(project_id):
    """Ensure the project exists"""
    project = session.query(Project).filter_by(id=project_id).first()
    if not project:
        raise ValueError(f"❌ Project with ID {project_id} not found!")
    return project

def validate_invoice(invoice_id):
    """Ensure the invoice exists"""
    invoice = session.query(Invoice).filter_by(id=invoice_id).first()
    if not invoice:
        raise ValueError(f"❌ Invoice with ID {invoice_id} not found!")
    return invoice
