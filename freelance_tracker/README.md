########Freelance Project & Earnings Tracker CLI########

#############Overview#######################

The Freelance Project & Earnings Tracker CLI is a powerful command-line application designed to help freelancers manage their projects, track invoices, and analyze earnings. This tool ensures that freelancers stay organized, never miss a deadline, and get paid on time.



####################Key Features (MVPs)##################

1. Project & Invoice Tracker - Log new projects, set deadlines, and track invoices (amount due, payment status, due date).

2. Automatic Late Payment Reminders - Identifies overdue invoices and sends reminders.

3. Earnings & Performance Reports - Generates financial reports to analyze income trends and outstanding payments.

4. Freelancer Rate Calculator - Suggests an optimal hourly/fixed rate based on past projects, workload, and earnings.

#######################User Stories###########################

1 .As a freelancer, I should be able to log my projects and deadlines so that I can keep track of ongoing and completed work.

2. As a freelancer, I should receive alerts for unpaid invoices so that I can follow up with clients and get paid on time.

3. As a freelancer, I should be able to generate financial reports so that I can analyze my income and make informed business decisions.

4. As a freelancer, I should be able to calculate my ideal hourly rate based on my workload and past earnings so that I can set competitive prices.

5. As a freelancer, I should be able to filter my earnings by client so that I can identify my most profitable clients and focus on them.


#################Installation & Setup##############################

####Prerequisites

Ensure you have the following installed:

Python 3.8+

Pipenv (for virtual environment and dependency management)

###Setup Instructions###

1. Clone this repository:
git clone https://github.com/Mwalimu-James/Python-phase-3-project.git
cd freelance-tracker-cli

2. Install dependencies:
pip install pipenv
pipenv install

3. Activate the virtual environment:
pipenv shell

4. Initialize the database:
python database.py

5. Run the application:
python app.py


######Usage Guide#####
1.Log a new project:
python app.py add_project --name "Website Redesign" --deadline "2024-03-15" --status "In Progress"

2. Add an invoice:
python app.py add_invoice --project_id 1 --amount_due 500 --due_date "2024-04-01"

3. Check outstanding invoices:
python app.py view_invoices --status "Pending"

4. Generate earnings report:
python app.py generate_report --month 3 --year 2024


 #######Database Schema (ERD)#########
 User (id, name, email, password)
│
├── Project (id, user_id, name, description, deadline, status)
│
├── Invoice (id, project_id, amount_due, amount_paid, due_date, status)
│
└── Payment (id, invoice_id, amount, payment_method, date_received)


#######Technologies Used###########

Python 3.8+ (Primary programming language)

SQLAlchemy (ORM for database management)

SQLite (Lightweight database for persistence)

Pipenv (Dependency and virtual environment management)

Click or Argparse (For CLI commands)


########Future Improvements##########

>> Integration with PayPal/Stripe for invoice payments.

>> Email notifications for overdue invoices.

>> Export financial reports to CSV/PDF.

>> Multi-user support for teams and agencies.

####Author & Contact########

JAMES KUNGU
Email: cegeavin@gmail.com 
GitHub: (https://github.com/Mwalimu-James)
