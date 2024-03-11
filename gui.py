import os
import customtkinter
import customtkinter as ctk
import pygame
from tkinter import font as tkFont, messagebox
import pyglet
import authentication

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
print("gui.py started")

ID_TOKEN = ''

class MessageApp(customtkinter.CTk):
    def __init__(self, q):
        super().__init__()
        # self.create_login_window()  # Call to create the login window
        self.create_main_window(q)

    def create_main_window(self, q):
        self.geometry(f"{1100}x{580}")
        self.title("Real-Time Message Display")
        self.queue = q
        self.after(100, self.check_queue)  # Set up an after loop to check the queue

        font_path = './font/Debrosee.ttf'
        font_name = 'Debrosee'  # The name by which the OS identifies the font
        self.load_custom_font(font_path)

        customFont = tkFont.Font(family=font_name, size=12)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Sidebar",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text='Dashboard',
                                                        command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Settings',
                                                        command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text='Audio',
                                                        command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create Status label
        self.message_label = ctk.CTkLabel(self, text="", fg_color='gray', text_color='black', corner_radius=10, pady=15,
                                          anchor='nw')
        self.message_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Add a Terminate Program button at the end of the sidebar
        self.terminate_program_button = customtkinter.CTkButton(self.sidebar_frame, text='Terminate Program',
                                                                command=lambda: self.terminate_program(''))
        self.terminate_program_button.grid(row=9, column=0, padx=20, pady=10)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_columnconfigure(1, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        # Create audio playing buttons (implement the audio logic into the command)
        self.seg_button_1 = customtkinter.CTkButton(self.slider_progressbar_frame, text='Audio 1', height=50,
                                                    command=lambda: self.sb_button('1', self.slider_2.get()))
        self.seg_button_2 = customtkinter.CTkButton(self.slider_progressbar_frame, text='Audio 2', height=50,
                                                    command=lambda: self.sb_button('2', self.slider_2.get()))
        self.seg_button_3 = customtkinter.CTkButton(self.slider_progressbar_frame, text='Audio 3', height=50,
                                                    command=lambda: self.sb_button('3', self.slider_2.get()))
        self.seg_button_4 = customtkinter.CTkButton(self.slider_progressbar_frame, text='Audio 4', height=50,
                                                    command=lambda: self.sb_button('4', self.slider_2.get()))
        self.seg_button_5 = customtkinter.CTkButton(self.slider_progressbar_frame, text='Audio 5', height=50,
                                                    command=lambda: self.sb_button('5', self.slider_2.get()))
        self.seg_button_6 = customtkinter.CTkButton(self.slider_progressbar_frame, text='Audio 6', height=50,
                                                    command=lambda: self.sb_button('6', self.slider_2.get()))
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 2.5), sticky="ew")
        self.seg_button_2.grid(row=0, column=1, padx=(20, 10), pady=(10, 2.5), sticky="ew")
        self.seg_button_3.grid(row=1, column=0, padx=(20, 10), pady=(10, 2.5), sticky="ew")
        self.seg_button_4.grid(row=1, column=1, padx=(20, 10), pady=(10, 2.5), sticky="ew")
        self.seg_button_5.grid(row=2, column=0, padx=(20, 10), pady=(10, 2.5), sticky="ew")
        self.seg_button_6.grid(row=2, column=1, padx=(20, 10), pady=(10, 2.5), sticky="ew")

        # Create volume slider
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=4, columnspan=2, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=2, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=3, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.seg_button_1.configure()


    def check_queue(self):
        if not self.queue.empty():
            message = self.queue.get()  # Get the next item from the queue
            self.update_message(message)  # Method to update the GUI with the new message
        self.after(100, self.check_queue)
    def load_custom_font(self, font_path):
        pyglet.font.add_file(font_path)
        return [pyglet.font.have_font('Font Name')]

    def playSound(self, num, volume):
        jukebox_dir = 'jukebox'
        song_name = str('audio' + num + '.wav')
        audio = os.path.join(jukebox_dir, song_name)
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(volume)  # Volume takes a value from 0.0 to 1.0
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()

        except Exception as e:
            print(f"Error playing {song_name}: {e}")

    def update_message(self, new_message):
        if new_message == "1" or new_message == "2" or new_message == "3" or new_message == "4" or new_message == "5" or new_message == "6":
            self.playSound(new_message, 3)
            new_message = 'Audio ' + new_message + " playing/ played"

        print(f"update message received: {new_message}")
        self.message_label.configure(text=new_message)

    def sb_button(self, msgVal, volume):
        self.update_message('Audio ' + msgVal +' playing/ played')
        self.playSound(msgVal, volume)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


def main(q):

    app = MessageApp(q)
    app.mainloop()
