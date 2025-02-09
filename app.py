import datetime
from tkinter import *
from tkinter import ttk, messagebox
from pathlib import Path
import jsonpickle
import pygame


collection = {
    "Computer": [],
    "Camera": [],
    "Phone": [],
    "Video Player": []
}

class RetroCollectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Collection")
        self.root.geometry("450x450")
        self.root.iconbitmap("assets/win98.ico")

        # Load data when starting the application
        self.load_data()

        # Creation of main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(N, W, E, S))


        # Adding a title label

        self.title_label = ttk.Label(self.main_frame, text="Retro Relic Collection", font=('MS Sans Serif', 18, 'bold', 'underline'))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Creation of buttons
        ttk.Button(self.main_frame, text="Add Item", cursor="hand2", command=self.show_add_window).grid(row=2, column=0, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Show Items", cursor="hand2", command=self.show_items_window).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Edit Item", cursor="hand2", command=self.show_edit_window).grid(row=2, column=2, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Delete Item", cursor="hand2", command=self.show_delete_window).grid(row=2, column=3, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Retro Sound♫", cursor="hand2", command=self.play_sound).grid(row=3, column=3, pady=5, padx=10)
        ttk.Button(self.main_frame, text="Add Type", cursor="hand2", command=self.show_type_window).grid(row=3, column=0, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Delete Type", cursor="hand2", command=self.show_delete_type_window).grid(row=3, column=1, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Show Time", cursor="hand2", command=self.show_time).grid(row=3, column=2, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Sort Item Types A-Z", cursor="hand2", command=self.sort_items_a_z).grid(row=4, column=0, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Sort Item Types Z-A", cursor="hand2", command=self.sort_items_z_a).grid(row=4, column=3, pady=5, padx=5)



        # Create display area
        self.display_area = Text(self.main_frame, height=15, width=50)
        self.display_area.grid(row=1, column=0, columnspan=4, pady=10)

        # Creation of the Scrollbar
        v_scrollbar = Scrollbar(self.main_frame, orient='vertical')
        v_scrollbar.grid(row=1, column=4, sticky='ns')
        self.display_area.config(yscrollcommand=v_scrollbar.set)

    @staticmethod
    def save_data(): # Saving the file using jsonpickle
        try:
            with open('collection_data.json', 'w', encoding='utf-8') as f:
                json_data = jsonpickle.encode(collection, indent=4)  # Serialize data
                f.write(json_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    @staticmethod
    def load_data(): # Loading the file using jsonpickle
        global collection
        try:
            if Path('collection_data.json').exists():
                with open('collection_data.json', 'r', encoding='utf-8') as f:
                    collection = jsonpickle.decode(f.read())  # Deserialize data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            collection = {
                "Computer": [],
                "Camera": [],
                "Phone": [],
                "Video Player": []
            }
    def show_type_window(self):
        type_window = Toplevel(self.root)
        type_window.title("Add Type")
        type_window.geometry("300x150")
        type_window.iconbitmap("assets/win98.ico")

        ttk.Label(type_window, text="Add New Type:").grid(row=0, column=0, pady=10, padx=10)

        type_entry = ttk.Entry(type_window)
        type_entry.grid(row=0, column=1, pady=10, padx=10)

        def add_type():
            new_type = type_entry.get().strip()

            if not new_type:  # Check if it is empty
                messagebox.showerror("Error", "Type name cannot be empty!")
                return

            if new_type in collection:  # Check if it already exists
                messagebox.showerror("Error", "This type already exists!")
                return

            collection[new_type] = []  # Add new type as an empty list
            self.save_data()  # Save updated collection
            messagebox.showinfo("Success", f"'{new_type}' added successfully!")
            type_window.destroy()
            self.show_items_window()
        ttk.Button(type_window, text="Add Type", command=add_type).grid(row=1, column=0, columnspan=2, pady=20)

    def show_delete_type_window(self):
        type_window = Toplevel(self.root)
        type_window.title("Delete Type")
        type_window.geometry("300x150")
        type_window.iconbitmap("assets/win98.ico")
        ttk.Label(type_window, text="Delete Type:").grid(row=0, column=0, pady=10, padx=10)
        type_var = StringVar()
        type_combo = ttk.Combobox(type_window, textvariable=type_var, values=list(collection.keys()))
        type_combo.grid(row=0, column=1, pady=5, padx=5)

        def delete_type():
            selected_type = type_var.get()
            if not selected_type:
                messagebox.showerror("Error", "Please select a type to delete.")
                return

            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_type}'? This will also delete all items within this type."):
                collection.pop(selected_type)
                self.save_data()
                messagebox.showinfo("Success", f"'{selected_type}' and its items have been deleted.")
                type_window.destroy()
                self.show_items_window()
        ttk.Button(type_window, text="Delete Type", command=delete_type).grid(row=1, column=0, columnspan=2, pady=20)


    def show_add_window(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Item")
        add_window.geometry("500x400")
        add_window.iconbitmap("assets/win98.ico")
        
        # Create form fields
        ttk.Label(add_window, text="Title:").grid(row=0, column=0, pady=5, padx=5)
        title_entry = ttk.Entry(add_window)
        title_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="Type:").grid(row=1, column=0, pady=5, padx=5)
        type_var = StringVar()
        type_combo = ttk.Combobox(add_window, textvariable=type_var, values=list(collection.keys()))
        type_combo.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="Date Added (dd/mm/yyyy):").grid(row=2, column=0, pady=5, padx=5)
        date_added_entry = ttk.Entry(add_window)
        date_added_entry.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="Date of Manufacture (dd/mm/yyyy):").grid(row=3, column=0, pady=5, padx=5)
        date_manufacture_entry = ttk.Entry(add_window)
        date_manufacture_entry.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="Description:").grid(row=4, column=0, pady=5, padx=5)
        description_text = Text(add_window, height=3, width=30)
        description_text.grid(row=4, column=1, pady=5, padx=5)

        
        def add_item_to_collection():
            try:
                title = title_entry.get()
                item_type = type_var.get()
                date_added = datetime.datetime.strptime(date_added_entry.get(), "%d/%m/%Y").date()
                date_manufacture = datetime.datetime.strptime(date_manufacture_entry.get(), "%d/%m/%Y").date()
                description = description_text.get("1.0", END).strip()
                
                if date_manufacture > datetime.date.today(): # Future Date of Manufacture validation error.
                    messagebox.showerror("Error", "Date of Manufacture cannot be in the future!")
                    return

                if date_added > datetime.date.today(): # Date added set for future validation error
                    messagebox.showerror("Error", "Date Added cannot be in the future!!")
                    return

                
                item = {
                    "Title": title,
                    "Date Added": date_added,
                    "Date of manufacture": date_manufacture,
                    "Description": description
                }
                collection[item_type].append(item)
                self.save_data()  # Save after adding item
                messagebox.showinfo("Success", "Item Added Successfully!")
                add_window.destroy()
                self.show_items_window()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid dates in DD/MM/YYYY format")
        
        ttk.Button(add_window, text="Add Item", cursor="hand2", command=add_item_to_collection).grid(row=5, column=0, columnspan=2, pady=20)

    def sort_items_a_z(self):
        global collection # Variable from the collection
        sorted_collection_a_z = {key: collection[key] for key in sorted(collection.keys())}
        collection = sorted_collection_a_z  # Replace the original collection with the sorted one
        self.show_items_window()  # Refresh display

    def sort_items_z_a(self):
        global collection
        sorted_collection_z_a = {key: collection[key] for key in sorted(collection.keys(), reverse=True)}
        collection = sorted_collection_z_a # replaces the original collection with the sorted one
        self.show_items_window() # refresh the display

    def show_items_window(self):
        self.display_area.delete(1.0, END)
        for item_type, items in collection.items():
            self.display_area.insert(END, f"\n=== {item_type} ===\n")
            if not items:
                self.display_area.insert(END, "No items in this category\n")
            for item in items:
                self.display_area.insert(END, f"\nTitle: {item['Title']}\n")
                # Use strftime to format the date in DD/MM/YYYY format
                date_added_str = item['Date Added'].strftime("%d/%m/%Y") if isinstance(item['Date Added'],
                                                                                       datetime.date) else item[
                    'Date Added']
                date_manufacture_str = item['Date of manufacture'].strftime("%d/%m/%Y") if isinstance(
                    item['Date of manufacture'], datetime.date) else item['Date of manufacture']
                self.display_area.insert(END, f"Date Added: {date_added_str}\n")
                self.display_area.insert(END, f"Date of Manufacture: {date_manufacture_str}\n")
                self.display_area.insert(END, f"Description: {item['Description']}\n")
                self.display_area.insert(END, "-" * 40 + "\n")

    def show_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messagebox.showinfo("Current Time", f"The current time is: {current_time}")

    def show_delete_window(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Item")
        delete_window.geometry("400x300")
        delete_window.iconbitmap("assets/win98.ico")
        
        ttk.Label(delete_window, text="Select Type:").grid(row=0, column=0, pady=5, padx=5)
        type_var = StringVar()
        type_combo = ttk.Combobox(delete_window, textvariable=type_var, values=list(collection.keys()))
        type_combo.grid(row=0, column=1, pady=5, padx=5)
        
        items_listbox = Listbox(delete_window, width=40, height=10)
        items_listbox.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        
        def update_items_list(*args):
            items_listbox.delete(0, END)
            selected_type = type_var.get()
            for idx, item in enumerate(collection[selected_type], 1):
                items_listbox.insert(END, f"{idx}. {item['Title']}")
        
        type_var.trace('w', update_items_list)
        
        def delete_selected_item():
            selected_type = type_var.get()
            if not selected_type:
                messagebox.showerror("Error", "Please select a type")
                return
            
            selection = items_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select an item to delete")
                return
                
            idx = selection[0]
            removed_item = collection[selected_type].pop(idx)
            confirm = messagebox.askyesno("Confirm Deletion",
                                          f"Are you sure you want to delete '{removed_item['Title']}'?")
            if confirm:
                self.save_data()  # Save after deleting item
                messagebox.showinfo("Success", f"Deleted item: {removed_item['Title']}")
                update_items_list()
                self.show_items_window()
            else:
                # If user cancels, re-insert the removed item
                collection[selected_type].insert(idx, removed_item)
        ttk.Button(delete_window, text="Delete Selected", cursor="hand2", command=delete_selected_item).grid(row=2, column=0, columnspan=2, pady=20)

    def show_edit_window(self):
        edit_select_window = Toplevel(self.root)
        edit_select_window.title("Select Item to Edit")
        edit_select_window.geometry("400x300")
        edit_select_window.iconbitmap("assets/win98.ico")
        
        ttk.Label(edit_select_window, text="Select Type:").grid(row=0, column=0, pady=5, padx=5)
        type_var = StringVar()
        type_combo = ttk.Combobox(edit_select_window, textvariable=type_var, values=list(collection.keys()))
        type_combo.grid(row=0, column=1, pady=5, padx=5)
        
        items_listbox = Listbox(edit_select_window, width=40, height=10)
        items_listbox.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        
        def update_items_list(*args):
            items_listbox.delete(0, END)
            selected_type = type_var.get()
            for idx, item in enumerate(collection[selected_type], 1):
                items_listbox.insert(END, f"{idx}. {item['Title']}")
        
        type_var.trace('w', update_items_list)
        
        def edit_selected_item():
            selected_type = type_var.get()
            if not selected_type:
                messagebox.showerror("Error", "Please select a type")
                return
            
            selection = items_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select an item to edit")
                return
            
            idx = selection[0]
            item = collection[selected_type][idx]
            edit_select_window.destroy()
            self.open_edit_form(selected_type, idx, item)
        
        ttk.Button(edit_select_window, text="Edit Selected", cursor="hand2", command=edit_selected_item).grid(row=2, column=0, columnspan=2, pady=20)

    def open_edit_form(self, item_type, idx, item):
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Item")
        edit_window.geometry("500x400")
        edit_window.iconbitmap("assets/win98.ico")

        # Create form fields
        ttk.Label(edit_window, text="Title:").grid(row=0, column=0, pady=5, padx=5)
        title_entry = ttk.Entry(edit_window)
        title_entry.insert(0, item['Title'])
        title_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(edit_window, text="Type:").grid(row=1, column=0, pady=5, padx=5)
        type_var = StringVar(value=item_type)
        type_combo = ttk.Combobox(edit_window, textvariable=type_var, values=list(collection.keys()))
        type_combo.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(edit_window, text="Date Added (dd/mm/yyyy):").grid(row=2, column=0, pady=5, padx=5)
        date_added_entry = ttk.Entry(edit_window)

        # Ensure item['Date Added'] is a string before using strptime()
        date_added_str = item['Date Added'] if isinstance(item['Date Added'], str) else item['Date Added'].strftime('%d/%m/%Y')
        date_added = datetime.datetime.strptime(date_added_str, "%d/%m/%Y").date()
        date_added_entry.insert(0, date_added.strftime("%d/%m/%Y"))
        date_added_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(edit_window, text="Date of Manufacture (dd/mm/yyyy):").grid(row=3, column=0, pady=5, padx=5)
        date_manufacture_entry = ttk.Entry(edit_window)

        # Ensure item['Date of manufacture'] is a string before using strptime()
        date_manufacture_str = item['Date of manufacture'] if isinstance(item['Date of manufacture'], str) else item['Date of manufacture'].strftime('%d/%m/%Y')
        date_manufacture = datetime.datetime.strptime(date_manufacture_str, "%d/%m/%Y").date()
        date_manufacture_entry.insert(0, date_manufacture.strftime("%d/%m/%Y"))
        date_manufacture_entry.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(edit_window, text="Description:").grid(row=4, column=0, pady=5, padx=5)
        description_text = Text(edit_window, height=3, width=30)
        description_text.insert("1.0", item['Description'])
        description_text.grid(row=4, column=1, pady=5, padx=5)

        
        def save_edited_item():
            try:
                new_title = title_entry.get()
                new_type = type_var.get()
                new_date_added = datetime.datetime.strptime(date_added_entry.get(), "%d/%m/%Y").date()
                new_date_manufacture = datetime.datetime.strptime(date_manufacture_entry.get(), "%d/%m/%Y").date()
                new_description = description_text.get("1.0", END).strip()
                
                if new_date_manufacture > datetime.date.today():
                    messagebox.showerror("Error", "Date of Manufacture cannot be in the future!")
                    return
                
                edited_item = {
                    "Title": new_title,
                    "Date Added": new_date_added,
                    "Date of manufacture": new_date_manufacture,
                    "Description": new_description
                }
                
                # Remove item from old category if category changed
                if new_type != item_type:
                    collection[item_type].pop(idx)
                    collection[new_type].append(edited_item)
                else:
                    collection[item_type][idx] = edited_item
                
                self.save_data()  # Save after editing item
                messagebox.showinfo("Success", "Item Updated Successfully!")
                edit_window.destroy()
                self.show_items_window()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid dates in DD/MM/YYYY format")
        
        ttk.Button(edit_window, text="Save Changes", cursor="hand2", command=save_edited_item).grid(row=5, column=0, columnspan=2, pady=20)

        # Play sound function
    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sound.mp3")
        pygame.mixer.music.play()



def main():
    root = Tk()
    RetroCollectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()