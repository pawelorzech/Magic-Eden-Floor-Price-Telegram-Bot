# Magic Eden Floor Price Telegram Bot
 
An easy-to-use Telegram bot code for notifications when the floor price of a project on Magic Eden reaches below the a specifically set floor price. Tracked collections are saved dependent on the chat. So multiple users can use the bot, and track different collections without causing issue for other users.

## How to setup the bot:

- Clone this repository into your local machine. 
- Make sure to have Python 3 installed.
- Run the following command in the project directory to install the required python libraries:
`pip install -r requirement.txt`
- Initialize a bot on Telegram. Use @BotFather to do this. It will give you a bot access token. Paste the bot token into line 16 of botScript.py.
- Run the botScript.py, and your bot will be online!
- Use /help for all available commands.

## Available bot commands:
- `/help`: Shows all possible commands.
- `/addCollection <magic eden collection link> <floor price for which to notify for example - 1.2>`: Adds the collection to track the floor price of.
- `/removeCollection <magic eden collection link>`: Removes the collection from being tracked.
- `/getCollection`: Shows all the collections being tracked.
- `/changeFloor <magic eden collection link> <new floor price for notification>`: Sets a new minimum floor price.
- `/start`: Starts sending notifications.
- `/stop`: Stops sending notifications.
