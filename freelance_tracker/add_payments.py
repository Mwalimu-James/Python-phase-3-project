from database import session
from models import Invoice, Payment
from datetime import datetime

# Fetch all pending invoices
invoices = session.query(Invoice).filter_by(status="Pending").all()

for invoice in invoices:
    payment = Payment(
        invoice_id=invoice.id,
        amount=invoice.amount_due,  # Pay full invoice amount
        payment_method="Bank Transfer",
        date_received=datetime(2024, 4, 10)  # Set a payment date
    )
    
    # Mark invoice as Paid
    invoice.amount_paid = invoice.amount_due
    invoice.status = "Paid"

    session.add(payment)

session.commit()
print("✅ All invoices have been paid successfully!")
