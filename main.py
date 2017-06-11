# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
import logging
import configparser
import datetime
import os
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
    now = str (datetime.datetime.now())
    for c in ['.', ':', '-', ' ']:
        now = now.replace(c, '_')
    if len(message.photo) > 0:
        file_id = message.photo[-1].file_id
        file_name = 'Photo_{now}'.format(now=now)
    elif message.video is not None:
        file_id = message.video.file_id
        file_name = 'Video_{now}'.format(now=now)
    elif message.document is not None:
        file_id = message.document.file_id
        file_name = message.document.file_name

    local_tmp_file = "/tmp/{file_name}".format(file_name=file_name)
    bot.get_file(file_id).download(custom_path=local_tmp_file)

    try:
        oc.mkdir(config['owncloud']['BACKUP_FOLDER'])
    except:
        logger.info('{} already exists.'.format(config['owncloud']['BACKUP_FOLDER']))

    today = str(datetime.date.today())
    try:
        oc.mkdir('{backup_folder}/{today}'.format(backup_folder=config['owncloud']['BACKUP_FOLDER'],
                                                  today=today))
    except HTTPResponseError:
        pass

    oc.put_file('{backup_folder}/{today}/{file_name}'.format(backup_folder=config['owncloud']['BACKUP_FOLDER'],
                                                             today=today,
                                                             file_name=file_name), local_tmp_file)

    os.remove(local_tmp_file)

    logger.info('File {} backuped to owncloud.'.format(file_name))

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
