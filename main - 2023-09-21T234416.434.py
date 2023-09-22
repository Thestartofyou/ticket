import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Define the URL of the flight search results page
url = "https://www.example.com/flights?origin=JFK&destination=LAX&departure_date=2023-10-01"

# Set your target price
target_price = 300  # Change this to your desired target price

# Set your email credentials (for sending notifications)
smtp_server = 'smtp.example.com'  # Update with your SMTP server
smtp_port = 587  # Update with your SMTP port
email_address = 'your_email@example.com'
email_password = 'your_email_password'
recipient_email = 'recipient_email@example.com'

# Function to send an email notification
def send_notification(subject, message):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(email_address, recipient_email, email_message)
        print("Notification email sent successfully.")
    except Exception as e:
        print(f"Error sending notification email: {str(e)}")
    finally:
        server.quit()

# Function to track ticket prices
def track_prices():
    while True:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the price element from the page (modify according to the website structure)
            price_element = soup.find('span', class_='ticket-price')

            if price_element:
                current_price = float(price_element.text.replace('$', '').replace(',', ''))
                print(f"Current price: ${current_price:.2f}")

                if current_price <= target_price:
                    send_notification("Flight Price Alert", f"The ticket price is now ${current_price:.2f}! Book now.")
                    break  # You can stop tracking once the target price is reached
            else:
                print("Price element not found on the page.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Check the price every hour (you can adjust the interval)
        time.sleep(3600)

if __name__ == "__main__":
    track_prices()

