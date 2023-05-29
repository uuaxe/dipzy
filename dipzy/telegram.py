import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PicklePersistence
)


logger = logging.getLogger(__name__)

class TelegramBot:
    """ Simple telegram bot for sending messages


    Args:
        token (str): Telegram token for bot
        filename (str, optional): Filename of pickled persistent data
    """

    def __init__(self, token, filename=None):
        self.token = token
        persistence = PicklePersistence(filename) if filename is not None else None
        self.updater = Updater(
            self.token, persistence=persistence, use_context=True
        )
        dp = self.updater.dispatcher 
        dp.add_handler(CommandHandler("start", self._start))
        dp.add_error_handler(self._error)
    
    def start_polling(self):
        self.updater.start_polling()
        logger.info('Telegram bot started polling...')

    def stop(self):
        self.updater.stop()
        logger.info(f'Telegram bot stopped polling.')

    def send_message(self, chat_id, text, **kwargs):
        # TODO: Handle multiple chat IDs
        self.updater.bot.send_message(chat_id, text, **kwargs)
        logger.info(f'Sent message to {chat_id}.')

    # Command handlers for telegram bot are denoted as private methods. 
    @staticmethod
    def _start(update, context):
        """Command handler for telegram bot"""
        # TODO: Retrieve chat ID
        update.message.reply_text('Notifications on!')

    @staticmethod
    def _error(update, context):
        """Log Errors caused by Updates."""
        logger.warning(f'Update "{update}" caused error "{context.error}"')    
