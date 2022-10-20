from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.leaderboard_list.items = anvil.server.call('get_leaderboard')
        self.total_flags = 35
        self.flags_left.text = self.total_flags

        # Initialize timer
        self.end_time = datetime(2022, 10, 18, 15, 40)
        self.timer_1.interval = 1

    def timer_1_tick(self, **event_args):
        '''This method is called Every [interval] seconds. Does not trigger if [interval] is 0.'''
        remaining_time = (self.end_time - datetime.now()).total_seconds() - 19800
        time = datetime.fromtimestamp(remaining_time)
        if remaining_time > 3600 * 3 or remaining_time < 0:
            self.time_remaining.text = '00:00'
        else:
            self.time_remaining.text = time.strftime('%M:%S' if remaining_time < 3600 else '%H:%M')
        self.timer_1.interval = 0 if remaining_time <= 0 else 1

    def leaderboard_refresh_timer_tick(self, **event_args):
        '''This method is called Every [interval] seconds. Does not trigger if [interval] is 0.'''
        self.leaderboard_list.items = anvil.server.call('get_leaderboard')
        self.refresh_data_bindings()
        self.flags_left.text = str(self.total_flags - sum([r['team_score'] for r in self.leaderboard_list.items]))
        
