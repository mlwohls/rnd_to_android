from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables.datatables import MDDataTable
from kivy.properties import StringProperty
from kivy.metrics import dp

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from datetime import datetime
import uuid

from database import Database
# Initialize db instance
db = Database()

Window.size = (540, 1200)

class MainScreen(Screen):
    pass

class DrillsScreen(Screen):
    pass

class TwoByFourScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_scores = []
        self.entry_dialog = None
        self.data_table = None
        self.data_table_row_num = 0
        self.history_table = None
    
    def show_dialog(self, **kwargs):
        if not self.entry_dialog:
            self.entry_dialog = MDDialog(
                title="Enter Score",
                type="custom",
                content_cls=TwoByFourDialog(),
            )
        self.entry_dialog.open()
        pass 

    def close_dialog(self, *args):
        self.entry_dialog.dismiss()

    def on_pre_enter(self, *args):
        app.current_drill = "twobyfours"
        app.update_session_id()
        self.add_history()
        
        if not self.data_table:
            self.data_table = MDDataTable(
                pos_hint={"center_y": 0.5, "center_x": 0.5},
                use_pagination=False,
                column_data=[
                    ("Station", dp(20)),
                    ("Target", dp(15)),
                    ("Score", dp(15)),
                    ("Notes", dp(50)),
                ],
                row_data=[],
            )
            self.ids.twobyfour_current_container.add_widget(self.data_table)
        
        #clear row_data when screen loads
        self.data_table.row_data = []

    def add_score(self, drill, session_id, score, other=None):
        db.submit_score(drill, session_id, int(score.text), other)
        self.close_dialog()
        self.data_table.add_row((str(self.data_table_row_num + 1), "4", score.text, ""))
        self.data_table_row_num += 1
        pass 

    def submit_session(self, **kwargs):
        print("Session submitted")
        pass 
    
    def pull_current_scores(self):
        session_id = app.session_id
        self.current_scores = db.get_session_scores('twobyfours', session_id)

    def add_history(self):

        if not self.history_table:
            self.history_table = MDDataTable(
                    pos_hint={"center_y": 0.5, "center_x": 0.5},
                    use_pagination=False,
                    column_data=[
                        ("Date", dp(30)),
                        ("# of Stations", dp(30)),
                        ("Average Score", dp(30)),
                    ],
                    row_data=[],
                )
            self.ids.twobyfour_history_container.add_widget(self.history_table)

        else:
            #clear_history
            self.history_table.row_data = []
        
        #update current history data
        row_data = []
        rows = db.get_historical_scores('twobyfours', app.session_id, limit = 5)
        for row in rows:
            row_data.append([row[1].strftime("%m/%d"), row[2], round(row[3],1)])
        
        self.history_table.row_data = row_data

    pass

class TwoByFourDialog(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE INPUT FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def close_dialog(self):
        self.dismiss()

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(DrillsScreen(name='drills'))
sm.add_widget(TwoByFourScreen(name='twobyfour'))

class MainApp(MDApp):
    current_drill = None
    current_scores = None
    historical_scores = None
    entry_dialog = None
    session_id = str(uuid.uuid4())

    def update_session_id(self):
        self.session_id = str(uuid.uuid4())

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"
    
    # def show_dialog(self, **kwargs):
    #     if not self.entry_dialog:
    #         self.entry_dialog = MDDialog(
    #             title="Enter Score",
    #             type="custom",
    #             content_cls=TwoByFourDialog(),
    #         )

    #     self.entry_dialog.open()
    #     pass 

    # def close_dialog(self, *args):
    #     self.entry_dialog.dismiss()
    #     self.pull_current_scores()
    
    # def pull_current_scores(self):
    #     self.current_scores = db.get_session_scores(self.current_drill, self.session_id)
        # print("APP...Trying to pull scores")
        # print(self.current_scores)
    
    
    

app = MainApp()
app.run()
