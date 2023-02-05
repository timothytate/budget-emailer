# Import Expenses Excel file
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

monthly_expenses = pd.read_excel('/Users/timothytate/Library/CloudStorage/OneDrive-Personal/Documents/Monthly Expenses.xlsx', sheet_name="Monthly Expenses")
monthly_expenses = monthly_expenses.reset_index(drop=True)

# Find the expected expenses from today to my next payday
today = datetime.date.today()
startingpayday = datetime.date(2023, 1, 12)

listofpaydays = []
while startingpayday < today:
    startingpayday += datetime.timedelta(days=14)
    listofpaydays.append(startingpayday)

nextpayday = listofpaydays[-1]
lastpayday = listofpaydays[-2]

# Transform the Day column to a datetime.date object in monthly_expenses starting at the lastpayday rolling into next month to include the year and month
# If the day is greater than or equal to the lastpayday.day, then the year and month will be the same as lastpayday, otherwise it will be the next month
monthly_expenses['Day'] = monthly_expenses['Day'].apply(lambda x: datetime.date(lastpayday.year, lastpayday.month, x) if x >= lastpayday.day else datetime.date(nextpayday.year, nextpayday.month, x))

# Make a list of the expenses that will occur between today and my next payday
expected_expenses = monthly_expenses.loc[monthly_expenses['Day'].between(today, nextpayday, inclusive=False)]

# Make a list of the expenses that will occur between the last payday and today
lastpayday_expenses = monthly_expenses.loc[monthly_expenses['Day'].between(lastpayday, today, inclusive=False)]

# Sort the expenses by the Day column by month, day, and year
expected_expenses = expected_expenses.sort_values(by=['Day'], ascending=True)
lastpayday_expenses = lastpayday_expenses.sort_values(by=['Day'], ascending=True)

# Find the total expected expenses and add it to the end of the expected expenses output
total_expected_expenses = expected_expenses['Amount'].sum()
expected_expenses.loc[len(expected_expenses)] = ['Total', "", "", total_expected_expenses]

# Send the expected expenses to my email
fromaddr = "your_app@gmail.com"
toaddr = "person1@gmail.com; person2@gmail.com"    
msg = MIMEMultipart()
msg['From'] = fromaddr  # From  email address
msg['To'] = toaddr  # To email address
msg['Subject'] = "Expected Expenses (before we get paid)"

# Add some text to the email body, the expected expenses, and lastpayday expenses
body = "Expenses from last payday to today. These should have cleared the bank:"
body += lastpayday_expenses.to_html()
body += "<br>" # Add a line break
body += "Remaining Expenses (before we get paid):"
body += expected_expenses.to_html()
body += "<br>" # Add a line break
body += "To update any of these expenses, please go to the Monthly Expenses Excel file in the OneDrive folder."
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("your username", "your password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
