# Run -> python csv_xls.py --xls_file_name filename

import pandas as pd 
from tkinter import *
from tkinter import filedialog 
from tkinter import messagebox as msg 
from pandastable import Table 
from tkintertable import TableCanvas 
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--xls_file_name", required=True)

args = vars(ap.parse_args())
   
  
class csv_to_excel: 
   
    def __init__(self, root): 
   
        self.root = root 
        self.file_name = '' 
        self.f = Frame(self.root, 
                       height = 200, 
                       width = 300) 
          
        # Place the frame on root window 
        self.f.pack() 
           
        # Creating label widgets 
        self.message_label = Label(self.f, 
                                   text = 'CSV TO XLS', 
                                   font = ('Arial', 19,'underline'), 
                                   fg = 'Green') 
        self.message_label2 = Label(self.f, 
                                    text = 'Converter of CSV to Excel file', 
                                    font = ('Arial', 14,'underline'), 
                                    fg = 'Red') 
   
        # Buttons 
        self.convert_button = Button(self.f, 
                                     text = 'Convert', 
                                     font = ('Arial', 14), 
                                     bg = 'Orange', 
                                     fg = 'Black', 
                                     command = self.convert_csv_to_xls) 
        self.exit_button = Button(self.f, 
                                  text = 'Exit', 
                                  font = ('Arial', 14), 
                                  bg = 'Red', 
                                  fg = 'Black',  
                                  command = root.destroy) 
   
        # Placing the widgets using grid manager 
        self.message_label.grid(row = 1, column = 1) 
        self.message_label2.grid(row = 2, column = 1) 
        self.convert_button.grid(row = 3, column = 0, 
                                 padx = 0, pady = 15) 
        self.exit_button.grid(row = 3, column = 2, 
                              padx = 10, pady = 15) 
   
    def convert_csv_to_xls(self): 
        try: 
            self.file_name = filedialog.askopenfilename(initialdir = '/Desktop', 
                                                        title = 'Select a CSV file', 
                                                        filetypes = (('csv file','*.csv'), 
                                                                     ('csv file','*.csv'))) 
               
            df = pd.read_csv(self.file_name) 
              
            # Next - Pandas DF to Excel file on disk 
            if(len(df) == 0):       
                msg.showinfo('No Rows Selected', 'CSV has no rows') 
            else: 
                  
                # saves in the current directory 
                with pd.ExcelWriter(args["xls_file_name"] + '.xls') as writer: 
                        df.to_excel(writer,'GFGSheet') 
                        writer.save() 
                        msg.showinfo('Excel file ceated', 'Excel File created')      
               
        except FileNotFoundError as e: 
                msg.showerror('Error in opening file', e)  
  
# Driver Code  
root = Tk() 
root.title('GFG---Convert CSV to Excel File') 
   
obj = csv_to_excel(root) 
root.geometry('800x600') 
root.mainloop() 
