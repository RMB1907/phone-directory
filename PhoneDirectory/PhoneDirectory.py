import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Contact:
    def __init__(self, name, phone, birthday, address):
        self.name = name
        self.phone = phone
        self.birthday = datetime.strptime(birthday, "%Y-%m-%d")  
        self.address = address
        self.prev = None
        self.next = None

def create_contact(name, phone, birthday, address):
    new_contact = Contact(name, phone, birthday, address)
    return new_contact

def add_contact(name_entry, phone_entry, birthday_entry, address_entry, head):
    name = name_entry.get()
    phone = phone_entry.get()
    birthday = birthday_entry.get()
    address = address_entry.get()

    if not name or not phone or not birthday or not address:
        messagebox.showerror("Error", "Please enter name, phone number, birthday, and address.")
        return

    new_contact = create_contact(name, phone, birthday, address)

    if head is None or name < head.name:
        new_contact.next = head
        if head is not None:
            head.prev = new_contact
        globals()['head'] = new_contact
    else:
        current = head
        while current.next is not None and name > current.next.name:
            current = current.next

        new_contact.next = current.next
        if current.next is not None:
            current.next.prev = new_contact
        current.next = new_contact
        new_contact.prev = current

    update_listbox(name_entry, phone_entry, birthday_entry, address_entry)  
    messagebox.showinfo("Success", "Contact added successfully.")
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    birthday_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def display_contacts(result_text, head):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Phone Directory (Sorted by Name):\n")
    
    current = head
    contacts = []
    
    while current is not None:
        contacts.append(current)
        current = current.next
    
    contacts.sort(key=lambda x: x.name.lower())
    
    count = 1
    today = datetime.now()

    for contact in contacts:
        result_text.insert(tk.END, f"\n{count}. Name: {contact.name}\nPhone: {contact.phone}\nAddress: {contact.address}")

        if today.month == contact.birthday.month and today.day == contact.birthday.day:
            result_text.insert(tk.END, "\n(BIRTHDAY TODAY!!)\n")
        else:
            result_text.insert(tk.END, f"\nBirthday: {contact.birthday.strftime('%Y-%m-%d')}\n")

        count += 1

def delete_contact(delete_entry, head):
    name_to_delete = delete_entry.get()

    current = head
    while current is not None and current.name != name_to_delete:
        current = current.next

    if current is None:
        messagebox.showerror("Error", f"No contact found with the name {name_to_delete}.")
    else:
        if current.prev is not None:
            current.prev.next = current.next
        else:
            globals()['head'] = current.next

        if current.next is not None:
            current.next.prev = current.prev

        update_listbox(delete_entry)  
        messagebox.showinfo("Success", f"Contact {name_to_delete} deleted successfully.")
        delete_entry.delete(0, tk.END)

def update_listbox(delete_entry=None, phone_entry=None, birthday_entry=None, address_entry=None):
    unique_names = set()  
    current = head
    while current is not None:
        unique_names.add(current.name)
        current = current.next

    names_listbox.delete(0, tk.END)
    for name in unique_names:
        names_listbox.insert(tk.END, name)

    if delete_entry:
        delete_entry.delete(0, tk.END)
    if phone_entry:
        phone_entry.delete(0, tk.END)
    if birthday_entry:
        birthday_entry.delete(0, tk.END)
    if address_entry:
        address_entry.delete(0, tk.END)

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    update_theme()

def update_theme():
    if dark_mode:
        bg_color = "#2C2C2C"
        fg_color = "black"
        font_color = "white"
    else:
        bg_color = "#f0f0f0"
        fg_color = "black"
        font_color = "#FF0000"

    root.configure(bg=bg_color)
    name_label.configure(bg=bg_color, fg=font_color)
    name_entry.configure(bg=fg_color, fg=font_color)
    phone_label.configure(bg=bg_color, fg=font_color)
    phone_entry.configure(bg=fg_color, fg=font_color)
    birthday_label.configure(bg=bg_color, fg=font_color)
    birthday_entry.configure(bg=fg_color, fg=font_color)
    address_label.configure(bg=bg_color, fg=font_color)
    address_entry.configure(bg=fg_color, fg=font_color)
    add_button.configure(bg="#4caf50", fg=font_color)
    display_button.configure(bg="#4caf50", fg=font_color)
    delete_label.configure(bg=bg_color, fg=font_color)
    delete_entry.configure(bg=fg_color, fg=font_color)
    delete_button.configure(bg="#ff6347", fg=font_color)
    
    names_listbox.configure(bg=fg_color, fg=font_color)
    result_text.configure(bg=bg_color, fg=font_color)

def close_splash():
    splash.destroy()
    open_main_window()

head = None
dark_mode = False

def open_main_window():
    global root, name_label, name_entry, phone_label, phone_entry, birthday_label, birthday_entry, address_label, address_entry
    global add_button, display_button, delete_label, delete_entry, delete_button, search_label, search_entry, search_button
    global names_listbox, result_text

    root = tk.Tk()
    root.title("Phone Directory")
    light_bg_color = "#f0f0f0"
    light_fg_color = "black"
    light_font_color = "#FF0000"

    root.configure(bg=light_bg_color)

    font_style = ("Helvetica", 18, "bold")

    name_label = tk.Label(root, text="Name:", bg=light_bg_color, fg=light_font_color, font=font_style)
    name_label.grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)

    name_entry = tk.Entry(root, font=font_style, bg=light_fg_color, fg=light_font_color)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    phone_label = tk.Label(root, text="Phone:", bg=light_bg_color, fg=light_font_color, font=font_style)
    phone_label.grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)

    phone_entry = tk.Entry(root, font=font_style, bg=light_fg_color, fg=light_font_color)
    phone_entry.grid(row=1, column=1, padx=10, pady=5)

    birthday_label = tk.Label(root, text="Birthday (YYYY-MM-DD):", bg=light_bg_color, fg=light_font_color, font=font_style)
    birthday_label.grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)

    birthday_entry = tk.Entry(root, font=font_style, bg=light_fg_color, fg=light_font_color)
    birthday_entry.grid(row=2, column=1, padx=10, pady=5)

    address_label = tk.Label(root, text="Address:", bg=light_bg_color, fg=light_font_color, font=font_style)
    address_label.grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)

    address_entry = tk.Entry(root, font=font_style, bg=light_fg_color, fg=light_font_color)
    address_entry.grid(row=3, column=1, padx=10, pady=5)

    add_button = tk.Button(root, text="Add Contact", command=lambda: add_contact(name_entry, phone_entry, birthday_entry, address_entry, head), bg="#4caf50", fg=light_font_color, font=font_style)
    add_button.grid(row=4, column=1, padx=10, pady=5)

    display_button = tk.Button(root, text="Display Contacts", command=lambda: display_contacts(result_text, head), bg="#4caf50", fg=light_font_color, font=font_style)
    display_button.grid(row=5, column=1, padx=10, pady=5)

    delete_label = tk.Label(root, text="Delete Contact:", bg=light_bg_color, fg=light_font_color, font=font_style)
    delete_label.grid(row=6, column=0, sticky=tk.E, padx=10, pady=5)

    delete_entry = tk.Entry(root, font=font_style, bg=light_fg_color, fg=light_font_color)
    delete_entry.grid(row=6, column=1, padx=10, pady=5)

    delete_button = tk.Button(root, text="Delete", command=lambda: delete_contact(delete_entry, head), bg="#ff6347", fg=light_font_color, font=font_style)
    delete_button.grid(row=6, column=2, padx=10, pady=5)

    
   
    names_listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=font_style, bg=light_fg_color, fg=light_font_color)
    names_listbox.bind("<<ListboxSelect>>", lambda event: delete_entry.delete(0, tk.END) or delete_entry.insert(tk.END, names_listbox.get(names_listbox.curselection())))
    names_listbox.grid(row=8, column=0, padx=10, pady=5)

    result_text = tk.Text(root, height=10, width=40, bg=light_bg_color, fg=light_font_color, font=font_style)
    result_text.grid(row=8, column=1, padx=10, pady=5)

    toggle_button_text = "Switch to Dark Mode" if not dark_mode else "Switch to Light Mode"
    toggle_button = tk.Button(root, text=toggle_button_text, command=toggle_dark_mode, bg="#607d8b", fg=light_font_color, font=font_style)
    toggle_button.grid(row=9, column=1, padx=10, pady=5)

    for i in range(2):  
        root.columnconfigure(i, weight=1)
    for i in range(10): 
        root.rowconfigure(i, weight=1)
    root.mainloop()

splash = tk.Tk()
splash.title("Phone Directory - Welcome")
splash.geometry("800x600")

bg_photo = tk.PhotoImage(file=r"C:\Users\Renee\Desktop\ph11.png")
bg_label = tk.Label(splash, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

splash_title_label = tk.Label(splash, text="Phone Directory", font=("Helvetica", 30), bg="white")
splash_title_label.pack(pady=20)

start_button = tk.Button(splash, text="Start", command=close_splash, bg="maroon", fg="white", font=("Helvetica", 16))
start_button.pack(side='bottom', pady=(0, 50), padx=20)

splash.mainloop()