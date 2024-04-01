
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.font import Font
import models
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import os
class project(tk.Tk):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.init__project()
        self.style = Style('flatly')
        self.main_gui()
        self.set_config()
    def init__project(self):
        self.title("Search")
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.ico")
        self.iconbitmap(icon_path)
        style = Style(theme='litera')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
    def main_gui(self):
        self.search_bar()
        self.nav()
        self.nav_notifications()
        self.set_table_body()
        pass
    def search_bar(self):
        search_bar = ttk.Frame(self)
        search_bar.grid(row=0, column=0, sticky='ew')
        default_font = Font(family="Arial", size=16)
        self.change_var_search_text = tk.StringVar()
        self.search_entry = ttk.Entry(search_bar,textvariable=self.change_var_search_text,  font=default_font)
        self.search_entry.grid(row=0, column=0, padx=5, pady=10, sticky='ew')
        self.tracker_checkbox_var = tk.IntVar()
        self.tracker_search = ttk.Checkbutton(search_bar,variable=self.tracker_checkbox_var, text="track search field",style='Roundtoggle.Toolbutton')
        self.tracker_search.grid(row=0,column=1)
        self.search_button = ttk.Button(search_bar, text="Search", padding=(10, 10)) #command=search_table
        self.search_button.grid(row=0, column=2, padx=(5, 10), pady=(5, 5), sticky='ew')
        search_bar.columnconfigure(2, weight=10)
        search_bar.columnconfigure(1, weight=2)
        search_bar.columnconfigure(0, weight=100)
    def nav(self):
        nav = ttk.Frame(self)
        nav.grid(row=1, column=0,  sticky='ew')
        self.upload_file = ttk.Button(nav, text="upload file",padding=(15,10)) #,command
        self.upload_file.grid(row=0, column=1, padx=5, pady=5,sticky='ew')
        self.export_file = ttk.Button(nav, text="export file",padding=(15,10)) #,command=export_output
        self.export_file.grid(row=0, column=2, padx=5, pady=5,sticky='ew')
        self.slider = ttk.Scale(nav, from_=0, to=100,length=400)
        self.slider.grid(row=0,column=3,padx=5, pady=5,sticky='ew')
        self.value_label = tk.Label(nav, text=f"Value:{80}")
        self.value_label.grid(row=1, column=3, padx=10, pady=10)
        self.slider.set(80)
        nav.columnconfigure(1,weight=2)
        nav.columnconfigure(2,weight=2)
        nav.columnconfigure(3,weight=20)
    def nav_notifications(self):
        labels = ttk.Frame(self)
        labels.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.status = ttk.Label(labels, text="",padding=(3,3))
        self.status.grid(row=3, column=1, pady=5)
        self.path = ttk.Label(labels, text="")
        self.path.grid(row=4, column=1, pady=5)
        labels.columnconfigure(0, weight=2)
        labels.columnconfigure(1, weight=2)
        labels.columnconfigure(2, weight=2)
    def set_table_body(self):
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.grid(row=0, column=1, sticky='ns')
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.grid(row=1, column=0, sticky='ew')

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Site ID", "Hub", "MTX", "Target SecGw MTX", "Site S1 (inner)", "Site S1 Mask (inner)", "Site X2 (inner)", "Site X2 Mask (inner)"),
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            show="headings"
        )

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        # Define column widths
        column_widths = {
            "Site ID": 150,
            "Hub": 50,
            "MTX": 50,
            "Target SecGw MTX": 50,
            "Site S1 (inner)": 50,
            "Site S1 Mask (inner)": 20,
            "Site X2 (inner)": 50,
            "Site X2 Mask (inner)": 20
        }

        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

            self.tree.column(col, width=column_widths[col])

        self.tree.grid(row=0, column=0, sticky='nsew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Configure a custom style for the Treeview headings
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14,'bold'))
        style.configure("Treeview.Cell", font=("Arial", 13))
        style.configure("Treeview", rowheight=30)
    def set_config(self):
        self.upload_file.configure(command=self.upload_file_process)
        self.search_button.configure(command=self.search_on_text)
        self.slider.configure(command=self.slider_changed)
        self.tracker_search.configure(command=self.tracker_search_process)
    def tracker_search_process(self,*args,**kwargs):
        print('------------')
        if self.tracker_checkbox_var.get() == 1:
            self.search_entry.bind("<KeyRelease>", self.search_on_text)
        else:
            self.search_entry.unbind("<KeyRelease>")
    def check_error(func):
        def wrapper(self,*args, **kwargs):
            try:
                return func(self,*args, **kwargs)
            except Exception as e:
                self.noticfication_message(f'Error in {e} ',1)
                return None  
        return wrapper
    @check_error
    def search_on_text(self,*args,**kwargs):
        self.put_data_into_table(just_size := self.table.search_on_text(self.search_entry.get().strip().lower()
                                                           ,int(self.slider.get())))
        self.noticfication_message(f'the output of search is {just_size.shape[0]} record at threshold {int(self.slider.get())}',0)
        self.export_file.configure(command=self.export_file_process)
        pass
    @check_error
    def export_file_process(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("output", "*.csv")])
        if file_path:
            self.table.export_file(file_path)
    @check_error
    def slider_changed(self,*args,**kwargs):
        self.put_data_into_table(just_size := self.table.change_threshold(int(self.slider.get())))
        self.noticfication_message(f'threshold changed to  {int(self.slider.get())} number of record {just_size.shape[0]}',0)
        self.value_label.configure(text=f"Value: {int(self.slider.get())}")
    @check_error
    def noticfication_message(self,msg,type_msg):
        if type_msg==0:
            self.status.config(text=msg)
            self.status.configure(background="green", foreground="white")
        elif type_msg==1:
            self.status.config(text=msg)
            self.status.configure(background="red", foreground="white")
        else:
            self.status.config(text=msg)
            self.status.configure(background="black", foreground="white")
    @check_error
    def upload_file_process(self):
        self.tree.delete(*self.tree.get_children())
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])

        if file_path:
            try:
                self.table=models.file_get(file_path)
                self.put_data_into_table(self.table.data_frame.head(100))
                self.path.config(text=f"The success file has been uploaded {file_path} number of records is {self.table.data_frame.shape[0]}")
                self.noticfication_message(f'success file has been uploaded',0)
            except Exception as e:
                self.noticfication_message(f'some thing error {e}',1)
                pass
        else:
            self.noticfication_message(f'File not specified',2)
            self.path.config(text=f"there is no file |:(")
            pass

    def put_data_into_table(self,df):      
        self.tree.delete(* self.tree.get_children())
        df=df.head(100)
        for index, row in df.iterrows():
            values =  tuple(row.tolist())
            self.tree.insert("", "end", values=values)

        

        
if __name__=="__main__":
    my_project=project()
    my_project.mainloop()