from database import session
from models import User, Project, Invoice
from datetime import datetime

# List of users with projects and invoices
users_data = [
    {"name": "James Kungu", "email": "james.kungu@example.com", "password": "pass123", "project": "E-commerce Website", "description": "Developing an online store", "amount_due": 1500},
    {"name": "Caleb Kiprotich", "email": "caleb.kip@example.com", "password": "pass123", "project": "Mobile App UI/UX", "description": "Designing a fintech app UI", "amount_due": 1200},
    {"name": "Trevor Omondi", "email": "trevor.omondi@example.com", "password": "pass123", "project": "Data Analysis Report", "description": "Analyzing sales data", "amount_due": 900},
    {"name": "Jessica Mwangi", "email": "jessica.mwangi@example.com", "password": "pass123", "project": "Marketing Campaign", "description": "Running social media ads", "amount_due": 1800},
    {"name": "Damaris Kerubo", "email": "damaris.kerubo@example.com", "password": "pass123", "project": "SEO Optimization", "description": "Improving website ranking", "amount_due": 1100},
    {"name": "Abdi Hersi", "email": "abdi.hersi@example.com", "password": "pass123", "project": "Cybersecurity Audit", "description": "Assessing security vulnerabilities", "amount_due": 2500},
    {"name": "David Odhiabo", "email": "david.odhiabo@example.com", "password": "pass123", "project": "Custom CRM System", "description": "Building a CRM for client management", "amount_due": 3000},
    {"name": "Branon Simiyu", "email": "branon.simiyu@example.com", "password": "pass123", "project": "Machine Learning Model", "description": "Developing a predictive model", "amount_due": 2700},
    {"name": "Eric Wainaina", "email": "eric.wainaina@example.com", "password": "pass123", "project": "Cloud Migration", "description": "Moving services to AWS cloud", "amount_due": 2200},
    {"name": "Samuel Kagotho", "email": "samuel.kagotho@example.com", "password": "pass123", "project": "Graphic Design Package", "description": "Creating brand identity assets", "amount_due": 1400}
]

# Set deadlines and due dates
deadline_date = datetime(2024, 3, 31)  # Project deadline
due_date = datetime(2024, 4, 15)  # Invoice due date

# Insert data into database
for user_data in users_data:
    # Check if user already exists
    user = session.query(User).filter_by(email=user_data["email"]).first()
    if not user:
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        session.add(user)
        session.commit()
    
    # Add Project
    project = Project(
        user_id=user.id,
        name=user_data["project"],
        description=user_data["description"],
        deadline=deadline_date,
        status="In Progress"
    )
    session.add(project)
    session.commit()

    # Add Invoice
    invoice = Invoice(
        project_id=project.id,
        user_id=user.id,
        amount_due=user_data["amount_due"],
        amount_paid=0.0,
        due_date=due_date,
        status="Pending"
    )
    session.add(invoice)
    session.commit()

    print(f"✅ Added User: {user.name}, Project: {project.name}, Invoice: ${invoice.amount_due}")

print("✅ All users, projects, and invoices added successfully!")
