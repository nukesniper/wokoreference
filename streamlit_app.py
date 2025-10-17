import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to get the current listings from the website
def get_listings():
    url = "https://woko.ch/en/zimmer-in-zuerich"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all("div", class_="property-listing")  # Assuming listings are contained in this div, update as necessary
    
    listings_text = ""
    for listing in listings:
        title = listing.find("h2").text if listing.find("h2") else ""
        price = listing.find("span", class_="price").text if listing.find("span", class_="price") else ""
        listings_text += f"{title} - {price}\n"
    
    return listings_text.strip()

# Function to send an email notification
def send_email(subject, body):
    sender_email = "your_email@gmail.com"
    receiver_email = "your_email@gmail.com"
    password = "your_email_password"  # Ensure your email has "less secure apps" enabled or use OAuth2
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Main Streamlit app
def main():
    st.title("Woko Listing Monitor")
    
    # Store the initial listings
    previous_listings = get_listings()
    
    if previous_listings:
        st.write("Initial listings fetched.")
    
    while True:
        st.write("Checking for new listings...")
        
        # Wait for 2 minutes before checking again
        time.sleep(120)
        
        # Get the new listings
        new_listings = get_listings()
        
        if new_listings and new_listings != previous_listings:
            # Send an email if listings have changed
            st.write("New listing detected!")
            send_email("New Listing on Woko.ch", "A new listing has appeared on Woko.ch.")
            
            # Update previous listings to the new listings
            previous_listings = new_listings
        else:
            st.write("No new listings.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
