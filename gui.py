import tkinter as tk
from tkinter import filedialog
from solution import generate_questions_for_obsidian_files
def browse_folder():
    folder_path_input.delete(0, tk.END)
    folder_path_input.insert(0, filedialog.askdirectory())

def start_processing():
    api_key = api_key_input.get().strip()
    folder_path = folder_path_input.get().strip()
    search_tags = search_tags_input.get().strip()
    target_deck = target_deck_input.get().strip()
    custom_tags = custom_tags_input.get().strip()

    search_tags_list = [tag.strip() for tag in search_tags.split(',')]
    new_folder_path = generate_questions_for_obsidian_files(api_key, folder_path, search_tags_list, target_deck, custom_tags)
    status_label.config(text=f"Processing complete. New files saved in: {new_folder_path}")



# Create the main tkinter window
root = tk.Tk()
root.title("Question Generator")

# Configure the grid weights for responsiveness
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)

# Create input fields and labels
api_key_label = tk.Label(root, text="OpenAI API Key:")
api_key_label.grid(row=0, column=0, padx=5, pady=5)
api_key_input = tk.Entry(root, width=50)
api_key_input.grid(row=0, column=1, padx=5, pady=5)

folder_path_label = tk.Label(root, text="Folder Path:")
folder_path_label.grid(row=1, column=0, padx=5, pady=5)
folder_path_input = tk.Entry(root, width=50)
folder_path_input.grid(row=1, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=5, pady=5)

search_tags_label = tk.Label(root, text="Search Tags:")
search_tags_label.grid(row=2, column=0, padx=5, pady=5)
search_tags_input = tk.Entry(root, width=50)
search_tags_input.grid(row=2, column=1, padx=5, pady=5)

target_deck_label = tk.Label(root, text="Target Deck:")
target_deck_label.grid(row=3, column=0, padx=5, pady=5)
target_deck_input = tk.Entry(root, width=50)
target_deck_input.grid(row=3, column=1, padx=5, pady=5)

custom_tags_label = tk.Label(root, text="Custom Tags:")
custom_tags_label.grid(row=4, column=0, padx=5, pady=5)
custom_tags_input = tk.Entry(root, width=50)
custom_tags_input.grid(row=4, column=1, padx=5, pady=5)

process_button = tk.Button(root, text="Generate Questions", command=start_processing)
process_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Run the tkinter main loop
root.mainloop()