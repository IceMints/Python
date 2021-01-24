"""
CISP71 Fall 2020
Implementing a Tkinter GUI program with CRUD sqlite database backend
Import database class
Create a desktop application to create, read, update, delete, retrieve all records from that table
The user interface should have Labels, Entry, OptionMenu, TextArea or treeview, and Buttons widgets.
The application needs to create, update, delete records.

"""
from tkinter import *
# import for message boxes
import tkinter.messagebox as mb
# import for Treeview
import tkinter.ttk as ttk
from PIL import Image, ImageTk
# import the Database class that was created in GHUI_Tkinter_Create_DB python file
from GHUI_Tkinter_Create_DB import Database


# creating the parent window
root = Tk()
# title of window
root.title('Fruit Bar')
# specify the size of parent window, and location of loading
root.geometry('1010x280+351+174')

# Fruity.jpg image from https://www.berries.com/blog/wp-content/uploads/2019/06/SB-Fruit-Cutting-hero-1.jpg
# using PIL, placed fruity.jpg as the background image for application.

# used try and except so the program will load with or without the .jpg file
try:
    # open image from file
    image = Image.open('fruity.jpg')
    # have Image convert and formate to something Tkinter can use
    photo_image = ImageTk.PhotoImage(image)
    # placed the image in the background like wallpaper
    lblImage = Label(root, image = photo_image)
    lblImage.pack()
except:
    pass


# create a path variable
path = ""

# create an object of Database class from GHUI_TKinter_Create_DB python file
db = Database(path+'Fruit.db')

"""
Declare functions that will be called with button presses
"""
# clears the entry of all the characters from index 0 to the end of the contents of the entry widget
def clear_form():
    entFruitID.delete(0, END)
    entFruit.delete(0, END)
    entDescription.delete(0, END)
    entPrice.delete(0, END)
    selected_supplier.set(supplier_list[0])

def exit():
    MsgBox = mb.askquestion('Exit', 'Are you sure you want to exit?', icon='warning')
    if MsgBox == 'yes':
        #add close connection
        root.destroy()

def delete_fruit():
    if entFruitID.get()=='':
        mb.showinfo('Information', 'Select a fruit to delete')
        return
    MsgBox = mb.askquestion('Delete Fruit?', 'Are you sure you want to delete this fruit?', icon='warning')
    if MsgBox == 'yes':
        db.delete(entFruitID.get())
        # call the function to clear entry boxes
        clear_form()
        # call the function to load data
        display_fruits()

def validate_entry():
    # validating entry widgets
        if entFruit.get().strip() == '':
            mb.showinfo('Information', 'Please enter fruit name')
            entFruit.focus_set()
            return False
        if entDescription.get().strip() == '':
            mb.showinfo('Information', 'Please enter description of fruit')
            entDescription.focus_set()
            return False
        if entPrice.get().strip() == '':
            mb.showinfo('Information', 'Please enter cost of fruit')
            entPrice.focus_set()
            return False
        if selected_supplier.get().strip() == '':
            mb.showinfo('Information', 'Please enter the supplier')
            return False

def add_fruit():
    if validate_entry() != False:
    # call insert method of the database class and pass values entered
    #if entFruit.get().strip() is not '' and entDescription.get().strip() is not '' and entPrice.get().strip() is not '' and selected_supplier.get().strip() is not '':
        db.insert(entFruit.get(), entDescription.get(), entPrice.get(), selected_supplier.get())
        # clear form
        clear_form()
        # load data
        display_fruits()
    else:
        return

# show selected fruit
def show_selected_fruit(event):
    clear_form()
    for selection in tvFruit.selection():
        item = tvFruit.item(selection)
        fruitID, fruit, description, price, supplier = item['values'][0:5]
        entFruitID.insert(0, fruitID)
        entFruit.insert(0, fruit)
        entDescription.insert(0, description)
        entPrice.insert(0, price)
        selected_supplier.set(supplier)

def update_fruit_data():
    if validate_entry() != False:
        # call the insert method of the database class and pass values entered
        db.update(entFruitID.get(), entFruit.get(), entDescription.get(), entPrice.get(), selected_supplier.get())
        # call the method to clear entry boxes
        clear_form()
        # call the load method
        display_fruits()
    else:
        return

def display_fruits():
    for row in tvFruit.get_children():
        tvFruit.delete(row)
    for row in db.fetch():
        fruitID = row[0]
        fruit = row[1]
        description = row[2]
        price = row[3]
        supplier = row[4]
        tvFruit.insert("", 'end', text=fruitID, values=(fruitID, fruit, description, price, supplier))

# create entry widgets
entFruitID = Entry(root)
entFruit = Entry(root)
entDescription = Entry(root)
entPrice = Entry(root)
#entSupplier = Entry(root) //changed to optionMenu, entry no longer necessary

# create a list for drop down list or option menu
supplier_list = ['', 'Farmer\'s Market', 'Albertsons', 'Smart & Final', 'Ralphs']

# define selected variable for drop down list or option menu
selected_supplier = StringVar()

# set a default value for the drop down list or option menu to first item on list
selected_supplier.set(supplier_list[0])

"""
Create labels that will be used in the geometry window
Create buttons and bind functions to button widgets
(http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter)
"""
# create a label widget for the title
lblTitle = Label(root, text='Fruit Bar', font=('Helvetica', 16), fg = "deep pink", bg = "#ffffff")

# create label widgets for each field
lblFruitID = Label(root, text='FruitID', font=('Helvetica', 10), bg = "#ffffff")
lblFruit = Label(root, text='Fruit:', font=('Helvetica', 10), bg = "#ffffff")
lblDescription = Label(root, text='Description:', font=('Helvetica', 10), bg = "#ffffff")
lblPrice = Label(root, text='Price:', font=('Helvetica', 10), bg = "#ffffff")
lblSupplier = Label(root, text='Supplier:', font=('Helvetica', 10), bg = "#ffffff")

# create button widgets
btnCreate = Button(root, text='Add', font=('Helvetica', 11), command=add_fruit)
btnUpdate = Button(root, text='Update', font=('Helvetica', 11), command=update_fruit_data)
btnDelete = Button(root, text='Delete', font=('Helvetica', 11), command=delete_fruit)
btnClear = Button(root, text='Clear', font=('Helvetica', 11), command=clear_form)
#btnDisplay = Button(root, text='Display', font=('Helvetica', 11), command=display_fruits) //display button not needed atm
btnExit = Button(root, text='Exit', font=('Helvetica', 16), command=exit)

# create an OptionMenu widget or drop down list for the supplier field
OptSupplier = OptionMenu(root, selected_supplier, *supplier_list)

"""
Use Treeview to place the objects on the geometry window
"""
# creating a Treeview widget
# specify tuple columns
columns = ('#1', '#2', '#3', '#4', '#5')

# create a Treeview widget and specify the columns
tvFruit = ttk.Treeview(root, show='headings', height='5', columns=columns)

# specify the respective column with heading
tvFruit.heading('#1', text='FruitID', anchor='center')
tvFruit.column('#1', width=45, anchor='center', stretch=False)

tvFruit.heading('#2', text='Fruit', anchor='center')
tvFruit.column('#2', width=10, anchor='center', stretch=True)

tvFruit.heading('#3', text='Description', anchor='center')
tvFruit.column('#3', width=10, anchor='center', stretch=True)

tvFruit.heading('#4', text='Price(ea)', anchor='center')
tvFruit.column('#4', width=10, anchor='center', stretch=True)

tvFruit.heading('#5', text='Supplier', anchor='center')
tvFruit.column('#5', width=10, anchor='center', stretch=True)

# add a verticle scroll bar
# Scroll bars are set up below with placement positions (x & y), height and width of treeview widget
# command to see the yaxis view of the treeview
vsb = ttk.Scrollbar(root, orient=VERTICAL, command=tvFruit.yview)

# place the vsb
vsb.place(x=420+550 + 1, y=40, height=180+20)

# configure the treeview that it will use the vsb for y-axis scrolling
tvFruit.configure(yscroll=vsb.set)

# create a horizontal scrollbar
hsb = ttk.Scrollbar(root, orient=HORIZONTAL, command=tvFruit.xview)

# place the hsb
hsb.place(x=420, y=40+200 + 1, width=530+20)

# configure the tree view to use the hsb to scroll x-axis horizontally
tvFruit.configure(xscroll=hsb.set)

# bind the tree view to the function show_selected_fruit
tvFruit.bind("<<TreeviewSelect>>", show_selected_fruit)

# place the labels
lblTitle.place (x=400, y=5, height=27, width=100)
#lblFruitID.place (x=63, y=40, height=23, width=50) //comment out so FruitID can't be seen or edit
lblFruit.place (x=68, y=60, height=23, width=45)
lblDescription.place (x=30, y=100, height=23, width=80)
lblPrice.place (x=60, y=140, height=23, width=50)
lblSupplier.place (x=43, y=180, height=23, width=66)

# place the entry widgets
#entFruitID.place (x=120, y=42, height=21, width=150) //comment out so FruitID can't be seen or edit
entFruit.place (x=120, y=60, height=21, width=150)
entDescription.place (x=120, y=100, height=21, width=150)
entPrice.place (x=120, y=140, height=21, width=150)
OptSupplier.place (x=120, y=180, height=21, width=150)

# place the button widgets
btnCreate.place (x=310, y=90, height=25, width=66)
btnUpdate.place (x=310, y=120, height=25, width=66)
btnDelete.place (x=310, y=160, height=25, width=66)
btnClear.place (x=310, y=40, height=25, width=66)
#btnDisplay.place (x=530, y=245, height=25, width=76) //display button not needed atm
btnExit.place (x=310, y=210, height=31, width=60)

# place the treeview widget
tvFruit.place (x=420, y=40, height=200, width=550)

# call display_fruits()
display_fruits()

# run until window close manually
root.mainloop()
