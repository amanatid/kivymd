"""
Dialog
======

Copyright (c) 2015 Andrés Rodríguez and KivyMD contributors -
    KivyMD library up to version 0.1.2
Copyright (c) 2019 Ivanov Yuri and KivyMD contributors -
    KivyMD library version 0.1.3 and higher

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

`Material Design spec, Dialogs <https://material.io/design/components/dialogs.html>`_

Example
-------

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.utils import get_hex_from_color

from kivymd.uix.dialog import MDInputDialog, MDDialog
from kivymd.theming import ThemeManager


Builder.load_string('''
<ExampleDialogs@BoxLayout>
    orientation: 'vertical'
    spacing: dp(5)

    MDToolbar:
        id: toolbar
        title: app.title
        left_action_items: [['menu', lambda x: None]]
        elevation: 10
        md_bg_color: app.theme_cls.primary_color

    FloatLayout:
        MDRectangleFlatButton:
            text: "Open input dialog"
            pos_hint: {'center_x': .5, 'center_y': .7}
            opposite_colors: True
            on_release: app.show_example_input_dialog()

        MDRectangleFlatButton:
            text: "Open Ok Cancel dialog"
            pos_hint: {'center_x': .5, 'center_y': .5}
            opposite_colors: True
            on_release: app.show_example_okcancel_dialog()
''')


class Example(MDApp):
    title = "Dialogs"

    def build(self):
        return Factory.ExampleDialogs()

    def callback_for_menu_items(self, *args):
        from kivymd.toast.kivytoast import toast
        toast(args[0])

    def show_example_input_dialog(self):
        dialog = MDInputDialog(
            title='Title', hint_text='Hint text', size_hint=(.8, .4),
            text_button_ok='Yes',
            events_callback=self.callback_for_menu_items)
        dialog.open()

    def show_example_okcancel_dialog(self):
        dialog = MDDialog(
            title='Title', size_hint=(.8, .3), text_button_ok='Yes',
            text="Your [color=%s][b]text[/b][/color] dialog" % get_hex_from_color(
                self.theme_cls.primary_color),
            text_button_cancel='Cancel',
            events_callback=self.callback_for_menu_items)
        dialog.open()


Example().run()
"""

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDTextButton
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.theming import ThemableBehavior
from kivymd import images_path
from kivymd.material_resources import DEVICE_IOS


from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from supabase import create_client, Client
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior

import smtplib, ssl

Builder.load_string(
    """
#:import images_path kivymd.images_path


<ContentInputDialog>
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(10)

    MDLabel:
        font_style: 'H6'
        text: root.title
        halign: 'left' if not root.device_ios else 'center'

    BoxLayout:
        id: box_input
        size_hint: 1, None

    Widget:
    Widget:

    MDSeparator:
        id: sep

    BoxLayout:
        id: box_buttons
        size_hint_y: None
        height: dp(20)
        padding: dp(20), 0, dp(20), 0

#:import webbrowser webbrowser
#:import parse urllib.parse
<ThinLabel@MDLabel>:
    size_hint: 1, None
    valign: 'middle'
    height: self.texture_size[1]

<ThinLabelButton@ThinLabel+MDTextButton>:
    size_hint_y: None
    valign: 'middle'
    height: self.texture_size[1]

<ThinBox@BoxLayout>:
    size_hint_y: None
    height: self.minimum_height
    padding: dp(0), dp(0), dp(10), dp(0)


<ListMDDialog>
    title: ""
    BoxLayout:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(10)
    
        MDLabel:
            id: title
            text: root.title
            font_style: 'H6'
            halign: 'left' if not root.device_ios else 'center'
            valign: 'top'
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
    
        ScrollView:
            id: scroll
            size_hint_y: None
            height:
                root.height - (title.height + dp(48)\
                + sep.height)
    
            canvas:
                Rectangle:
                    pos: self.pos
                    size: self.size
                    #source: '{}dialog_in_fade.png'.format(images_path)
                    source: '{}transparent.png'.format(images_path)
    
            MDList:
                id: list_layout
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(15)
                canvas.before:
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: [1,0,0,.5]   
                ThinBox:
                    ThinLabel:
                        text: "Τίτλος(Title): "
                    ThinLabel:
                        id: room
                        text: root.Title  
                        
                        
                ThinBox:
                    ThinLabel:
                        text: "Status: "
                    ThinLabel:
                        text: root.Status             
                        
                ThinBox:
                    ThinLabel:
                        text: "'Ονομα(Name): "
                    ThinLabel:
                        text: root.Name 
                        
                ThinBox:
                    ThinLabel:
                        text: "Επίθετο(LastName): "
                    ThinLabel:
                        text: root.Lastname      
                        
                                                  
                        
                ThinBox:
                    ThinLabel:
                        text: "Διεύθυνση(Address): "
                    ThinLabelButton:
                        text: root.Address
                        
                        
                ThinBox:
                    ThinLabel:
                        text: "Τήλ(Phone Num).: "
                    ThinLabel:
                        text: root.Phonenumber   
                        
                
                ThinBox:
                    ThinLabel:
                        text: "Τιμή(€):"
                    ThinLabelButton:
                        text: str(root.Price)
                
                                
                ThinBox:
                    id : thinbox1
                    ThinLabel:
                        id: thinlabel1
                        text: "Website 1: "
                    ThinLabelButton:
                        id: thinlabelbutton1
                        text: root.Website1
                        on_release:
                            root.on_button() #webbrowser.open(self.text)
                            
                ThinBox:
                    id : thinbox2
                    ThinLabel:
                        id : thinlabel2
                        text: "Website 2: "
                    ThinLabelButton:
                        id: thinlabelbutton2 
                        text: root.Website2
                        on_release:
                            webbrowser.open(self.text)            
                
                            
                 
                        
               
        MDSeparator:
            id: sep


<ContentMDDialog>
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(10)

    text_button_ok: ''
    text_button_cancel: ''

    MDLabel:
        id: title
        text: root.title
        font_style: 'H6'
        halign: 'left' if not root.device_ios else 'center'
        valign: 'top'
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]

    ScrollView:
        id: scroll
        size_hint_y: None
        height:
            root.height - (box_buttons.height + title.height + dp(48)\
            + sep.height)

        canvas:
            Rectangle:
                pos: self.pos
                size: self.size
                #source: f'{images_path}dialog_in_fade.png'
                source: f'{images_path}transparent.png'

        MDLabel:
            text: '\\n' + root.text + '\\n'
            size_hint_y: None
            height: self.texture_size[1]
            valign: 'top'
            halign: 'left' if not root.device_ios else 'center'
            markup: True

    MDSeparator:
        id: sep

    BoxLayout:
        id: box_buttons
        size_hint_y: None
        height: dp(20)
        padding: dp(20), 0, dp(20), 0

        
<ImageButton@ButtonBehavior+AsyncImage>:
    allow_stretch: False
    keep_ratio: False        

<ContentMDDialog_Photos@Screen>
    orientation: 'vertical'
    padding: dp(5)
    spacing: dp(5)

    #text_button_ok: ''
    #text_button_cancel: ''
    #MDLabel:
    #    text:'hi'
   # Image:
   #     source:"1.jpg"  


    ScreenManager:
        id: scrn_mngr
        Screen:
            name: 'screen_one'
            BoxLayout:
                #orientation:'vertical'
                #AsyncImage:
                #    id:test
                #    source:''
                ImageButton:
                    id: screen_one
                    source: '' 
                    on_press:
                        # You can define the duration of the change
                        # and the direction of the slide
                        root.ids.scrn_mngr.current ='screen_two'
	

	    Screen:
            name: 'screen_two' 
            BoxLayout:
                ImageButton:
                    id: screen_two
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_three'
	
                        
   
       
        Screen:
            name: 'screen_three' 
            BoxLayout:
                ImageButton:
                    id: screen_three
                    source:'' 
                    on_press:
                        root.ids.scrn_mngr.current ='screen_four' 
                        
                                
        Screen:
            name: 'screen_four' 
            BoxLayout:
                ImageButton:
                    id: screen_four
                    source: ''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_five' 
                        
        
        Screen:
            name: 'screen_five' 
            BoxLayout:
                ImageButton:
                    id: screen_five
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_six'                           
    
        
        Screen:
            name: 'screen_six' 
            BoxLayout:
                ImageButton:
                    id: screen_six
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_seven'                           
    
        
        Screen:
            name: 'screen_seven' 
            BoxLayout:
                ImageButton:
                    id: screen_seven
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_eight'                           
    
    
        Screen:
            name: 'screen_eight' 
            BoxLayout:
                ImageButton:
                    id: screen_eight
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_nine'                           
    
        Screen:
            name: 'screen_nine' 
            BoxLayout:
                ImageButton:
                    id: screen_nine
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_ten'                           
    
        Screen:
            name: 'screen_ten' 
            BoxLayout:
                ImageButton:
                    id: screen_ten
                    source:''
                    on_press:
                        root.ids.scrn_mngr.current ='screen_one'                           
    

    BoxLayout:
        id: box_buttons
        size_hint_y: None
        height: dp(20)
        padding: dp(20), 0, dp(20), 0
   


<ContentMDDialog_Password>
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(10)

    text_button_ok: ''
    text_button_cancel: ''
    text_button_password: ''
    

    MDLabel:
        id: title
        text: root.title
        font_style: 'H6'
        halign: 'left' if not root.device_ios else 'center'
        valign: 'top'
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]

    GridLayout:
        cols: 2
        padding:dp(5)
        spacing: dp(10)
        adaptive_height: True 
       
        
        MDTextFieldRound:
            id:emailinput
            hint_text: 'Your Email'
            padding:dp(10),dp(10)
            size_hint:0.2,None
            height:dp(16)
            font_size:dp(25)
            #halign: 'right'
            #pos_hint: {"center_x":0.0, "center_y":1}  
            
    
    MDSeparator:
        id: sep   
         
    BoxLayout:
        id: box_buttons
        size_hint_y: None
        height: dp(20)
        padding: dp(20), 0, dp(20), 0

        
"""
)

if DEVICE_IOS:
    Heir = BoxLayout
else:
    Heir = MDCard


# FIXME: Not work themes for iOS.
class BaseDialog(ThemableBehavior, ModalView):
    def set_content(self, instance_content_dialog):
        def _events_callback(result_press):
            self.dismiss()
            if result_press and self.events_callback:
                self.events_callback(result_press, self)

        if self.device_ios:  # create buttons for iOS
            self.background = self._background

            if isinstance(instance_content_dialog, ContentInputDialog):
                self.text_field = MDTextFieldRect(
                    pos_hint={"center_x": 0.5},
                    size_hint=(1, None),
                    multiline=False,
                    height=dp(33),
                    cursor_color=self.theme_cls.primary_color,
                    hint_text=instance_content_dialog.hint_text,
                )
                instance_content_dialog.ids.box_input.height = dp(33)
                instance_content_dialog.ids.box_input.add_widget(
                    self.text_field
                )

            if self.text_button_cancel != "":
                anchor = "left"
            else:
                anchor = "center"
            box_button_ok = AnchorLayout(anchor_x=anchor)
            box_button_ok.add_widget(
                MDTextButton(
                    text=self.text_button_ok,
                    font_size="18sp",
                    on_release=lambda x: _events_callback(self.text_button_ok),
                )
            )
            instance_content_dialog.ids.box_buttons.add_widget(box_button_ok)

            if self.text_button_cancel != "":
                box_button_ok.anchor_x = "left"
                box_button_cancel = AnchorLayout(anchor_x="right")
                box_button_cancel.add_widget(
                    MDTextButton(
                        text=self.text_button_cancel,
                        font_size="18sp",
                        on_release=lambda x: _events_callback(
                            self.text_button_cancel
                        ),
                    )
                )
                instance_content_dialog.ids.box_buttons.add_widget(
                    box_button_cancel
                )

        else:  # create buttons for Android
            if isinstance(instance_content_dialog, ContentInputDialog):
                self.text_field = MDTextField(
                    size_hint=(1, None),
                    height=dp(48),
                    hint_text=instance_content_dialog.hint_text,
                )
                instance_content_dialog.ids.box_input.height = dp(48)
                instance_content_dialog.ids.box_input.add_widget(
                    self.text_field
                )
                instance_content_dialog.ids.box_buttons.remove_widget(
                    instance_content_dialog.ids.sep
                )

            box_buttons = AnchorLayout(
                anchor_x="right", size_hint_y=None, height=dp(30)
            )
            box = BoxLayout(size_hint_x=None, spacing=dp(5))
            box.bind(minimum_width=box.setter("width"))
            button_ok = MDRaisedButton(
                text=self.text_button_ok,
                on_release=lambda x: _events_callback(self.text_button_ok),
            )
            box.add_widget(button_ok)

            if self.text_button_cancel != "":
                button_cancel = MDFlatButton(
                    text=self.text_button_cancel,
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: _events_callback(
                        self.text_button_cancel
                    ),
                )
                box.add_widget(button_cancel)

            box_buttons.add_widget(box)
            instance_content_dialog.ids.box_buttons.add_widget(box_buttons)
            instance_content_dialog.ids.box_buttons.height = button_ok.height
            instance_content_dialog.remove_widget(
                instance_content_dialog.ids.sep
            )

class ListMDDialog(BaseDialog):
    Title = StringProperty("Missing data")
    RentType = StringProperty("Missing data")
    Name = StringProperty("Missing data")
    Lastname = StringProperty("Missing data")
    Address = StringProperty("Missing data")
    Phonenumber = StringProperty("Missing data")
    Price = NumericProperty("0")
    Website1 = StringProperty("Missing data")
    Website2 = StringProperty("Missing data")
    Status= StringProperty("Status")

    background = StringProperty('{}ios_bg_mod.png'.format(images_path))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def on_button(self):
        self.dialog = MDDialog_Photos( self.Title)
        self.dialog.open()
        pass




class BaseDialogMDInputDialog(ThemableBehavior, ModalView):
    def set_content(self, instance_content_dialog):
        def _events_callback(result_press):
            self.dismiss()
            if result_press and self.events_callback:
                self.events_callback(result_press, self)

        if self.device_ios:  # create buttons for iOS
            self.background = self._background

            if isinstance(instance_content_dialog, ContentInputDialog):
                self.text_field = MDTextFieldRect(
                    pos_hint={"center_x": 0.5},
                    size_hint=(1, None),
                    multiline=False,
                    height=dp(33),
                    cursor_color=self.theme_cls.primary_color,
                    hint_text=instance_content_dialog.hint_text,
                )
                instance_content_dialog.ids.box_input.height = dp(33)
                instance_content_dialog.ids.box_input.add_widget(
                    self.text_field
                )

            if self.text_button_cancel != "":
                anchor = "left"
            else:
                anchor = "center"
            box_button_ok = AnchorLayout(anchor_x=anchor)
            box_button_ok.add_widget(
                MDTextButton(
                    text=self.text_button_ok,
                    font_size="18sp",
                    on_release=lambda x: _events_callback(self.text_button_ok),
                )
            )
            instance_content_dialog.ids.box_buttons.add_widget(box_button_ok)

            if self.text_button_cancel != "":
                box_button_ok.anchor_x = "left"
                box_button_cancel = AnchorLayout(anchor_x="right")
                box_button_cancel.add_widget(
                    MDTextButton(
                        text=self.text_button_cancel,
                        font_size="18sp",
                        on_release=lambda x: _events_callback(
                            self.text_button_cancel
                        ),
                    )
                )
                instance_content_dialog.ids.box_buttons.add_widget(
                    box_button_cancel
                )

        else:  # create buttons for Android

            if isinstance(instance_content_dialog, ContentInputDialog):
                self.text_field = MDTextFieldRect(
                    #hint_text=None,
                    #helper_text_mode='on_focus',
                    size_hint=(1, None),
                    height=dp(48),
                    hint_text=instance_content_dialog.hint_text,
                )


                instance_content_dialog.ids.box_input.height = dp(48)
                instance_content_dialog.ids.box_input.add_widget(
                    self.text_field
                )



                instance_content_dialog.ids.box_buttons.remove_widget(
                    instance_content_dialog.ids.sep
                )

            box_buttons = AnchorLayout(
                anchor_x="right", size_hint_y=None, height=dp(30)
            )
            box = BoxLayout(size_hint_x=None, spacing=dp(5))
            box.bind(minimum_width=box.setter("width"))
            button_ok = MDRaisedButton(
                text=self.text_button_ok,
                on_release=lambda x: _events_callback(self.text_button_ok),
            )
            box.add_widget(button_ok)

            if self.text_button_cancel != "":
                button_cancel = MDFlatButton(
                    text=self.text_button_cancel,
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: _events_callback(
                        self.text_button_cancel
                    ),
                )
                box.add_widget(button_cancel)

            box_buttons.add_widget(box)
            instance_content_dialog.ids.box_buttons.add_widget(box_buttons)
            instance_content_dialog.ids.box_buttons.height = button_ok.height
            instance_content_dialog.remove_widget(
                instance_content_dialog.ids.sep
            )




class MDInputDialog(BaseDialogMDInputDialog):
    title = StringProperty("Title")
    hint_text = StringProperty("")
    text_button_ok = StringProperty("Ok")
    text_button_cancel = StringProperty()
    events_callback = ObjectProperty()
    _background = StringProperty(f"{images_path}ios_bg_mod.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content_dialog = ContentInputDialog(
            title=self.title,
            hint_text=self.hint_text,
            text_button_ok=self.text_button_ok,
            text_button_cancel=self.text_button_cancel,
            device_ios=self.device_ios,
        )

        self.add_widget(self.content_dialog)
        self.set_content(self.content_dialog)
        Clock.schedule_once(self.set_field_focus, 0.5)

    def set_field_focus(self, interval):
        self.text_field.focus = True


class MDDialog(BaseDialog):
    title = StringProperty("Title")
    text = StringProperty("Text dialog")
    text_button_cancel = StringProperty()
    text_button_ok = StringProperty("Ok")
    events_callback = ObjectProperty()
    _background = StringProperty(f"{images_path}ios_bg_mod.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        content_dialog = ContentMDDialog(
            title=self.title,
            text=self.text,
            text_button_ok=self.text_button_ok,
            text_button_cancel=self.text_button_cancel,
            device_ios=self.device_ios,
        )
        self.add_widget(content_dialog)
        self.set_content(content_dialog)


class ContentInputDialog(Heir):
    title = StringProperty()
    hint_text = StringProperty()
    text_button_ok = StringProperty()
    text_button_cancel = StringProperty()
    device_ios = BooleanProperty()


class ContentMDDialog(Heir):
    title = StringProperty()
    text = StringProperty()
    text_button_cancel = StringProperty()
    text_button_ok = StringProperty()
    device_ios = BooleanProperty()
























class ContentMDDialog_Photos(Heir,Screen):
   # title = StringProperty()
   # text = StringProperty()
    text_button_cancel = StringProperty()
    text_button_ok = StringProperty()
    #device_ios = BooleanProperty()



class BaseDialog_Photos(ThemableBehavior, ModalView):
    def set_content(self, instance_content_dialog):
        def _events_callback(result_press):
            self.dismiss()
            if result_press and self.events_callback:
                self.events_callback(result_press, self)

        if self.device_ios:  # create buttons for iOS
            pass
        else:  # create buttons for Android
            if isinstance(instance_content_dialog, ContentInputDialog):


                pass

                #instance_content_dialog.ids.box_input.height = dp(48)



            box_buttons = AnchorLayout(
                anchor_x="right", size_hint_y=None, height=dp(30)
            )



            box = BoxLayout(size_hint_x=None, spacing=dp(5))
            box.bind(minimum_width=box.setter("width"))
            button_ok = MDRaisedButton(
                text=self.text_button_ok,
                on_release=lambda x: _events_callback(self.text_button_ok),
            )
            box.add_widget(button_ok)


            box_buttons.add_widget(box)
            instance_content_dialog.ids.box_buttons.add_widget(box_buttons)
            instance_content_dialog.ids.box_buttons.height = button_ok.height




class MDDialog_Photos(BaseDialog_Photos,ScreenManager):
    text_button_cancel = StringProperty()
    text_button_ok = StringProperty("Close")
    events_callback = ObjectProperty()
    _background = StringProperty(f"{images_path}ios_bg_mod.png")

    def __init__(self,room, **kwargs):
        super().__init__(**kwargs)
        print(room)
        content_dialog = ContentMDDialog_Photos(
            text_button_ok=self.text_button_ok,
            text_button_cancel=self.text_button_cancel,
        )

        # Put Photos on the Screens to swipe
        url = "https://qnscunyvfnnzesjgophl.supabase.co"  # os.environ.get("SUPABASE_URL")
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFuc2N1bnl2Zm5uemVzamdvcGhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjMxMDc4NzksImV4cCI6MjAzODY4Mzg3OX0.ApOkDtGdm3eGRl0lR8A9PvijBQMtbORS2aVX-UR96ag"  # os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        room = room.replace(" ", "")

        photos = 10
        icon = []
        for photo in range(photos):
            strphoto = str(photo + 1)
            icon.append(supabase.storage.from_("eroomsphotos/" + str(room)).get_public_url(strphoto + ".jpg"))

        im0 = AsyncImage(source=icon[0],allow_stretch=True, keep_ratio=False)
        im1 = AsyncImage(source=icon[1],allow_stretch=True, keep_ratio=False)
        im2 = AsyncImage(source=icon[2],allow_stretch=True, keep_ratio=False)
        im3 = AsyncImage(source=icon[3],allow_stretch=True, keep_ratio=False)
        im4 = AsyncImage(source=icon[4],allow_stretch=True, keep_ratio=False)
        ##print(im1)

        # content_dialog.ids['screen_one'].add_widget(im1)
        content_dialog.ids['screen_one'].source = icon[0]
        content_dialog.ids['screen_two'].source = icon[1]
        content_dialog.ids['screen_three'].source = icon[2]
        content_dialog.ids['screen_four'].source = icon[3]
        content_dialog.ids['screen_five'].source = icon[4]

        
        content_dialog.ids['screen_six'].source = icon[5]
        content_dialog.ids['screen_seven'].source = icon[6]
        content_dialog.ids['screen_eight'].source = icon[7]
        content_dialog.ids['screen_nine'].source = icon[8]
        content_dialog.ids['screen_ten'].source = icon[9]

####        print(content_dialog.ids['screen_one'].source)
       # print(im1)
       # print(icon[1])
       # content_dialog.ids['test'].source = icon[1]

       # content_dialog.ids['screen_one'].add_widget(im1)


        #print(content_dialog.ids['screen_one'].background_normal)

       #content_dialog.ids['screen_four'].background_down = icon[1]
       # content_dialog.ids['screen_four'].background_normal = '2.jpg'


        #print('inside',content_dialog.ids['screen_four'].background_normal)


        self.add_widget(content_dialog)
        self.set_content(content_dialog)










class ContentMDDialog_Password(Heir):
    title = StringProperty()
    text = StringProperty()
    text_button_cancel = StringProperty()
    text_button_ok = StringProperty()
    text_button_password= StringProperty()
    device_ios = BooleanProperty()





class BaseDialog_Password(ThemableBehavior, ModalView):


    def set_content(self, instance_content_dialog):
        def _events_callback(result_press):
            self.dismiss()
            if result_press and self.events_callback:
                self.events_callback(result_press, self)

        def _events_callback_password(result_press):

            app = App.get_running_app()

            email = app.dialog_password.content_dialog.ids['emailinput'].text
            print('email=',email)






            if  email == '':
                 self.dialog_warning = MDDialog(title='Προειδοποίηση!(Warning!)',
                                                 text='Παρακαλώ συμπληρώστε το email σας για αποστολή του κωδικού σας!',
                                                 size_hint=[.45, .45])
                 self.dialog_warning.open()
            else:

              #  print(password_status)



#############-------------Match the Email from our Database to Recover Password-----
                 url = "https://qnscunyvfnnzesjgophl.supabase.co"  # os.environ.get("SUPABASE_URL")
                 key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFuc2N1bnl2Zm5uemVzamdvcGhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjMxMDc4NzksImV4cCI6MjAzODY4Mzg3OX0.ApOkDtGdm3eGRl0lR8A9PvijBQMtbORS2aVX-UR96ag"  # os.environ.get("SUPABASE_KEY")
                 supabase = create_client(url, key)
                 data = None
                 data1 = None
                 password_owner= None
                 password_renter = None
                 loginowner= False
                 loginrenter= False

                 username = email

                 try:
                    data= supabase.table("Owners_Users").select("Username, Password").eq("Username", username).execute()
                    password_owner = data.data[0]['Password']
                    loginowner = True
                 except:
                    loginowner = False

                 try:
                     data = supabase.table("Renters_Users").select("Username, Password").eq("Username",username).execute()
                     password_renter = data.data[0]['Password']
                     loginrenter = True
                 except:
                     loginrenter = False



                 if loginowner == True or loginrenter == True:
                      if loginowner == True:
                          urpassword = password_owner

                      if loginrenter  == True:
                          urpassword = password_renter
#######################-----------Send Email--------------------####################
                      port = 587  # For starttls
                      smtp_server = "smtp.gmail.com"
                      sender_email = 'erooms2024@gmail.com'  #"amanatid@gmail.com"  # Enter your address
                      receiver_email = email  # Enter receiver address
                      password = 'zkka mrdk pbvl kmeu'  #'pbmy oyhd fjsv abqe'
                      message = f"\nSubject: Hi there,\n Your password is {urpassword}"

                      context = ssl.create_default_context()
                      with smtplib.SMTP(smtp_server, port) as server:
                          server.ehlo()  # Can be omitted
                          server.starttls(context=context)
                          server.ehlo()  # Can be omitted
                          server.login(sender_email, password)
                          try:
                              server.sendmail(sender_email, receiver_email, message)
                          except:
                              print('Something went wrong')




                 else:
                     self.dialog_register_status = MDDialog(title='Λάθος email ή πρόβλημα με τον server!(Wrong Email or Server Issue!)',
                                                   text='',size_hint=[.45, .45])
                     self.dialog_register_status.open()





#######################-----------Send Email--------------------####################
#                port = 587  # For starttls
#                smtp_server = "smtp.gmail.com"
#                sender_email = 'erooms2024@gmail.com'  #"amanatid@gmail.com"  # Enter your address
#                receiver_email = email  # Enter receiver address
#                password = 'zkka mrdk pbvl kmeu'  #'pbmy oyhd fjsv abqe'
#                message = f"\nSubject: Hi there,\n Your password is {urpassword}"
#
#                context = ssl.create_default_context()
#                with smtplib.SMTP(smtp_server, port) as server:
#                    server.ehlo()  # Can be omitted
#                    server.starttls(context=context)
#                    server.ehlo()  # Can be omitted
#                    server.login(sender_email, password)
#                    try:
#                        server.sendmail(sender_email, receiver_email, message)
#                    except:
#                        print('Something went wrong')
#                        password_status = 'Email Not Sent'

#            if password_status== None:
#                self.dialog_register = MDDialog(
#                    title='Ο Κωδικός σας αποστάλει επιτυχώς στο email σας!(Succesfull send of the password onto your mailbox !)',
#                    text='',
#                    size_hint=[.45, .45])
#                self.dialog_register.open()
#            else:
#                self.dialog_register_status = MDDialog(
#                    title='Λάθος email ή πρόβλημα με τον server!(Wrong Email or Server Issue!)',
#                    text='',
#                    size_hint=[.45, .45])
#                self.dialog_register_status.open()


######################--------------End Send Email--------------------####################

            ###print('Button Press', self.events_callback, result_press)

            if result_press and self.events_callback:
                self.events_callback(result_press, self)





        if self.device_ios:  # create buttons for iOS
            pass

        else:  # create buttons for Android

            if isinstance(instance_content_dialog, ContentInputDialog):
                self.text_field = MDTextFieldRect(
                    #hint_text=None,
                    #helper_text_mode='on_focus',
                    size_hint=(1, None),
                    height=dp(48),
                    hint_text=instance_content_dialog.hint_text,
                )


                instance_content_dialog.ids.box_input.height = dp(48)
                instance_content_dialog.ids.box_input.add_widget(
                    self.text_field
                )



                instance_content_dialog.ids.box_buttons.remove_widget(
                    instance_content_dialog.ids.sep
                )

            box_buttons = AnchorLayout(
                anchor_x="right", size_hint_y=None, height=dp(30)
            )
            box = BoxLayout(size_hint_x=None, spacing=dp(5))
            box.bind(minimum_width=box.setter("width"))

            button_password = MDRaisedButton(
                text=self.text_button_password, font_size=18,
                on_release=lambda x: _events_callback_password(self.text_button_password),
            )
            box.add_widget(button_password)


            button_ok = MDRaisedButton(
                text=self.text_button_ok,font_size=18,
                on_release=lambda x: _events_callback(self.text_button_ok),
            )
            box.add_widget(button_ok)

            if self.text_button_cancel != "":
                button_cancel = MDFlatButton(
                    text=self.text_button_cancel,
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: _events_callback(
                        self.text_button_cancel
                    ),
                )
                box.add_widget(button_cancel)

            box_buttons.add_widget(box)
            instance_content_dialog.ids.box_buttons.add_widget(box_buttons)
            instance_content_dialog.ids.box_buttons.height = button_ok.height
            instance_content_dialog.remove_widget(
                instance_content_dialog.ids.sep
            )



class MDDialog_Password(BaseDialog_Password):
    title = StringProperty("Title")
    text = StringProperty("Text dialog")
    text_button_cancel = StringProperty()
    text_button_ok = StringProperty("Close")
    text_button_password= StringProperty("Send Email")

    events_callback = ObjectProperty()
    _background = StringProperty(f"{images_path}ios_bg_mod.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_dialog = ContentMDDialog_Password(
            title=self.title,
            text=self.text,
            text_button_ok=self.text_button_ok,
            text_button_cancel=self.text_button_cancel,
            text_button_password= self.text_button_password,
            device_ios=self.device_ios,
        )


        self.add_widget(self.content_dialog)
        self.set_content(self.content_dialog)










