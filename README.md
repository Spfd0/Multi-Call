# Multi-Caller Application

This is a Python application that allows users to make multiple concurrent phone calls using the Twilio API. The application provides a graphical user interface (GUI) built with Tkinter for easy interaction.

## Features

- Add contacts manually or load them from a file
- Edit the message to be spoken during the call
- Make concurrent calls to selected contacts
- Clear the contact list
- User-friendly GUI

## Prerequisites

Before running the application, make sure you have the following:

- Python 3.7 or higher
- A Twilio account with valid credentials (Account SID, Auth Token, and Twilio phone number)
- https://www.twilio.com/en-us

## Installation

1. Clone this repository:
   git clone https://github.com/Spfd0/Multi-Call
   
   cd Multi-Call

3. Install the required dependencies:
   pip3 install twilio 

4. Set up your Twilio credentials:
   - Open the script and replace the placeholders for ACCOUNT_SID, AUTH_TOKEN, and TWILIO_NUMBER with your actual Twilio credentials.

## Usage

1. Run the application:
   python multi_call_v2.0.py

2. Use the GUI to:
   - Add contacts manually or load them from a file
   - Edit the message to be spoken during the call
   - Select contacts and initiate calls
   - Clear the contact list

## File Format for Loading Contacts

When loading contacts from a file, use the following format:

   Name1,+1XXXXXXXXXX
   Name2,+1XXXXXXXXXX
   Name3,+1XXXXXXXXXX

Each line should contain a name and a phone number separated by a comma. Phone numbers should be in the format +1XXXXXXXXXX.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for educational purposes only. Please ensure you comply with all applicable laws and regulations when using this application to make automated phone calls.
