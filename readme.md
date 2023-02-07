# Budget Tracker
Like most people, I live on the edge hoping I won't overdraft my bank account paycheck to paycheck. Here's a humble python script that will read the day of the week you are expecting your expenses to come out of your account, create a list of thoses expeses up until your next paycheck, and email you the list/total.

### Step 1: Create a gmail account
Create a gmail account that will be used to send the email. I recommend using a throwaway account for this. But you do you.

### Step 2: Create a google app password
Go to [Google App Passwords](https://myaccount.google.com/apppasswords) and create a new app password for the gmail account you just created. Make sure to select mail as the app and select other as the device. Copy the password you just created.

### Step 3: Replace the variables in the script with your own
Replace the variables in the script with your own. The variables are:
- `fromaddr` - The email address you just created
- `server.login()` - The username and password you created
- `toaddr` - The email address you want to send the email to

### Step 4: Update the excel expenses file
Update the excel expenses file with your expenses. The script will read the excel file and create a list of expenses for the week. The excel file should have the following columns:
- `Day` - The day of the week you expect the expense to come out of your account each month
- `Expense` - The name of the expense
- `Category` - The category of the expense (i.e. food, gas, etc.)
- `Amount` - The amount of the expense

### Step 5: Run the script
Run the script and it will create a list of expenses that should have cleared your account, and a list that are still to come before your next paycheck. 

Change directory to the directory where the script is located.

    cd /path/to/directory

Run the makefile with the following command:

    make

Run the script on Linux with the following command:

    python3 budgetemailer.py

Run the script on Windows with the following command:

    python budgetemailer.py

## Step 6: Schedule the script to run daily
Schedule the script to run daily. I use cron on Linux to schedule the script to run daily at 8:00am. 

    0 8 * * * cd /path/to/directory && python3 budgetemailer.py

Schedule the script to run daily on Windows. I use Task Scheduler to schedule the script to run daily at 8:00am.

    schtasks /create /tn "Budget Tracker" /tr "C:\path\to\directory\python.exe C:\path\to\directory\budgetemailer.py" /sc daily /st 08:00:00

**Important Note** - the script and the excel file must be in the same directory.
