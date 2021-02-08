from tkinter import *
from tkinter import ttk, filedialog, messagebox
from pprint import pprint
import os
import glob
import json
import re
import ctypes
import string
import random
from ttkwidgets.autocomplete import AutocompleteCombobox

ctypes.windll.shcore.SetProcessDpiAwareness(2)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Reqtificator:

    def data_setup(self):
        self.section_tags = ["- skill section -", "- skill section2 -"]
        self.default_skill_dict = {}
        self.custom_skill_dict = {}

        self.default_skill_list = []
        self.custom_skill_list = []

        self.target_gbots_list = []

        self.settings = {}
        self.section_names = []

        self.find_files()
        self.retrieve_skills()
        self.retrieve_settings()

    def find_files(self):
        self.default_skills_location = glob.glob("./Skills/Default Skills/req_*.gbot")
        self.custom_skills_location = glob.glob("./Skills/Custom Skills/req_*.gbot")
        self.target_gbots_location = glob.glob("./Bots/*.gbot")
    
    def retrieve_settings(self):
        with open("./settings.json", "r", encoding="utf-8") as f:
            self.settings = json.load(f)
        self.section_names = self.settings["sections_names"]

    def save_settings(self):
        with open('./settings.json', 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)
    def retrieve_skills(self):
        for skill in self.default_skills_location:
            with open(skill, "r", encoding='utf-8') as f:
                gbot_skill = json.load(f)
            name = skill.split("\\")[1]
            name = re.sub("(req_)|(.gbot)|_", " ", name).lstrip().rstrip().capitalize()
            self.default_skill_dict[name] = gbot_skill["Commands"]["$values"]
        self.default_skill_list = [skill_name for skill_name in self.default_skill_dict]

        for skill in self.custom_skills_location:
            with open(skill, "r", encoding='utf-8') as f:
                gbot_skill = json.load(f)
            name = skill.split("\\")[1]
            name = re.sub("(req_)|(.gbot)|_", " ", name).lstrip().rstrip().capitalize()
            self.custom_skill_dict[name] = gbot_skill["Commands"]["$values"]
        self.custom_skill_list = [skill_name for skill_name in self.custom_skill_dict]

    def replace_skils(self):
        for gbot in self.target_gbots_location:
            gbot_name = gbot.split("\\")[-1]
            index = 0
            completed_section = []
            completed_skills = []
            target_skill = ""
            with open(gbot, "r", encoding='utf-8') as f:
                bot_json = json.load(f)
                
            for section in self.section_tags:
                values = bot_json["Commands"]["$values"]
                for i in values:
                    # print(index, ": ", i)
                    index += 1
                    if len(self.t_in) == 2:
                        index = 0
                        break
                    try:
                        name = str(i["Name"]).lstrip().rstrip()
                        if name == section:
                            if len(self.t_in) != 2:
                                self.t_in.append(index)
                    except: pass
                # print(self.t_in)
                target_skill = self.skill_list[self.skill[0]]
                self.skill.pop(0)

                # pprint(self.skill_list[target_skill])
                bot_json_2 = values[:self.t_in[0]+1] + target_skill + values[self.t_in[1]-1:]
                bot_json["Commands"]["$values"] = bot_json_2
                self.t_in = []
                # print("\n"*10)

            with open('./Results/test3.gbot', 'w', encoding='utf-8') as f:
                json.dump(bot_json, f, ensure_ascii=False, indent=4)
            continue

class GUI(Reqtificator):
    font = ("Calibri Light", 11)
    fs = "Calibri Light"
    bg = "White"
    fg = "Black"
    sub = "#f5f5f5"

    # rr = "#fc5d5d"
    # rr = "#f2f2f2"
    rr = bg

    select_bg = "#57a8ff"


    def __init__(self, master):
        self.master = master
        self.master.geometry("670x450+50+100")
        self.master.resizable(False, True)
        self.master["bg"] = "White"
        self.class_mode_var = StringVar()

        # Variables
        self.grim_folder = ""
        self.item_focus = ""

        # Reqtificator setups
        self.data_setup()
        self.retrieve_skills()

        # GUI setups
        # self.widget_style()
        self.menu_setup()
        self.widgets_setup()

        # Item insertions
        self.insert_files_dropdown()
        self.section_list_window()
        

    def widget_style(self):
        style = ttk.Style()

        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

    def menu_setup(self):
        # Widget checks
        self.section_is_opened = False



        # Menus
        self.menubar = Menu(self.master)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open File...")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.settings_menu = Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Section List", command=lambda: self.open_Toplevel("section_list"))
        self.settings_menu.add_command(label="Configurations")
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Advanced")
        self.menubar.add_cascade(label="Settings", menu=self.settings_menu)

        self.directory = Menu(self.menubar, tearoff=0)
        self.directory.add_command(label="Grim Bots Folder", command=self.select_folder )
        self.directory.add_command(label="Lab Bots Folder", command=lambda: os.startfile(os.path.realpath("./Bots")))
        self.directory.add_command(label="Results Folder", command=lambda: os.startfile(os.path.realpath("./Results")))
        self.directory.add_command(label="Default Skills Folder", command=lambda: os.startfile(os.path.realpath("./Skills/Default Skills")))
        self.directory.add_command(label="Custom Skills Folder", command=lambda: os.startfile(os.path.realpath("./Skills/Custom Skills")))
        self.menubar.add_cascade(label="Directories", menu=self.directory)

        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_command(label="Update")
        self.help.add_separator()
        self.help.add_command(label="About")
        self.help.add_command(label="Instructions")
        self.help.add_separator()
        self.help.add_command(label="Discord")
        self.menubar.add_cascade(label="Help", menu=self.help)

        self.menubar.add_command(label="Refresh", command=self.insert_files_dropdown)

        self.master.config(menu=self.menubar)

    def widgets_setup(self):
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        # Frame at TOP
        self.top_frame = Frame(self.master, bg=GUI.rr, width=700, height=30)
        self.top_frame.grid(row=0, column=0, columnspan=4, padx=(10), pady=10, sticky=N+W)

        self.top_label = Label(self.top_frame, text="Gbot:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.top_label.place(x=7, y=0)

        self.top_dropdown = AutocompleteCombobox(self.top_frame, font=GUI.font, completevalues=[])
        self.top_dropdown.bind('<Button-3>',self.rClicker, add='')
        self.top_dropdown.place(x=55, y=2, width=445, height=25)
        self.top_dropdown.bind("<<ComboboxSelected>>", lambda x: self.dropdown_focus())

        self.save_button = Button(self.top_frame, text="Save", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 11))
        self.save_button.place(x=502, y=1, height=27, width=70)

        self.load_button = Button(self.top_frame, text="Load", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 11))
        self.load_button.place(x=575, y=1, height=27, width=70)

        # Frame at the LEFT
        self.left_frame = Frame(self.master, bg=GUI.rr, width=350, height=400)
        self.left_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky=W+N+S)
        self.left_frame.rowconfigure(2, weight=1)

        self.left_label = Label(self.left_frame, text="Sections:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.left_label.grid(row=0, column=0,  pady=1, sticky=W+N)

        # self.left_dropdown = ttk.Combobox(self.left_frame, values=[], width=29, font=GUI.font)
        # self.left_dropdown.grid(row=1, column=0, columnspan=10, padx=(1), pady=1, sticky=N)

        self.left_dropdown = AutocompleteCombobox(self.left_frame, font=GUI.font, width=19, completevalues=[])
        self.left_dropdown.bind('<Button-3>',self.rClicker, add='')
        self.left_dropdown.grid(row=1, column=0, columnspan=10, padx=(1), pady=1, sticky=W+E+N)


        self.left_listbox = Listbox(self.left_frame, bg=GUI.sub, fg=GUI.fg, bd=1,
            width=29, height=10, relief=GROOVE, font=GUI.font,
            activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        self.left_listbox.grid(row=2, column=0, columnspan=9, padx=1, pady=1, sticky=S+N)

        self.left_scroll = Scrollbar(self.left_frame)
        self.left_listbox.config(yscrollcommand=self.left_scroll.set)
        self.left_scroll.config(command=self.left_listbox.yview)
        self.left_scroll.grid(row=2, column=9, padx=(1), pady=1, sticky=S+N)


        # Frame at the RIGHT
        self.right_frame = Frame(self.master, bg=GUI.rr, width=350, height=400)
        self.right_frame.grid(row=1, column=3, columnspan=2, padx=(15), pady=10, sticky=W+N+S)
        self.right_frame.rowconfigure(2, weight=1)

        self.right_label = Label(self.right_frame, text="Class Skills:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.right_label.grid(row=0, column=0,  pady=1, sticky=W+N)

        self.right_label2 = Label(self.right_frame, text="Using:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.right_label2.grid(row=0, column=5,  pady=1, sticky=W+N)

        self.right_switch = Button(self.right_frame, text="Default Skills", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 9), command=self.main_switch_skills)
        self.right_switch.place(x=200, y=31, height=29, width=88)

        self.skills_dropdown = AutocompleteCombobox(self.right_frame, font=GUI.font, width=19, completevalues=self.default_skill_list)
        self.skills_dropdown.current(0)
        self.skills_dropdown.bind('<Button-3>',self.rClicker, add='')
        self.skills_dropdown.grid(row=1, column=0, columnspan=5, padx=(1), pady=1, sticky=N+W)
        self.skills_dropdown.bind("<<ComboboxSelected>>", lambda x: self.insert_skills(x))

        self.skills_listbox = Listbox(self.right_frame, bg=GUI.sub, fg=GUI.fg, bd=1,
            width=29, height=10, relief=GROOVE, font=GUI.font,
            activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        self.skills_listbox.grid(row=2, column=0, columnspan=9, padx=1, pady=1, sticky=S+N)

        self.right_scroll = Scrollbar(self.right_frame)
        self.skills_listbox.config(yscrollcommand=self.right_scroll.set)
        self.right_scroll.config(command=self.skills_listbox.yview)
        self.right_scroll.grid(row=2, column=9, padx=(1), pady=1, sticky=S+N)


        # Frames at the bottom
        self.bottom_frame = Frame(self.master, bg=GUI.rr, width=700, height=30)
        self.bottom_frame.grid(row=3, column=0, columnspan=4, padx=13, pady=5, sticky=W+E+N)

        self.reset_section_button = Button(self.bottom_frame, text="Reset Section", bg=GUI.bg, fg=GUI.fg, relief=GROOVE, font=GUI.font)
        self.reset_section_button.place(x=80, width=120, height=27)

        self.set_section_button = Button(self.bottom_frame, text="Use Skills", bg=GUI.bg, fg=GUI.fg, relief=GROOVE, font=GUI.font)
        self.set_section_button.place(x=430, width=120, height=27)

    def dropdown_focus(self):
        self.top_frame.focus()
        # self.top_dropdown.focus_set()

    def section_list_window(self):
        self.section_list = Toplevel()
        self.section_list.protocol('WM_DELETE_WINDOW', lambda: self.close_Toplevel("section_list"))
        self.section_list.title("Section List")
        self.section_list.geometry("400x800+750+100")
        self.section_list["bg"] = GUI.bg
        self.section_list.rowconfigure(2, weight=1)

        self.section_is_opened = True

        # Intruction frame
        self.sl_instructions_frame = LabelFrame(self.section_list, text="Instructions",
            bg=GUI.rr, fg=GUI.fg)
        self.sl_instructions_frame.grid(row=0, column=0, columnspan=4, sticky=N+W+E,
            padx=12, pady=10)

        self.sl_instruction_text = Label(self.sl_instructions_frame,
            bg=GUI.bg, fg=GUI.fg, relief=FLAT, font=GUI.font, wraplength=380, justify=LEFT,
            text="The skill section names must be EXACTLY the same name as the "\
                 "ones inside the .gbot or else none of these will work. "\
                 "To Add a section name, choose what type of name it is and click Add."\
                 "To remove one, however, click on the item and click Del.")
        self.sl_instruction_text.pack(fill="both", expand="yes")

        # Button Frames
        self.sl_frame_2 = LabelFrame(self.section_list, text="Add/Remove Section Names",
            bg=GUI.rr, height=40)
        self.sl_frame_2.grid(row=1, column=0, columnspan=4, sticky=N+W+E,
            padx=12, pady=10, ipady=4)

        self.sl_drop = AutocompleteCombobox(self.sl_frame_2, font=GUI.font, width=19,
            completevalues=["Dual Named Section", "Single Named Section"])
        self.sl_drop.current(1)
        self.sl_drop.grid(row=0, column=1, columnspan=3, sticky=N+W+E, pady=5)
        self.sl_drop.bind("<<ComboboxSelected>>", lambda x: self.section_list_dropdown(x))

        self.sl_drop_label = Label(self.sl_frame_2, text="Type:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.sl_drop_label.grid(row=0, column=0, sticky=W, padx=5)


        self.sl_entry1 = Entry(self.sl_frame_2, bg=GUI.sub, fg=GUI.fg, 
            width=25, relief=GROOVE, font=GUI.font)
        self.sl_entry1.grid(row=1, column=1, columnspan=1, sticky=N+W+E, pady=5)
        self.sl_value_1_label = Label(self.sl_frame_2, text="Name 1:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.sl_value_1_label.grid(row=1, column=0, sticky=W, padx=5)
        self.sl_entry1.bind('<Button-3>',self.rClicker, add='')

        self.sl_entry2 = Entry(self.sl_frame_2, bg=GUI.sub, fg=GUI.fg, 
            width=25, relief=GROOVE, font=GUI.font)
        # self.sl_entry2.grid(row=2, column=1, columnspan=1, sticky=N+W+E, pady=5)
        self.sl_value_1_label = Label(self.sl_frame_2, text="Name 2:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.sl_entry2.bind('<Button-3>',self.rClicker, add='')
        # self.sl_value_1_label.grid(row=2, column=0, sticky=W, padx=5)


        self.sl_add = Button(self.sl_frame_2, text="Add", bg=GUI.sub, fg=GUI.fg, height=1,
            width=4, relief=GROOVE, font=GUI.font, command=self.add_sections)
        self.sl_add.place(x=310, y=42, width=50, height=29)

        self.sl_rem = Button(self.sl_frame_2, text="Del", bg=GUI.sub, fg=GUI.fg, height=1,
            width=4, relief=GROOVE, font=GUI.font, command=self.delete_section)
        self.sl_rem.place(x=310, y=5, width=50, height=29)

        # List box Frame
        self.sl_frame_3 = LabelFrame(self.section_list, text="Section Lists",
            bg=GUI.rr, height=40)
        self.sl_frame_3.grid(row=2, column=0, columnspan=4, sticky=N+S+E+W,
            padx=12, pady=10)

        self.sl_listbox = Listbox(self.sl_frame_3, bg=GUI.sub, fg=GUI.fg, bd=2, 
            width=38, height=10, relief=GROOVE, font=GUI.font,
            activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        self.sl_listbox.grid(row=0, column=0, sticky=W+S+N)
        
        self.sl_frame_3.rowconfigure(0, weight=1)
        self.sl_listbox.bind('<Double-Button-1>', self.section_edit_window)

        self.sl_scroll = Scrollbar(self.sl_frame_3)
        self.sl_listbox.config(yscrollcommand=self.sl_scroll.set)
        self.sl_scroll.config(command=self.sl_listbox.yview)
        self.sl_scroll.grid(row=0, column=1, padx=1, sticky=E+N+S)

        spacer = Label(self.section_list, text="  ", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        spacer.grid(row=3, column=0, columnspan=4, sticky=S+N+W+E)


        # Function inis
        # self.insert_section_names()
        self.insert_edit_section_list()

    def section_list_dropdown(self, event):
        type_ = self.sl_drop.get()
        self.section_list.focus()
        if type_ == "Dual Named Section":
            self.sl_entry2.grid(row=2, column=1, columnspan=1, sticky=N+W+E, pady=5)
            self.sl_value_1_label.grid(row=2, column=0, sticky=W, padx=5)
            return
        if type_ == "Single Named Section":
            self.sl_entry2.grid_forget()
            self.sl_value_1_label.grid_forget()
            return

    def section_edit_window(self, event):
        ind = self.sl_listbox.curselection()[0]

        item_ = self.sl_listbox.get(ind)
        if "[S]" in item_:
            item_ = item_.split("[S] ")[1]
        if "[D]" in item_: 
            item_ = item_.split("[D] ")[1]
        print(item_)
        item_key_ = ""
        for key in self.settings["sections_names"]:
            if self.settings["sections_names"][key]["value_1"] == item_:
                item_key_ = key
                break
        type_ = self.settings["sections_names"][item_key_]["type"]
        self.item_focus = (item_key_, type_, ind)
        value_1 = self.settings["sections_names"][item_key_]["value_1"]
        if type_ == "single":
            type_ = "Single Named Section"
            li = 18
        if type_ == "dual":
            type_ = "Dual Named Section"
            value_2 = self.settings["sections_names"][item_key_]["value_2"]
            li = 50

        s_height = 90 + li
        self.section_edit = Toplevel()
        self.section_edit.title("self.section_edit Edit")
        self.section_edit.geometry(f"400x{s_height}+700+100")
        self.section_edit.resizable(False, False)
        self.section_edit["bg"] = GUI.bg
        self.section_edit.focus()

        labelframe = Frame(self.section_edit, bg=GUI.rr, height=40)
        labelframe.pack(expand=1, fill='both')

        # text = Text(labelframe, bg=GUI.sub, fg=GUI.fg, width=25, height=6, relief=GROOVE, font=GUI.font)
        # text.pack(side=TOP, fill=X, pady=10, padx=10)

        label_type = Label(labelframe, text=f"Type:\t{type_}", bg=GUI.bg, fg=GUI.fg,
            width=33,font=GUI.font, anchor="w")
        label_type.place(x=5, y=5)

        self.entry1_edit = Entry(labelframe, bg=GUI.sub, fg=GUI.fg, width=33, relief=GROOVE, font=GUI.font)
        self.entry1_edit.place(x=80, y=35)
        self.entry1_edit_label = Label(labelframe, text="Name 1:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.entry1_edit.bind('<Button-3>',self.rClicker, add='')
        self.entry1_edit_label.place(x=5, y=35)
        self.entry1_edit.insert(0, value_1)

        if type_ == "Dual Named Section":
            self.entry2_edit = Entry(labelframe, bg=GUI.sub, fg=GUI.fg, width=33, relief=GROOVE, font=GUI.font)
            self.entry2_edit.insert(0, value_2)
            self.entry2_edit.place(x=80, y=70)
            self.entry2_edit.bind('<Button-3>',self.rClicker, add='')
            self.entry2_edit_label = Label(labelframe, text="Name 2:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
            self.entry2_edit_label.place(x=5, y=70)

        save_button = Button(labelframe, text="Save", bg=GUI.sub, fg=GUI.fg, height=1,
            width=4, relief=GROOVE, font=GUI.font, command=self.save_section)
        save_button.place(x=245, y=55+li, height=27, width=70)

        cancel_button = Button(labelframe, text="Cancel", bg=GUI.sub, fg=GUI.fg, height=1,
            width=4, relief=GROOVE, font=GUI.font, command=self.section_edit.destroy)
        cancel_button.place(x=320, y=55+li, height=27, width=70)

    def save_section(self):
        value_1 = self.entry1_edit.get()
        key = self.item_focus[0]
        type_ = self.item_focus[1]
        index = self.item_focus[2]
        if type_  == "single":
            type_key = "[S] "
            self.settings["sections_names"][key] = {
                    "type": "single",
                    "value_1": value_1,
            }
        if self.item_focus[1] == "dual":
            type_key = "[D] "
            value_2 = self.entry2_edit.get()
            self.settings["sections_names"][key] = {
                    "type": "dual",
                    "value_1": value_1,
                    "value_2": value_2
            }
        self.sl_listbox.delete(index)
        self.sl_listbox.insert(index, type_key + value_1)
        self.save_settings()
        messagebox.showinfo("Notice", "Item successfully saved.")
        self.section_edit.destroy()

    def add_sections(self):
        type_ = self.sl_drop.get()
        index = self.sl_listbox.size() + 1
        value_1 = self.sl_entry1.get()

        for key in self.settings["sections_names"]:
            if self.settings["sections_names"][key]["value_1"] == value_1:
                messagebox.showinfo("Warning", "Section name already exists. Please pick a different one.")
                return

        while True:
            key = self.id_generator()
            if key in self.settings["sections_names"]:
                continue
            else:
                break

        if not value_1:
            messagebox.showinfo("Warning", "Input at least one character length within the value entry.")
            return
        if type_ == "Single Named Section":
            type_key = "[S] "
            self.settings["sections_names"][key] = {
                    "type": "single",
                    "value_1": value_1,
            }
        if type_ == "Dual Named Section":
            type_key = "[D] "
            value_2 = self.sl_entry2.get()
            self.settings["sections_names"][key] = {
                    "type": "dual",
                    "value_1": value_1,
                    "value_2": value_2
            }
        print(self.settings)
        self.sl_listbox.insert(index, type_key + value_1)
        self.save_settings()

    def delete_section(self):
        

        try:
            index = self.sl_listbox.curselection()
            item = self.sl_listbox.get(index)
            if "[S]" in item:
                item = item.split("[S] ")[1]
            if "[D]" in item: 
                item = item.split("[D] ")[1]
        except:
            messagebox.showinfo("Warning", "Please choose a section from the list to delete.")
            return


        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            for key in self.settings["sections_names"]:
                if self.settings["sections_names"][key]["value_1"] == item:
                    self.settings["sections_names"].pop(key, None)
                    pprint(self.settings)
                    break
            self.sl_listbox.delete(index)
            self.save_settings()
            return
        else:
            print("I'm Not Deleted Yet")


    def warning_top(self):
        self.warning_top_win = Toplevel()
        self.warning_top_win.title("Deleting Section")
        self.warning_top_win.geometry("400x120+1200+100")
        self.warning_top_win["bg"] = GUI.bg
        self.warning_top_win.resizable(False, False)

        

        # self.warning_top_win.focus()
        label = Label(self.warning_top_win, text="Confirm section deletion? This is irreversible.", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        label.place(x=40, y=20)

        accept_button = Button(self.warning_top_win, text="Accept", width=10, relief=GROOVE, bg=GUI.rr, fg=GUI.fg,
            font=GUI.font)
        accept_button.place(x=100, y=60, height=27, width=70)
        cancel_button = Button(self.warning_top_win, text="Cancel", width=10, relief=GROOVE, bg=GUI.bg, fg=GUI.fg,
            font=GUI.font, command=self.warning_top_win.destroy)
        cancel_button.place(x=210, y=60, height=27, width=70)
        self.warning_top_win.focus()

    def open_Toplevel(self, mode):
        if mode == "section_list":
            if self.section_is_opened == True:
                self.section_list.lift()
            if self.section_is_opened == False:
                self.section_list_window()

    def close_Toplevel(self, mode):
        if mode == "section_list":
            self.section_is_opened = False
            self.section_list.destroy()

    def select_folder(self):
        if not self.settings["GrimoirePath"]:
            self.settings["GrimoirePath"] = filedialog.askdirectory(title='Please select Grimoire Bot Directory. You can change this later in the Settings.')
            self.save_settings()
        else:
            os.startfile(self.settings["GrimoirePath"])        


    def main_switch_skills(self):
        self.skills_listbox.delete(0,'end')
        if self.right_switch["text"] == "Default Skills":
            self.right_switch["text"] = "Custom Skills"
            self.class_mode_var.set("custom")
            self.skills_dropdown.set('')
            self.skills_dropdown["value"] = self.custom_skill_list
            try:
                self.skills_dropdown.current(0)
            except: pass
            return
        if self.right_switch["text"] == "Custom Skills":
            self.right_switch["text"] = "Default Skills"
            self.class_mode_var.set("default")
            self.skills_dropdown.set('')
            self.skills_dropdown["value"] = self.default_skill_list
            try:
                self.skills_dropdown.current(0)
            except: pass
            return

    # System File inserts
    def insert_skills(self, event):
        class_name = self.skills_dropdown.get()
        if class_name:
            self.skills_listbox.delete(0,'end')
            index = 0
            for items in self.default_skill_dict[class_name]:
                text = "Skill " + items["Skill"]
                self.skills_listbox.insert(index, text)
                index += 1

    def insert_files_dropdown(self):
        self.find_files()
        self.target_gbots_list = []
        for gbot in self.target_gbots_location:
            file = gbot.split("\\")[-1]
            self.target_gbots_list.append(file)
        self.top_dropdown["completevalues"] = self.target_gbots_list

    def insert_edit_section_list(self):
        ind = 0
        for item in self.settings["sections_names"]:
            type_ = self.settings["sections_names"][item]["type"]
            if type_ == "single":
                tag = "[S] "
            if type_ == "dual":
                tag = "[D] "
            self.sl_listbox.insert(ind, tag + self.settings["sections_names"][item]["value_1"])
            ind+=1

    def rClicker(self, e):
        ''' right click context menu for all Tk Entry and Text widgets
        '''

        try:
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')

            def rClick_Cut(e):
                e.widget.event_generate('<Control-x>')

            def rClick_Paste(e):
                e.widget.event_generate('<Control-v>')

            e.widget.focus()

            nclst=[
                   (' Cut', lambda e=e: rClick_Cut(e)),
                   (' Copy', lambda e=e: rClick_Copy(e)),
                   (' Paste', lambda e=e: rClick_Paste(e)),
                   ]

            rmenu = Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

        except TclError:
            pass

        return "break"


    def rClickbinder(self, r):
        try:
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-3>',
                             func=rClicker, add='')
        except TclError:
            pass

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

if __name__=="__main__":
    root = Tk()
    x = GUI(root)
    root.mainloop()