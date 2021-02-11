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
import configparser

ctypes.windll.shcore.SetProcessDpiAwareness(2)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Gbots:

    def __init__(self, path):
        self.file_path = path
        self.bot_name = path.split("\\")[-1]
        self.command_list = []

        with open(path, "r", encoding='utf-8') as f:
            self.file_json = json.load(f)


    def get_commands(self):
        th = self.settings["Config.cfg"]
        comms = self.file_json["Commands"]["$values"]
        ItemNoColon = ["Is in combat", "Is not in combat", "Is Member", "Is Not Member"]
        index = 0
        for item in comms:
            
            cmd = item["$type"]

            while True:
                # Combat tab
                # Kill
                if "CmdKill" in cmd:
                    pack = (index, f"Kill {item['Monster']}", th['KillColor'])
                    break
                # Attack
                if "CmdAttack" in cmd:
                    pack = (index, f"Attack {item['Monster']}", th['AttackColor'])
                    break
                # Kill for Items
                if "CmdKillFor" in cmd:
                    pack = (index, f"Kill for items: {item['Monster']}", th['KillForColor'])
                    break
                # Kill for tempitems
                if "CmdKillFor" in cmd and "ItemType" in item:
                    pack = (index, f"Kill for tempitems: {item['Monster']}", th['KillForColor'])
                    break
                # Use Skill (cmd)
                if "CmdUseSkill" in cmd:
                    pack = (index, f"Skill {item['Skill']}", th['UseSkillColor'])
                    break
                # Add Skill (cmd)
                if "CmdSkillSet" in cmd:
                    pack = (index, f"Skill Set: {item['Name'].upper()}", th['SkillSetColor'])
                    break
                # Rest
                if "CmdRest" in cmd:
                    pack = (index, "Rest", th['RestColor'])
                    break
                # Rest fully
                if "CmdRest" in cmd and "Full" in item:
                    pack = (index, "Rest Fully", th['RestColor'])
                    break


                # Item tab
                # Get Drop
                if "Item.CmdGetDrop" in cmd:
                    pack = (index, f"Get drop: {item['ItemName']}", th['GetDropColor'])
                    break
                # Sell Drop
                if "Item.CmdSell" in cmd:
                    pack = (index, f"Sell: {item['ItemName']}", th['SellColor'])
                    break
                # Equip Drop
                if "Item.CmdEquip" in cmd:
                    pack = (index, f"Equip: {item['ItemName']}", th['EquipColor'])
                    break
                # To bank from inv
                if "Item.CmdBankTransfer" in cmd:
                    pack = (index, f"Inv -> Bank: {item['ItemName']}", th['BankTransferColor'])
                    break
                # To inv from bank
                if "Item.CmdBankTransfer" in cmd and "TransferFromBank" in item:
                    pack = (index, f"Bank -> Inv: {item['ItemName']}", th['BankTransferColor'])
                    break
                # Bank Swap
                if "Item.CmdBankSwap" in cmd:
                    pack = (index, f"Bank Swap {{{item['BankItemName']}, {item['InventoryItemName']}}}", th['BankSwapColor'])
                    break
                # Load Shop
                if "Item.CmdLoad" in cmd:
                    pack = (index, f"Load Shop: {item['ShopId']}", th['LoadBotColor'])
                    break
                # Buy item
                if "Item.CmdBuy" in cmd:
                    pack = (index, f"Buy item: {item['ItemName']}", th['BuyColor'])
                    break
                # Buy item fast
                if "Item.CmdBuyFast" in cmd:
                    pack = (index, f"Buy item fast: {item['ItemName']}", th['BuyFastColor'])
                    break
                # Get Map Item
                if "Item.CmdMapItem" in cmd:
                    pack = (index, f"Get map item: {item['ItemId']}", th['MapItemColor'])
                    break

                # Map tab
                # join Map
                if "Map.CmdJoin" in cmd:
                    pack = (index, f"Join: {item['Map']}, {item['Cell']}, {item['Pad']}", th['JoinColor'])
                    break
                # Jump
                if "Map.CmdMoveToCell" in cmd:
                    pack = (index, f"Mote to cell: {item['Cell']}, {item['Pad']}", th['MoveToCellColor'])
                    break
                # Yulgar?
                if "Map.CmdYulgar" in cmd:
                    pack = (index, "Join yulgar", th['YulgarColor'])
                    break
                # Set Spawnpoint
                if "Map.CmdSetSpawn" in cmd:
                    pack = (index, "Set Spawnpoint", th['SetSpawnColor'])
                    break
                # Walk to
                if "Map.CmdWalk" in cmd:
                    pack = (index, f"Walk to: {item['X']}, {item['Y']}", th['WalkColor'])
                # Walk Randomly
                if "Map.CmdWalk" in cmd and "Type" in item:
                    pack = (index, "Walk Randomly", th['WalkColor'])
                    break
                # # Walk Randomly
                # if "Map.CmdSetSpawn" in cmd and "Type" in item:
                #     pack = (index, "Set Spawnpoint", th['SetSpawnColor'])
                #     break

                # Quest tab
                # Complete command
                if "Quest.CmdCompleteQuest" in cmd and "ItemId" not in item['Quest']:
                    pack = (index, f"Complete quest: {item['Quest']['QuestID']}", th['CompleteQuestColor'])
                    break
                # Complete command with Item ID
                if "Quest.CmdCompleteQuest" in cmd and "ItemId" in item['Quest']:
                    pack = (index, f"Complete quest: {item['Quest']['QuestID']}:{item['Quest']['ItemId']}", th['CompleteQuestColor'])
                    break
                # Accept command
                if "Quest.CmdAcceptQuest" in cmd:
                    pack = (index, f"Accept quest: {item['Quest']['QuestID']}", th['CompleteQuestColor'])
                    break

                # Misc Tabs
                # Item Statements
                if "Misc.Statements" in cmd and "Item" in item["Tag"] and item['Value2'] != "":
                    pack = (index, f"{item['Text']}: {item['Value1']}, {item['Value2']}", th['CompleteQuestColor'])
                    break
                if "Misc.Statements" in cmd and "Item" in item["Tag"] and item['Value2'] == "":
                    pack = (index, f"{item['Text']}: {item['Value1']}", th['CompleteQuestColor'])
                    break
                if "Misc.Statements" in cmd and "Item" in item["Tag"] and item['Value1'] == "" and item['Value2'] == "":
                    pack = (index, f"{item['Text']}", th['CompleteQuestColor'])
                    break

                # This Player Statements
                if "Misc.Statements" in cmd and "This player" in item["Tag"] and item['Value2'] != "":
                    pack = (index, f"{item['Text']}: {item['Value1']}, {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "This player" in item["Tag"] and item['Value2'] == "":
                    pack = (index, f"{item['Text']}: {item['Value1']}")
                    break
                if "Misc.Statements" in cmd and "This player" in item["Tag"] and item['Value1'] == "" and item['Value2'] == "":
                    pack = (index, f"{item['Text']}")
                    break

                # Player Statements
                if "Misc.Statements" in cmd and "Player" in item["Tag"] and item['Value2'] != "":
                    pack = (index, f"{item['Text']}: {item['Value1']}, {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Player" in item["Tag"] and item['Value2'] == "":
                    pack = (index, f"{item['Text']}: {item['Value1']}")
                    break
                if "Misc.Statements" in cmd and "Player" in item["Tag"] and item['Value1'] == "" and item['Value2'] == "":
                    pack = (index, f"{item['Text']}")
                    break

                # Map Statements
                if "Misc.Statements" in cmd and "Map" in item["Tag"] and item['Value2'] != "":
                    pack = (index, f"{item['Text']}: {item['Value1']}, {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Map" in item["Tag"] and item['Value2'] == "":
                    pack = (index, f"{item['Text']}: {item['Value1']}")
                    break
                if "Misc.Statements" in cmd and "Map" in item["Tag"] and item['Value1'] == "" and item['Value2'] == "":
                    pack = (index, f"{item['Text']}")
                    break

                # Monster Statements
                if "Misc.Statements" in cmd and "Monster" in item["Tag"] and item['Value2'] != "":
                    pack = (index, f"{item['Text']}: {item['Value1']}, {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Monster" in item["Tag"] and item['Value2'] == "":
                    pack = (index, f"{item['Text']}: {item['Value1']}")
                    break
                if "Misc.Statements" in cmd and "Monster" in item["Tag"] and item['Value1'] == "" and item['Value2'] == "":
                    pack = (index, f"{item['Text']}")
                    break

                # Quest Statements
                if "Misc.Statements" in cmd and "Quest" in item["Tag"] and item['Value2'] != "":
                    pack = (index, f"{item['Text']}: {item['Value1']}, {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Quest" in item["Tag"] and item['Value2'] == "":
                    pack = (index, f"{item['Text']}: {item['Value1']}")
                    break
                if "Misc.Statements" in cmd and "Quest" in item["Tag"] and item['Value1'] == "" and item['Value2'] == "":
                    pack = (index, f"{item['Text']}")
                    break

                # Misc Statements
                if "Misc.Statements" in cmd and "Misc" in item["Tag"] and item['Text'] == "Int Greater Than":
                    pack = (index, f"Int > {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Misc" in item["Tag"] and item['Text'] == "Int Lesser Than":
                    pack = (index, f"Int < {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Misc" in item["Tag"] and item['Text'] == "Int is":
                    pack = (index, f"Int == {item['Value2']}")
                    break
                if "Misc.Statements" in cmd and "Misc" in item["Tag"] and item['Text'] == "Int is not":
                    pack = (index, f"Int != {item['Value2']}")
                    break

                # Set Bot Delay
                if "Misc.CmdBotDelay" in cmd:
                    pack = (index, f"Set bot delay: {item['Delay']}")
                    break
                # Set Delay
                if "Misc.CmdDelay" in cmd:
                    pack = (index, f"Delay: {item['Delay']}")
                    break
                # Set Int 0
                if "Misc.CmdInt" in cmd and "Value" not in item:
                    pack = (index, f"Set {item['Int']}: 0")
                    break
                # Set Int to Value
                if "Misc.CmdInt" in cmd and "type" not in item:
                    pack = (index, f"Set {item['Int']}: {item['Value']}")
                    break
                # Set Int Increase
                if "Misc.CmdInt" in cmd and item["type"] == 1:
                    pack = (index, f"Increase {item['Int']} by 1")
                    break
                # Set Int Decrease
                if "Misc.CmdInt" in cmd and item["type"] == 2:
                    pack = (index, f"Decrease {item['Int']} by 1")
                    break
                # Send Packet
                if "Misc.CmdPacket" in cmd and "Client" not in item:
                    pack = (index, f"Send packet: {item['Packet']}")
                    break
                # Send Client Packet
                if "Misc.CmdPacket" in cmd and "Client" in item:
                    pack = (index, f"Send client packet: {item['Packet']}")
                    break
                # Load Bot Command
                if "Misc.CmdLoadBot" in cmd:
                    pack = (index, f"Load bot: {item['BotFileName']}")
                    break
                # Goto Player Command
                if "Misc.CmdGotoPlayer" in cmd:
                    pack = (index, f"Goto player: {item['PlayerName']}")
                    break
                # Command Blank
                if "Misc.CmdBlank2" in cmd and item["Text"] == " ":
                    pack = (index, "", "blank_ind")
                    break
                # Command Blank with Text
                if "Misc.CmdBlank2" in cmd and item["Text"] != " ":
                    data = re.match("\[.+\]", item["Text"])
                    if data:
                        data = re.split("(\[.+\])", item["Text"]) 
                        cr = data[1].replace("[", "").replace("]", "").replace(" ", "").split(",")
                        color = (int(cr[0]), int(cr[1]), int(cr[2]),)
                        text = data[2]
                        pack = (index, text, "blank_ind", color)
                        # print(f"{item['Text']}: {pack}")
                        break
                    pack = (index, item["Text"], "blank_ind")
                    break

                   
                # Play Sound
                if "Misc.CmdBeep" in cmd:
                    pack = (index, f"Beep {item['Times']} Times")
                    break
                # Toggle Provoke Off
                if "Misc.CmdToggleProvoke" in cmd and "Type" not in item:
                    pack = (index, "Provoke Off")
                    break
                # Toggle Provoke On
                if "Misc.CmdToggleProvoke" in cmd and item["Type"] == 1:
                    pack = (index, "Provoke On")
                    break
                # Toggle Provoke
                if "Misc.CmdToggleProvoke" in cmd and item["Type"] == 2:
                    pack = (index, "Provoke Toggle")
                    break
                # Stop Bot
                if "Misc.CmdStop" in cmd:
                    pack = (index, "Stop Bot")
                    break
                # Restart bot
                if "Misc.CmdRestart" in cmd:
                    pack = (index, "Restart bot")
                    break
                # Logout
                if "Misc.CmdLogout" in cmd:
                    pack = (index, "Logout")
                    break
               # Goto
                if "Misc.CmdGotoLabel" in cmd:
                    pack = (index, f"Goto Label: {item['Label']}")
                    break
               # Add
                if "Misc.CmdLabel" in cmd:
                    pack = (index, f"[{item['Name'].upper()}]", "blank_ind")
                    break

               # Goto Index 0
                if "Type" in item:
                    if "Misc.CmdIndex" in cmd and item["Type"] == 2 and "Index" not in item:
                        pack = (index, "Goto index: 0")
                        break 
                   # Goto Index n
                    if "Misc.CmdIndex" in cmd and item["Type"] == 2 and "Index" in item:
                        pack = (index, f"Goto index: {item['Index']}")
                        break

                   # Index down 0
                    if "Misc.CmdIndex" in cmd and item["Type"] == 1 and "Index" not in item:
                        pack = (index, f"Index down: 0")
                        break
                   # Index down n
                    if "Misc.CmdIndex" in cmd and item["Type"] == 1 and "Index" in item:
                        pack = (index, f"Index down: {item['Index']}")
                        break

               # Index up 0
                if "Misc.CmdIndex" in cmd and "Type" not in item and "Index" not in item:
                    pack = (index, f"Index up: 0")
                    break
               # Index up n
                if "Misc.CmdIndex" in cmd and "Type" not in item and "Index" in item:
                    pack = (index, f"Index up: {item['Index']}")
                    break

                # Options Tab
                # Log Debug
                if "Misc.CmdLog" in cmd and "Debug" in item:
                    pack = (index, f"Log Debug: {item['Text']}")
                    break
                # log Script
                if "Misc.CmdLog" in cmd and "Debug" not in item:
                    pack = (index, f"Log Script: {item['Text']}")
                    break

                # Client Tab
                # Log Debug
                if "Misc.CmdChange" in cmd:
                    pack = (index, f"Name: {item['Text']}")
                    break
                # Log Debug
                if "Misc.CmdChange" in cmd and "Guild" in item:
                    pack = (index, f"Guild: {item['Text']}")
                    break
                pack=(index, "")
                break

            self.command_list.append(pack)
            index += 1


class Reqtificator:

    def data_setup(self):
        self.section_tags = ["- skill section -", "- skill section2 -"]
        self.default_skill_dict = {}
        self.custom_skill_dict = {}

        self.default_skill_list = []
        self.custom_skill_list = []

        self.gbot_lists = {}

        self.settings = {}
        self.section_names = []

        self.find_files()
        self.retrieve_skills()
        self.retrieve_settings()

    def find_files(self):
        self.default_skills_location = glob.glob("./Skills/Default Skills/req_*.gbot")
        self.custom_skills_location = glob.glob("./Skills/Custom Skills/req_*.gbot")
        self.target_gbots_location = glob.glob("./Bots/*.gbot")

        for gbot in self.target_gbots_location:
            name = gbot.split("\\")[-1]
            self.gbot_lists[name] = Gbots(gbot)
    
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
    def config_read(self):
        if "Config.cfg" in self.settings:
            if self.settings["Config.cfg"] != {}:
                return
        if "Config.cfg" not in self.settings:
            self.theme_config = {}
            with open("./config.cfg", "r") as f:
                raw_theme = f.read()
            for i in raw_theme.split("\n"):
                item = i.split("=")
                self.theme_config[item[0]] = item[1]
            pprint(self.theme_config)
            self.settings["Config.cfg"] = self.theme_config
            self.save_settings()


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
        self.master.geometry("800x600+50+100")
        self.master.resizable(False, True)
        self.master.title("Pro Reqtifier")
        self.master["bg"] = "White"
        self.class_mode_var = StringVar()

        # Variables
        self.grim_folder = ""
        self.item_focus = ""

        # Reqtificator setups
        self.data_setup()
        self.retrieve_skills()
        self.config_read()

        # GUI setups
        self.widget_style()
        self.menu_setup()
        self.widgets_setup()

        # Item insertions
        self.section_list_window()
        

    def widget_style(self):
        style = ttk.Style()
        # # this is set background and foreground of the treeview
        style.configure("Treeview",
                        background="#44444",
                        foreground="#000000",
                        rowheight=17,
                        fieldbackground="#E1E1E1",
                        font=(GUI.fs, 9))

        # # set backgound and foreground color when selected
        style.map('Treeview', background=[('selected', '#BFBFBF')], foreground=[('selected', 'black')])

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
        self.directory.add_command(label="Lab Bots Folder", command=lambda: self.open_folder("./Bots"))
        self.directory.add_command(label="Results Folder", command=lambda: self.open_folder("./Results"))
        self.directory.add_command(label="Default Skills Folder", command=lambda: self.open_folder("./Skills/Default Skills"))
        self.directory.add_command(label="Custom Skills Folder", command=lambda: self.open_folder("./Skills/Custom Skills"))
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

        self.top_dropdown = AutocompleteCombobox(self.top_frame, font=GUI.font, completevalues=list(self.gbot_lists.keys()))
        self.top_dropdown.bind('<Button-3>',self.rClicker, add='')
        self.top_dropdown.place(x=55, y=2, width=445, height=25)
        self.top_dropdown.bind("<<ComboboxSelected>>", lambda x: self.dropdown_focus())
        self.top_dropdown.bind("<<ComboboxSelected>>", lambda x: self.insert_commands())

        self.save_button = Button(self.top_frame, text="Save", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 11))
        self.save_button.place(x=502, y=1, height=27, width=70)

        self.load_button = Button(self.top_frame, text="Load", bg=GUI.bg, fg=GUI.fg,
            relief=GROOVE, font=(GUI.fs, 11))
        self.load_button.place(x=575, y=1, height=27, width=70)

        # Frame at the LEFT
        self.left_frame = Frame(self.master, bg=GUI.rr, width=550, height=400)
        self.left_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky=W+N+S)
        self.left_frame.rowconfigure(2, weight=1)

        self.left_label = Label(self.left_frame, text="Sections:", bg=GUI.bg, fg=GUI.fg, font=GUI.font)
        self.left_label.grid(row=0, column=0,  pady=1, sticky=W+N)

        # self.left_dropdown = ttk.Combobox(self.left_frame, values=[], width=29, font=GUI.font)
        # self.left_dropdown.grid(row=1, column=0, columnspan=10, padx=(1), pady=1, sticky=N)

        self.left_dropdown = AutocompleteCombobox(self.left_frame, font=GUI.font, width=19, completevalues=["All Commands"])
        self.left_dropdown.current(0)
        self.left_dropdown.bind('<Button-3>',self.rClicker, add='')
        self.left_dropdown.grid(row=1, column=0, columnspan=10, padx=(1), pady=1, sticky=W+E+N)


        # self.left_listbox = Listbox(self.left_frame, bg=GUI.sub, fg=GUI.fg, bd=1,
        #     width=35, height=10, relief=GROOVE, font=(GUI.fs, 9),
        #     activestyle="none", highlightthickness=0, selectbackground=GUI.select_bg)
        # self.left_listbox.grid(row=2, column=0, columnspan=9, padx=1, pady=1, sticky=S+N)


        self.left_listbox = ttk.Treeview(self.left_frame, selectmode='browse', columns=("1", "2")) 
        self.left_listbox['show'] = 'headings'

        self.left_listbox.column("1", width=50, anchor ='w') 
        self.left_listbox.heading("1", text="n")

        self.left_listbox.column("2", width=320, anchor ='w') 
        self.left_listbox.heading("2", text="Commands")
        

        self.left_listbox.grid(row=2, column=0, columnspan=9, padx=1, pady=1, sticky=S+N)
        

        self.left_scroll = Scrollbar(self.left_frame)
        self.left_listbox.config(yscrollcommand=self.left_scroll.set)
        self.left_scroll.config(command=self.left_listbox.yview)
        self.left_scroll.grid(row=2, column=9, padx=(1), pady=1, sticky=S+N)

        self.left_scroll_hor = Scrollbar(self.left_frame, orient="horizontal")
        self.left_listbox.config(xscrollcommand=self.left_scroll_hor.set)
        self.left_scroll_hor.config(command=self.left_listbox.xview)
        self.left_scroll_hor.grid(row=3, column=0, columnspan=9, sticky=E+W)

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
        self.section_edit.attributes('-topmost', True)
        self.section_edit.grab_set()

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


    def open_folder(self, dir_):
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        os.startfile(os.path.realpath(dir_))

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
    def insert_commands(self):
        item = self.top_dropdown.get()
        target = self.gbot_lists[item]
        target.get_commands()
        self.left_listbox.delete(*self.left_listbox.get_children())
        for i in target.command_list:
            if "blank_ind" in i:
                text = f"{i[1]}"
                ind = ""
            else:
                text = f"{i[1]}"
                ind = f"[{i[0]}]"

            if len(i) == 4:
                lin = "#%02x%02x%02x"%i[3]
                self.left_listbox.insert("", 'end', text=i[0], values=(ind, text, ), tag=(str(i[0]))) 
                self.left_listbox.tag_configure(str(i[0]), foreground=lin, font=('Calibri', 10,'bold'))
            else:
                self.left_listbox.insert("", 'end', text=i[0], values=(ind, text, ) ) 



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
        self.target_gbots_location = glob.glob("./Bots/*.gbot")
        pprint(self.target_gbots_location)
        self.gbot_lists = {}
        for gbot in self.target_gbots_location:
            name = gbot.split("\\")[-1]
            self.gbot_lists[name] = Gbots(gbot)
        self.top_dropdown["completevalues"]=list(self.gbot_lists.keys())
        return

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