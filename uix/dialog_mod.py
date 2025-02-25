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
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
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
                        text: "Τύπος Μισθώματος(Rent Type): "
                    ThinLabel:
                        text: root.RentType              
                        
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
                        text: "Τιμή(Price): "
                    ThinLabelButton:
                        text: root.Price
                
                                
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
    allow_stretch: True
    keep_ratio: False        

<ContentMDDialog_Photos@Screen>
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    #text_button_ok: ''
    #text_button_cancel: ''
    MDLabel:
        text:'hi'
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
                Button:
                    id: screen_two
                    text: "Go to Screen 34"
                    background_color : 1, 0, 0, 1
                    on_press:
                        root.ids.scrn_mngr.current ='screen_three'
                        
        Screen:
            name: 'screen_three' 
            BoxLayout:
                Button:
                    id: screen_three
                    text: "Go to Screen 5"
                    background_color : 1, 0, 1, 1
                    on_press:
                        root.ids.scrn_mngr.current ='screen_four' 
                        
                                
        Screen:
            name: 'screen_four' 
            BoxLayout:
                Button:
                    id: screen_four
                    text: "Go to Screen 6"
                   # background_normal : '1.jpg'
			       # background_down  : '1.jpg'
                    on_press:
                        root.ids.scrn_mngr.current ='screen_five' 
                        
        
        Screen:
            name: 'screen_five' 
            BoxLayout:
                Button:
                    id: screen_five
                    text: "Go to Screen 7"
                    background_color : 1, 0, 1, 1
                    on_press:
                        root.ids.scrn_mngr.current ='screen_one'                           
    
       
    

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
    Price = StringProperty("Missing data")
    Website1 = StringProperty("Missing data")
    Website2 = StringProperty("Missing data")

    background = StringProperty('{}ios_bg_mod.png'.format(images_path))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def on_button(self):
        ###print('insideddddddddddddddd')
        self.dialog = MDDialog_Photos( self.Title)
        self.dialog.open()
        pass



class MDInputDialog(BaseDialog):
    title = StringProperty("Title")
    hint_text = StringProperty()
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
























class ContentMDDialog_Photos(Screen):
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
    text_button_ok = StringProperty("Ok")
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

        photos = 2
        icon = []
        for photo in range(photos):
            strphoto = str(photo + 1)
            icon.append(supabase.storage.from_("eroomsphotos/" + str(room)).get_public_url(strphoto + ".jpg"))

        im1 = AsyncImage(source=icon[1],allow_stretch=True, keep_ratio=False)
        # content_dialog.ids['screen_one'].add_widget(im1)
        content_dialog.ids['screen_one'].source = icon[1]
        print(content_dialog.ids['screen_one'].source)
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












