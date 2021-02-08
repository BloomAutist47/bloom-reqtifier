from tkinter import *
from tkinter import ttk, filedialog
from pprint import pprint
import os
import glob
import json
import re
import ctypes
 
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
        print(self.settings)
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
                print(self.t_in)
                self.t_in = []
                pprint(self.skill)
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
        self.master.geometry("800x450")
        # self.master.tk.call('tk', 'scaling', 4.0)
        self.master["bg"] = "White"
        self.class_mode_var = StringVar()

        self.grim_folder = ""

        # Reqtificator setups
        self.data_setup()
        self.retrieve_skills()

        # GUI setups
        self.menu_setup()
        self.widgets_setup()

        # Item insertions
        self.file_dropdown()
        # self.section_list()



    def menu_setup(self):
        # Menus
        self.menubar = Menu(self.master)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open File...")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.settings_menu = Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Section List", command=self.section_list)
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

        self.menubar.add_command(label="Refresh", command=self.file_dropdown)

        self.master.config(menu=self.menubar)

    def widgets_setup(self):
        # Frame at TOP
        self.top_frame = Frame(self.master, bg=GUI.rr, width=575, height=30)
        self.top_frame.place(x=8, y=15)

        self.top_label = Label(self.top_frame, text="Gbot:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.top_label.place(x=10, y=0)

        self.top_dropdown = ttk.Combobox(self.top_frame, values=[], width=51, font=GUI.font)
        self.top_dropdown.place(x=50, y=0, width=437)

        self.save_button = Button(self.top_frame, text="Save", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 11))
        self.save_button.place(x=489, y=0, height=24, width=78)
        
        
        # Frame at the LEFT
        self.left_frame = Frame(self.master, bg=GUI.rr, width=275, height=255)
        self.left_frame.place(x=10, y=40)
        self.left_label = Label(self.left_frame, text="Sections:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.left_label.place(x=10, y=10)

        self.left_dropdown = ttk.Combobox(self.left_frame, values=[], width=29, font=GUI.font)
        self.left_dropdown.place(x=10, y=30)

        self.left_listbox = Listbox(self.left_frame, bg=GUI.sub, fg=GUI.fg, bd=1,
            width=29, height=10, relief=GROOVE, font=GUI.font,
            activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        self.left_listbox.place(x=10, y=60)

        self.left_scroll = Scrollbar(self.left_frame)
        self.left_listbox.config(yscrollcommand=self.left_scroll.set)
        self.left_scroll.config(command=self.left_listbox.yview)
        self.left_scroll.place(x=247, y=60, height=194)


        # Frame at the RIGHT
        self.right_frame = Frame(self.master, bg=GUI.rr, width=275, height=255)
        self.right_frame.place(x=310, y=40)
        self.right_label = Label(self.right_frame, text="Class Skills:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.right_label.place(x=10, y=10)

        self.right_label2 = Label(self.right_frame, text="Using:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.right_label2.place(x=187, y=10)

        self.right_switch = Button(self.right_frame, text="Default Skills", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 10), command=self.switch)
        self.right_switch.place(x=187, y=30, height=24)

        self.skills_dropdown = ttk.Combobox(self.right_frame, values=self.default_skill_list, width=19, font=GUI.font)
        self.skills_dropdown.place(x=10, y=30)
        self.skills_dropdown.bind("<<ComboboxSelected>>", lambda x: self.insert_skills(x))

        self.skills_listbox = Listbox(self.right_frame, bg=GUI.sub, fg=GUI.fg, bd=1,
            width=29, height=10, relief=GROOVE, font=GUI.font,
            activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        self.skills_listbox.place(x=10, y=60)

        self.right_scroll = Scrollbar(self.right_frame)
        self.skills_listbox.config(yscrollcommand=self.right_scroll.set)
        self.right_scroll.config(command=self.skills_listbox.yview)
        self.right_scroll.place(x=247, y=60, height=194)


        # Frames at the bottom
        self.bottom_frame = Frame(self.master, bg=GUI.rr, width=575, height=40)
        self.bottom_frame.place(x=10, y=300)

        self.reset_section_button = Button(self.bottom_frame, text="Reset Section", bg=GUI.bg, fg=GUI.fg, relief=GROOVE, font=GUI.font)
        self.reset_section_button.place(x=80, width=100, height=25)
        self.set_section_button = Button(self.bottom_frame, text="Use Skills", bg=GUI.bg, fg=GUI.fg, relief=GROOVE, font=GUI.font)
        self.set_section_button.place(x=395, width=100, height=25)

    def section_list(self):
        self.section_list = Toplevel()
        self.section_list.title("Section List")
        self.section_list.geometry("300x500+800+100")
        self.section_list["bg"] = GUI.bg

        # Intruction frame
        self.sl_instructions_frame = LabelFrame(self.section_list, text="Instructions",
            bg=GUI.bg, fg=GUI.fg)
        self.sl_instructions_frame.place(x=10, y=10, width=280)
        self.sl_instruction_text = Label(self.sl_instructions_frame, padx=20,
            bg=GUI.bg, fg=GUI.fg, relief=FLAT, font=GUI.font, wraplength=280, justify=LEFT,
            text="The skill section names must be EXACTLY the same name as the "\
                 "ones inside the .gbot or else none of these will work. "\
                 "To remove section names, click on the item and click [ - ].")
        self.sl_instruction_text.pack(fill="both", expand="yes")

        # Button Frames
        self.sl_frame_2 = LabelFrame(self.section_list, text="Add/Remove Section Names",
            bg=GUI.rr, height=40)
        self.sl_frame_2.place(x=10, y=115, width=280, height=50)
        self.sl_entry = Entry(self.sl_frame_2, bg=GUI.sub, fg=GUI.fg, 
            width=25, relief=GROOVE, font=GUI.font)
        self.sl_entry.place(x=5, y=0)

        self.sl_add = Button(self.sl_frame_2, text="+", bg=GUI.sub, fg=GUI.fg, 
            width=2, relief=GROOVE, font=GUI.font)
        self.sl_add.place(x=215, y=0, height=24)

        self.sl_min = Button(self.sl_frame_2, text="-", bg=GUI.sub, fg=GUI.fg, 
            width=2, relief=GROOVE, font=GUI.font)
        self.sl_min.place(x=245, y=0, height=24)

        # List box Frame
        self.sl_frame_3 = LabelFrame(self.section_list, text="Section Lists",
            bg=GUI.rr, height=40)
        self.sl_frame_3.place(x=10, y=170, width=280, height=320)

        self.sl_listbox = Listbox(self.sl_frame_3, bg=GUI.sub, fg=GUI.fg, bd=2, 
            width=30, height=10, relief=GROOVE, font=GUI.font,
            activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        self.sl_listbox.place(x=5, y=5, height=290)

        self.sl_scroll = Scrollbar(self.sl_frame_3)
        self.sl_listbox.config(yscrollcommand=self.sl_scroll.set)
        self.sl_scroll.config(command=self.sl_listbox.yview)
        self.sl_scroll.place(x=250, y=5, width=20, height=290)

        # Function inis
        self.insert_section_names()

    def select_folder(self):
        if not self.settings["GrimoirePath"]:
            self.settings["GrimoirePath"] = filedialog.askdirectory(title='Please select Grimoire Bot Directory. You can change this later in the Settings.')
            self.save_settings()
        else:
            os.startfile(self.settings["GrimoirePath"])

    def switch(self):
        self.skills_listbox.delete(0,'end')
        if self.right_switch["text"] == "Default Skills":
            self.right_switch["text"] = "Custom Skills"
            self.class_mode_var.set("custom")
            self.skills_dropdown.set('')
            self.skills_dropdown["value"] = self.custom_skill_list
            return
        if self.right_switch["text"] == "Custom Skills":
            self.right_switch["text"] = "Default Skills"
            self.class_mode_var.set("default")
            self.skills_dropdown.set('')
            self.skills_dropdown["value"] = self.default_skill_list
            return

    def insert_skills(self, event):
        class_name = self.skills_dropdown.get()
        if class_name:
            self.skills_listbox.delete(0,'end')
            index = 0
            for items in self.default_skill_dict[class_name]:
                text = "Skill " + items["Skill"]
                self.skills_listbox.insert(index, text)
                index += 1

    def file_dropdown(self):
        self.find_files()
        self.target_gbots_list = []
        for gbot in self.target_gbots_location:
            file = gbot.split("\\")[-1]
            self.target_gbots_list.append(file)
        self.top_dropdown["value"] = self.target_gbots_list

    def insert_section_names(self):
        # try:
        if self.section_names:
            index = 0
            for section in self.section_names:
                self.sl_listbox.insert(index, section)
                index += 1
            return
        # except:
        #     print("Something's wrong with the section list")
        #     return


if __name__=="__main__":
    root = Tk()
    x = GUI(root)
    root.mainloop()