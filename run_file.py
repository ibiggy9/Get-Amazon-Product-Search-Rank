# Importing required modules
import schedule
import os

def run():
    """
    Execute the target Python script and print a message to indicate execution.
    """
    # Run the Python script using os.system
    os.system("python3.9 inputs.py")
    
    # Print message to console to indicate that the script is running
    print('running')

# Schedule the 'run' function to execute every 24 hours
schedule.every(24).hours.do(run)

# Keep the script running and check for pending scheduled tasks
while True:
    schedule.run_pending()
