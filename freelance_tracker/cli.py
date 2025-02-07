import click
from database import session
from models import User, Project, Invoice, Payment
from datetime import datetime
from tabulate import tabulate
from sqlalchemy.sql import extract
from sqlalchemy import func



# Utility functions for validation and formatting
def validate_date(date_str):
    """Validate and parse date input (YYYY-MM-DD)"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(click.style("❌ Invalid date format! Use YYYY-MM-DD.", fg="red"))

def validate_user(user_id):
    """Ensure the user exists in the database"""
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError(click.style(f"❌ User with ID {user_id} not found!", fg="red"))
    return user

def validate_project(project_id):
    """Ensure the project exists"""
    project = session.query(Project).filter_by(id=project_id).first()
    if not project:
        raise ValueError(click.style(f"❌ Project with ID {project_id} not found!", fg="red"))
    return project

def validate_invoice(invoice_id):
    """Ensure the invoice exists"""
    invoice = session.query(Invoice).filter_by(id=invoice_id).first()
    if not invoice:
        raise ValueError(click.style(f"❌ Invoice with ID {invoice_id} not found!", fg="red"))
    return invoice

def format_table(data, headers):
    """Formats and displays tabular data using tabulate"""
    if not data:
        return click.style("✅ No records found!", fg="green")
    return tabulate(data, headers=headers, tablefmt="fancy_grid")

@click.group()
def cli():
    """Freelance Project & Earnings Tracker CLI"""
    pass

# 1️ Add a New Project
@click.command()
@click.option("--user_id", prompt="Enter User ID", type=int)
@click.option("--name", prompt="Project Name")
@click.option("--description", prompt="Project Description")
@click.option("--deadline", prompt="Deadline (YYYY-MM-DD)")
@click.option("--status", default="In Progress", help="Project Status (default: In Progress)")
def add_project(user_id, name, description, deadline, status):
    """Add a new freelance project"""
    try:
        validate_user(user_id)
        deadline_date = validate_date(deadline)

        project = Project(
            user_id=user_id,
            name=name,
            description=description,
            deadline=deadline_date,
            status=status
        )
        session.add(project)
        session.commit()
        click.echo(click.style(f"✅ Project '{name}' added successfully!", fg="green"))

    except ValueError as e:
        click.echo(str(e))

# 2️ Update a Project
@click.command()
@click.option("--project_id", prompt="Enter Project ID", type=int)
@click.option("--name", default=None, help="New Project Name")
@click.option("--description", default=None, help="New Project Description")
@click.option("--deadline", default=None, help="New Deadline (YYYY-MM-DD)")
@click.option("--status", default=None, help="New Status")
def update_project(project_id, name, description, deadline, status):
    """Update project details"""
    try:
        project = validate_project(project_id)

        if name:
            project.name = name
        if description:
            project.description = description
        if deadline:
            project.deadline = validate_date(deadline)
        if status:
            project.status = status

        session.commit()
        click.echo(click.style(f"✅ Project ID {project_id} updated successfully!", fg="yellow"))

    except ValueError as e:
        click.echo(str(e))

# 3️ Delete a Project
@click.command()
@click.option("--project_id", prompt="Enter Project ID", type=int)
def delete_project(project_id):
    """Delete a project"""
    try:
        project = validate_project(project_id)
        session.delete(project)
        session.commit()
        click.echo(click.style(f"✅ Project ID {project_id} deleted successfully!", fg="red"))

    except ValueError as e:
        click.echo(str(e))

# 4️ Add a New Invoice
@click.command()
@click.option("--project_id", prompt="Enter Project ID", type=int)
@click.option("--amount_due", prompt="Amount Due", type=float)
@click.option("--due_date", prompt="Due Date (YYYY-MM-DD)")
def add_invoice(project_id, amount_due, due_date):
    """Add an invoice for a project"""
    try:
        validate_project(project_id)
        due_date_parsed = validate_date(due_date)

        invoice = Invoice(
            project_id=project_id,
            amount_due=amount_due,
            amount_paid=0.0,
            due_date=due_date_parsed,
            status="Pending"
        )
        session.add(invoice)
        session.commit()
        click.echo(click.style(f"✅ Invoice of ${amount_due} added for Project ID {project_id}.", fg="green"))

    except ValueError as e:
        click.echo(str(e))

# 5️ Update an Invoice
@click.command()
@click.option("--invoice_id", prompt="Enter Invoice ID", type=int)
@click.option("--amount_due", default=None, type=float, help="New Amount Due")
@click.option("--due_date", default=None, help="New Due Date (YYYY-MM-DD)")
@click.option("--status", default=None, help="New Status")
def update_invoice(invoice_id, amount_due, due_date, status):
    """Update invoice details"""
    try:
        invoice = validate_invoice(invoice_id)

        if amount_due:
            invoice.amount_due = amount_due
        if due_date:
            invoice.due_date = validate_date(due_date)
        if status:
            invoice.status = status

        session.commit()
        click.echo(click.style(f"✅ Invoice ID {invoice_id} updated successfully!", fg="yellow"))

    except ValueError as e:
        click.echo(str(e))

# 6️ Delete an Invoice
@click.command()
@click.option("--invoice_id", prompt="Enter Invoice ID", type=int)
def delete_invoice(invoice_id):
    """Delete an invoice"""
    try:
        invoice = validate_invoice(invoice_id)
        session.delete(invoice)
        session.commit()
        click.echo(click.style(f"✅ Invoice ID {invoice_id} deleted successfully!", fg="red"))

    except ValueError as e:
        click.echo(str(e))

# 7️ Record a Payment
@click.command()
@click.option("--invoice_id", prompt="Enter Invoice ID", type=int)
@click.option("--amount", prompt="Payment Amount", type=float)
@click.option("--payment_method", prompt="Payment Method (Bank, PayPal, etc.)")
@click.option("--date_received", prompt="Payment Date (YYYY-MM-DD)")
def record_payment(invoice_id, amount, payment_method, date_received):
    """Record a payment for an invoice"""
    try:
        invoice = validate_invoice(invoice_id)
        date_received_parsed = validate_date(date_received)

        payment = Payment(
            invoice_id=invoice_id,
            amount=amount,
            payment_method=payment_method,
            date_received=date_received_parsed
        )

        # Update invoice status
        invoice.amount_paid += amount
        if invoice.amount_paid >= invoice.amount_due:
            invoice.status = "Paid"

        session.add(payment)
        session.commit()
        click.echo(click.style(f"✅ Payment of ${amount} recorded for Invoice ID {invoice_id}.", fg="blue"))

    except ValueError as e:
        click.echo(str(e))

@click.command()
@click.option("--user_id", prompt="Enter User ID", type=int)
def view_invoices(user_id):
    """View all outstanding invoices for a freelancer"""
    try:
        validate_user(user_id)
        invoices = session.query(Invoice).join(Project).filter(
            Project.user_id == user_id, Invoice.status == "Pending"
        ).all()

        if not invoices:
            click.echo(click.style("✅ No outstanding invoices!", fg="green"))
        else:
            data = [[inv.id, inv.amount_due, inv.due_date, inv.status] for inv in invoices]
            headers = ["Invoice ID", "Amount Due ($)", "Due Date", "Status"]
            click.echo(click.style("\n Outstanding Invoices:", fg="cyan", bold=True))
            click.echo(format_table(data, headers))

    except ValueError as e:
        click.echo(str(e))

@click.command()
@click.option("--user_id", prompt="Enter User ID", type=int)
@click.option("--month", prompt="Enter Month (1-12)", type=int)
@click.option("--year", prompt="Enter Year", type=int)
def generate_report(user_id, month, year):
    """Generate a financial report for a freelancer"""
    try:
        validate_user(user_id)

        # ✅ Use extract() to filter by month and year
        payments = session.query(Payment).join(Invoice).join(Project).filter(
            Project.user_id == user_id,
            func.strftime("%m", Payment.date_received) == str(month).zfill(2),
            func.strftime("%y", Payment.date_received) == str(year)
        ).all()
        total_earnings = sum(payment.amount for payment in payments)

        click.echo(click.style(f"\n Earnings Report for {month}/{year}", fg="yellow", bold=True))
        click.echo(click.style(f" Total Earnings: ${total_earnings:.2f}", fg="green", bold=True))

    except ValueError as e:
        click.echo(str(e))

cli.add_command(generate_report)
# Register CLI commands
cli.add_command(add_project)
cli.add_command(update_project)
cli.add_command(delete_project)
cli.add_command(add_invoice)
cli.add_command(update_invoice)
cli.add_command(delete_invoice)
cli.add_command(record_payment)
cli.add_command(view_invoices)
cli.add_command(generate_report)

if __name__ == "__main__":
    cli()
