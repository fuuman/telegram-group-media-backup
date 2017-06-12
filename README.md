# telegram-group-media-backup

This code can run as bot for the telegram messenger. After creating your own bot and connecting it to that script via config.ini, you can add it to a telegram group. Take care, that the [privacy mode](https://core.telegram.org/bots#privacy-mode) of your bot is disabled. If it's not, your bot cannot read the messages sent to your group. After adding every photo, video or file sent to that group will be backuped to a configured folder on an owncloud server. 

## What you need
- a telegram bot token (create via bot father)
- running owncloud server
- _optional_: a server where your bot can run (You can run it locally on your PC, but if your session is closed or the PC powered off, there will be no backups. So I would suggest you to use free providers like _heroku_ if you aren't running a server on your own.)


## How to start
- git clone https://github.com/fuuman/telegram-group-media-backup.git
- cd telegram-group-media-backup
- cp config.ini.example config.ini
- edit config.ini and fill in your configuration data (you need to create a new telegram bot first)
- `pip install -r requirements.txt` in a new virtualenv using python3.6

To test if everything is working well, you can run `python main.py` and add your new bot to a telegram group now. Sending a file to the group should let it appear in your owncloud.

### Info
This bot was implemented using the [python-telegram-bot](https://python-telegram-bot.org/), a nice wrapper for the official Telegram API.

### TODO 
- add more cloud storage provider

### LICENSE
[MIT License](https://github.com/fuuman/telegram-group-media-backup/blob/master/LICENSE)

Copyright (c) 2017 Marco Schanz
