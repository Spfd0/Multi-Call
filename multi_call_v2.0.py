import os
import asyncio
import aiohttp
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Twilio credentials
ACCOUNT_SID = 'TWILIO_ACCOUNT_SID'
AUTH_TOKEN = 'TWILIO_AUTH_TOKEN'
TWILIO_NUMBER = 'TWILIO_PHONE_NUMBER'

# Initialize Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

async def make_call(session, contact, twiml):
    name, number = contact
    try:
        call = await asyncio.to_thread(
            client.calls.create,
            to=number,
            from_=TWILIO_NUMBER,
            twiml=twiml
        )
        return f"Call to {name} ({number}) initiated. Call SID: {call.sid}"
    except TwilioRestException as e:
        return f"Error calling {name} ({number}): {str(e)}"

async def make_concurrent_calls(contacts, twiml):
    async with aiohttp.ClientSession() as session:
        tasks = [make_call(session, contact, twiml) for contact in contacts]
        results = await asyncio.gather(*tasks)
    return results

class MultiCallerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multi-Caller Application")
        self.geometry("320x500")

        self.contacts = []
        self.twiml = '<Response><Say>This is an automated call. Please disregard.</Say></Response>'

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Multi-Caller Application", font=("Helvetica", 16)).pack(pady=10)

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        ttk.Label(self.input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = ttk.Entry(self.input_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self, text="Add Contact", command=self.add_contact).pack(pady=5)
        ttk.Button(self, text="Load from File", command=self.load_from_file).pack(pady=5)

        self.contacts_listbox = tk.Listbox(self, width=50, height=10, selectmode=tk.EXTENDED)
        self.contacts_listbox.pack(pady=10)

        ttk.Button(self, text="Edit Message", command=self.edit_message).pack(pady=5)
        ttk.Button(self, text="Make Calls", command=self.make_calls).pack(pady=5)
        ttk.Button(self, text="Clear Contacts", command=self.clear_contacts).pack(pady=5)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if name and phone.startswith('+') and len(phone) == 12 and phone[1:].isdigit():
            self.contacts.append((name, phone))
            self.contacts_listbox.insert(tk.END, f"{name}: {phone}")
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Please use the format: Name, +1XXXXXXXXXX")

    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 2 and parts[1].startswith('+') and len(parts[1]) == 12 and parts[1][1:].isdigit():
                        self.contacts.append((parts[0], parts[1]))
                        self.contacts_listbox.insert(tk.END, f"{parts[0]}: {parts[1]}")

    def edit_message(self):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Message")
        edit_window.geometry("450x220")

        ttk.Label(edit_window, text="Edit the message:").pack(pady=5)
        message_entry = tk.Text(edit_window, height=8, width=44)
        message_entry.pack(pady=5)
        message_entry.insert(tk.END, self.twiml[15:-17])  # Extract the message from TwiML

        def save_message():
            new_message = message_entry.get("1.0", tk.END).strip()
            self.twiml = f'<Response><Say>{new_message}</Say></Response>'
            edit_window.destroy()
            messagebox.showinfo("Message Updated", "The call message has been updated.")

        ttk.Button(edit_window, text="Save", command=save_message).pack(pady=5)

    def make_calls(self):
        selected_indices = self.contacts_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("No Contacts Selected", "Please select contacts before making calls.")
            return

        selected_contacts = [self.contacts[i] for i in selected_indices]
        if messagebox.askyesno("Confirmation", f"Do you want to proceed with calls to {len(selected_contacts)} selected contacts?"):
            results = asyncio.run(make_concurrent_calls(selected_contacts, self.twiml))
            messagebox.showinfo("Call Results", "\n".join(results))

    def clear_contacts(self):
        self.contacts = []
        self.contacts_listbox.delete(0, tk.END)

if __name__ == "__main__":
    app = MultiCallerApp()
    app.mainloop()
