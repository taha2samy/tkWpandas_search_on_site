import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.font import Font
import models
from ttkbootstrap import Style
table=models.pd.DataFrame()
output=''
def search_table(*args):
    try:
        global tree,table,search_entry,status,output
        tree.delete(*tree.get_children())
        search_term = search_entry.get().strip().lower()
        output = models.search(int(slider.get()),table,search_term)
        put_data_into_table(output)
        status.config(text=f'the output of search is {output.shape[0]} record')
        status.configure(background="green", foreground="white")
    except:
        status.config(text=f'something wrong in')
        status.configure(background="red", foreground="white")


def put_data_into_table(df):      
    global tree
    tree.delete(*tree.get_children())
    for index, row in df.iterrows():
        values =  tuple(row.tolist())
        print(values)
        tree.insert("", "end", values=values)

def select_xlsx_file():
    global path,table,status
    tree.delete(*tree.get_children())
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            table=models.read_file(file_path)
            put_data_into_table(table.head(100))
            path.config(text=f"The success file has been uploaded {file_path} number of records is {table.shape[0]}")
            status.config(text=f'success file has been uploaded')
            status.configure(background="green", foreground="white")
        except Exception as e:
            status.config(text=f'some thing error {e}')
            status.configure(background="red", foreground="white")
            pass
    else:
        status.config(text=f'File not specified')
        status.configure(background="black", foreground="white")
        path.config(text=f"|:(")
        pass
def on_checkbox_clicked():
    global search_entry
    if checkbox_var.get() == 1:
        print("Checkbox is checked")
        search_entry.bind("<KeyRelease>", search_table)

    else:
        print("Checkbox is unchecked") 
        search_entry.unbind("<KeyRelease>")  
def slider_changed(*args):
    global value_label
    value_label.config(text=f"Value: {int(slider.get())}")
    search_table()
def export_output():
    global output
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("output", "*.csv")])
    if file_path:
        try:
            output.to_csv(file_path, index=False)
            status.config(text=f'The file has been successfully saved')
            status.configure(background="green", foreground="white")
        except:
            status.config(text=f'There is an error in the saving process')
            status.configure(background="red", foreground="white")
        pass
    else:
        status.config(text=f'No path has been specified for saving')
        status.configure(background="black", foreground="white")

        
        
root = tk.Tk()
root.title("Search Table")
root.iconbitmap('home.ico')
style = Style(theme='litera')

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
search_bar = ttk.Frame(root)
search_bar.grid(row=0, column=0, sticky='ew')
default_font = Font(family="TkDefaultFont", size=16)

search_text = tk.StringVar()
search_entry = ttk.Entry(search_bar,textvariable=search_text,  font=default_font)
search_entry.grid(row=0, column=0, padx=5, pady=10, sticky='ew')



checkbox_var = tk.IntVar()
checkbox = ttk.Checkbutton(search_bar, text="track search field", variable=checkbox_var, command=on_checkbox_clicked)
checkbox.grid(row=0,column=1)

search_button = ttk.Button(search_bar, text="Search", padding=(10, 5), command=search_table)
search_button.grid(row=0, column=2, padx=(5, 10), pady=(5, 5), sticky='ew')

search_bar.columnconfigure(2, weight=10)
search_bar.columnconfigure(1, weight=2)
search_bar.columnconfigure(0, weight=100)
root.columnconfigure(0, weight=1)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
body = ttk.Frame(root)
body.grid(row=1, column=0,  sticky='ew')
upload_file = ttk.Button(body, text="upload file",command=select_xlsx_file,padding=(8,8))
upload_file.grid(row=0, column=1, padx=5, pady=5,)
export_file = ttk.Button(body, text="export file",padding=(8,8),command=export_output)
export_file.grid(row=0, column=2, padx=5, pady=5)
button3 = ttk.Button(body, text="Button 3",padding=(8,8))
slider = ttk.Scale(body, from_=0, to=100, orient="horizontal",length=300)
slider.grid(row=0,column=3,padx=5, pady=5)
value_label = tk.Label(body, text=f"Value:{80}")
value_label.grid(row=1, column=3, padx=10, pady=10)
slider.set(80)




#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

labels = ttk.Frame(root)
labels.grid(row=2, column=0, columnspan=2, sticky='ew')
status = ttk.Label(labels, text="",padding=(3,3))
status.grid(row=3, column=1, pady=5)
path = ttk.Label(labels, text="")
path.grid(row=4, column=1, pady=5)
labels.columnconfigure(0, weight=2)
labels.columnconfigure(1, weight=2)
labels.columnconfigure(2, weight=2)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
tree_frame = ttk.Frame(root)
tree_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')

root.rowconfigure(3, weight=1)

# Create Scrollbars
tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_y.grid(row=0, column=1, sticky='ns')
tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
tree_scroll_x.grid(row=1, column=0, sticky='ew')


# Create Treeview
tree = ttk.Treeview(
    tree_frame,
    columns=("Site ID", "Hub", "MTX", "Target SecGw MTX", "Site S1 (inner)", "Site S1 Mask (inner)", "Site X2 (inner)", "Site X2 Mask (inner)"),
    yscrollcommand=tree_scroll_y.set,
    xscrollcommand=tree_scroll_x.set,
    show="headings",
    style="Treeview.Treeview"  # Hide indexing column
)
tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)
# Set Scrollbar commands

# Define column widths
column_widths = {
    "Site ID": 30,
    "Hub": 150,
    "MTX": 50,
    "Target SecGw MTX": 50,
    "Site S1 (inner)": 50,
    "Site S1 Mask (inner)": 20,
    "Site X2 (inner)": 50,
    "Site X2 Mask (inner)": 20
}

# Configure columns
for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, width=column_widths[col])

# Pack the treeview widget
tree.grid(row=0, column=0, sticky='nsew')

# Configure tree_frame to expand
tree_frame.rowconfigure(0, weight=1)
tree_frame.columnconfigure(0, weight=1)


slider.configure(command=slider_changed)
root.mainloop()
