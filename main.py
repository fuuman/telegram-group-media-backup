#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to send timed Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, Job, MessageHandler, Filters
import logging
import configparser
import datetime
import time
from lib.owncloud_helper import OwncloudHelper
from owncloud import HTTPResponseError

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()

oc = OwncloudHelper().oc

def backup(bot, update):
    message = update.message
    if len(message.photo) > 0:
        file_id = message.photo[-1].file_id
        file_name = 'Photo_{id}'.format(id=str(time.time()).replace('.',''))
    elif message.video is not None:
        file_id = message.video.file_id
        file_name = 'Video_{id}'.format(id=str(time.time()).replace('.',''))
    elif message.document is not None:
        file_id = message.document.file_id
        file_name = message.document.file_name

    bot.get_file(file_id).download(custom_path="/tmp/{file_name}".format(file_name=file_name))

    today = str(datetime.date.today())
    try:
        oc.mkdir('family_media_backup/{}'.format(today))
    except HTTPResponseError:
        pass

    oc.put_file('family_media_backup/{}/{}'.format(today, file_name),
                '/tmp/{file_name}'.format(file_name=file_name))

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    config.read('config.ini')

    updater = Updater(config['bot']['API_TOKEN'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(Filters.video | Filters.photo | Filters.document, backup))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
