import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
from readExcel import readExcel
from resultToJson import resultToJson


root = TkinterDnD.Tk()
root.title("Excel to CRM")


frame = tk.Frame(root, padx=20, pady=20)
frame.pack()


# Create a "Proceed" button
def proceed_clicked():
    def drop(event):
        file_path = event.data
        excelData = readExcel(file_path)
        resultToJson(excelData)
    label = tk.Label(frame, text="Drop an Excel file here:")
    label.pack()
    drop_target = tk.Label(frame, text="Drop Here", borderwidth=2, relief="groove")
    drop_target.pack(pady=10)
    drop_target.drop_target_register(DND_FILES)
    drop_target.dnd_bind('<<Drop>>', drop)

empID = tk.Entry(frame)
empID.pack()
proceed_button = tk.Button(frame, text="Proceed", command=proceed_clicked)
proceed_button.pack()

root.mainloop()
