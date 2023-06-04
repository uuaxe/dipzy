import os
import unittest
import dipzy as dz


class TestTwitter(unittest.TestCase):
    def setUp(self):
        token = os.environ.get("TWITTER_BEARER")
        self.twtr = dz.Twitter(token)
        
    def test_get_users(self):
        r = self.twtr.get_users(usernames="elonmusk")
