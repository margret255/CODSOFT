import tkinter as tk
from tkinter import messagebox
import json

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("600x500")

        # Contact fields
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(root, width=50)
        self.name_entry.pack(pady=5)

        self.phone_label = tk.Label(root, text="Phone No:")
        self.phone_label.pack(pady=10)
        self.phone_entry = tk.Entry(root, width=50)
        self.phone_entry.pack(pady=5)

        self.email_label = tk.Label(root, text="Email:")
        self.email_label.pack(pady=10)
        self.email_entry = tk.Entry(root, width=50)
        self.email_entry.pack(pady=5)

        self.address_label = tk.Label(root, text="Address:")
        self.address_label.pack(pady=10)
        self.address_entry = tk.Entry(root, width=50)
        self.address_entry.pack(pady=5)

        # Buttons
        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Contacts", command=self.view_contacts)
        self.view_button.pack(pady=5)

        self.search_button = tk.Button(root, text="Search Contact", command=self.search_contact)
        self.search_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Contact", command=self.update_contact)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(pady=5)

        self.contacts_listbox = tk.Listbox(root, width=70, height=10)
        self.contacts_listbox.pack(pady=20)

        self.load_contacts()

    def load_contacts(self):
        """Load contacts from the JSON file."""
        try:
            with open("contacts.json", "r") as file:
                # Try loading the contacts, if empty, initialize as an empty list
                self.contacts = json.load(file) if file.read().strip() else []
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle both missing and empty or malformed files
            self.contacts = []

    def save_contacts(self):
        """Save contacts to the JSON file."""
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file)

    def add_contact(self):
        """Add a new contact."""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if name and phone:
            new_contact = {"name": name, "phone": phone, "email": email, "address": address}
            self.contacts.append(new_contact)
            self.save_contacts()
            self.clear_entries()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showwarning("Input Error", "Name and Phone number are required!")

    def view_contacts(self):
        """Display all contacts."""
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def search_contact(self):
        """Search for a contact by name or phone number."""
        search_term = self.name_entry.get().strip()
        self.contacts_listbox.delete(0, tk.END)
        if search_term:
            for contact in self.contacts:
                if search_term.lower() in contact['name'].lower() or search_term in contact['phone']:
                    self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")
        else:
            messagebox.showwarning("Input Error", "Please enter a name or phone number to search!")

    def update_contact(self):
        """Update contact details."""
        try:
            selected_index = self.contacts_listbox.curselection()[0]
            selected_contact = self.contacts[selected_index]
            # Pre-fill the fields with the contact's current details
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_contact["name"])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, selected_contact["phone"])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, selected_contact["email"])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, selected_contact["address"])

            def apply_update():
                selected_contact["name"] = self.name_entry.get().strip()
                selected_contact["phone"] = self.phone_entry.get().strip()
                selected_contact["email"] = self.email_entry.get().strip()
                selected_contact["address"] = self.address_entry.get().strip()
                self.save_contacts()
                self.view_contacts()
                self.clear_entries()
                messagebox.showinfo("Success", "Contact updated successfully!")

            update_button = tk.Button(self.root, text="Apply Update", command=apply_update)
            update_button.pack(pady=5)

        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")

    def delete_contact(self):
        """Delete selected contact."""
        try:
            selected_index = self.contacts_listbox.curselection()[0]
            selected_contact = self.contacts[selected_index]
            result = messagebox.askyesno("Delete", f"Are you sure you want to delete the contact: {selected_contact['name']}?")
            if result:
                del self.contacts[selected_index]
                self.save_contacts()
                self.view_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully!")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def clear_entries(self):
        """Clear input fields."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()

if __name__ == "__main__":
    main()
