import logging
import requests

logger = logging.getLogger(__name__)


class Bot:
    """ Basic telegram bot using web API"""
    
    domain = f"https://api.telegram.org"
    
    def __init__(self, token):
        self.token = token
        self.base_url = f"{self.domain}/bot{self.token}"
        
    def _request(
        self, endpoint, method="GET", params=None, **kwargs
    ):
        query_url = self.base_url + endpoint 
        r = requests.request(method, query_url, params=params, **kwargs)
        if r.status_code != 200 and r.status_code != 201:
            raise Exception(f"Request error: {r.status_code} {r.text}")
        
        return r 

    def get_me(self) -> requests.models.Response:
        r = self._request("/getMe")
        return r
    
    def get_updates(self) -> requests.models.Response:
        r = self._request("/getUpdates")
        return r

    def send_message(self, chat_id, text, **kwargs):
        params = {
            "chat_id": chat_id,
            "text": text
        }
        if kwargs:
            params.update(kwargs)

        r = self._request("/sendMessage", params=params)
        return r


# Deprecated code using python-telegram-bot package v13.x
# class TelegramBot:
#     """ Simple telegram bot for sending messages
# 
# 
#     Args:
#         token (str): Telegram token for bot
#         filename (str, optional): Filename of pickled persistent data
#     """
# 
#     def __init__(self, token, filename=None):
#         self.token = token
#         persistence = PicklePersistence(filename) if filename is not None else None
#         self.updater = Updater(
#             self.token, use_context=True
#         )
#         dp = self.updater.dispatcher 
#         dp.add_handler(CommandHandler("start", self._start))
#         dp.add_error_handler(self._error)
#     
#     def start_polling(self):
#         self.updater.start_polling()
#         logger.info('Telegram bot started polling...')
# 
#     def stop(self):
#         self.updater.stop()
#         logger.info(f'Telegram bot stopped polling.')
# 
#     def send_message(self, chat_id, text, **kwargs):
#         # TODO: Handle multiple chat IDs
#         self.updater.bot.send_message(chat_id, text, **kwargs)
#         logger.info(f'Sent message to {chat_id}.')
# 
#     # Command handlers for telegram bot are denoted as private methods. 
#     @staticmethod
#     def _start(update, context):
#         """Command handler for telegram bot"""
#         # TODO: Retrieve chat ID
#         update.message.reply_text('Notifications on!')
# 
#     @staticmethod
#     def _error(update, context):
#         """Log Errors caused by Updates."""
#         logger.warning(f'Update "{update}" caused error "{context.error}"')    
