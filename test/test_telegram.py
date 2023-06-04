import os
import unittest
import dipzy as dz


class TestBot(unittest.TestCase):
    def setUp(self):
        token = os.environ.get("TELEGRAM_TOKEN")
        self.bot = dz.telegram.Bot(token)
        
    def test_init(self):
        r = self.bot.get_me()
        self.assertEqual(r.status_code, 200)
    
    def test_get_updates(self):
        r = self.bot.get_updates()

    def test_send_message(self):
        chat_id = 948759574
        r = self.bot.send_message(chat_id, "unittest!")
