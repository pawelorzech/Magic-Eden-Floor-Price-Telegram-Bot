import logging
from time import sleep
from telegram.ext import Updater, CommandHandler
import requests
import pprint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
global collection
collection = {"5298831332": {"united_ape_nation": 0.0}}
global updateRate
updateRate = 30
botToken = '5197120221:AAEQkrp7S4aDw5XoV1Na2wS7tum5oreXEhw'

def store_dict(fname, dic):
    with open(fname, "w") as f:
        f.write(pprint.pformat(dic, indent=4, sort_dicts=False))

def test(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(str(update.message.chat.id))

def help(update, context):
    """Send a message when the command /help is issued."""
    ret = "'/help': Shows all possible commands.\n'/addCollection <magic eden collection link> <floor price for which to notify for example - 1.2>': Adds the collection to track the floor price of.\n'/removeCollection <magic eden collection link>': Removes the collection from being tracked.\n'/getCollection': Shows all the collections being tracked.\n'/changeFloor <magic eden collection link> <new floor price for notification>': Sets a new minimum floor price.\n'/start': Starts sending notifications.\n'/stop': Stops sending notifications.\nIf you encounter any issues, send a message to @RageFked."

    update.message.reply_text(ret)    

def id(update, context):
    """Send a message when the command /id is issued."""
    userDetails = update.message.from_user
    print(userDetails['id'])
    update.message.reply_text(str(userDetails['id']))

def addCollection(update, context):
    newCol = (context.args[0]).split("/")[-1]
    userID = str(update.message.chat.id)

    if userID in collection:
        if newCol not in collection[userID]:
            if len(context.args) == 1:
                collection[userID][newCol] = 0.0
            else:
                collection[userID][newCol] = float(context.args[1])
                
            store_dict()
            update.message.reply_text("Collection added for tracking.")
        else:
            update.message.reply_text("Collection already tracked.")
    else:
        collection[userID] = {}
        if len(context.args) == 1:
            collection[userID][newCol] = 0.0
        else:
            collection[userID][newCol] = float(context.args[1])
        store_dict()
        
def changeFloor(update, context):
    newCol = (context.args[0]).split("/")[-1]
    userID = str(update.message.chat.id)

    if userID in collection:
        if newCol in collection[userID] and len(context.args) > 1:
            collection[userID][newCol] = float(context.args[1])
            update.message.reply_text("Floor price changed.")
            store_dict()
        else:
            update.message.reply_text("This collection is not tracked.")
    else:
        update.message.reply_text("You have no collection added for tracking.")


def removeCollection(update, context):
    newCol = (context.args[0]).split("/")[-1]
    userID = str(update.message.chat.id)
    
    if userID in collection:
        if newCol not in collection[userID]:
            update.message.reply_text("Collection is not tracked.")
        else:
            collection[userID].pop(newCol)
            update.message.reply_text("Collection removed from tracking.")
            store_dict()
    

def getCollection(update, context):
    ret_str = ""
    userID = str(update.message.chat.id)

    if userID in collection:
        for key in collection[userID]:
            if collection[userID][key] <= 0.0:
                ret_str = ret_str + key + ": Always notified. No floor price set.\n"
            else:
                ret_str = ret_str + key + ": Notified if floor price is at or below " + str(collection[userID][key]) + " SOL.\n"
    else:
        ret_str = 'You have no collection added for tracking.'
    update.message.reply_text(ret_str)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def newPing(context):
    context.bot.send_message(context.job.context, text=checkFloor(userID = str(context.job.context)))

def startTimer(update, context):
    context.job_queue.run_repeating(newPing, updateRate, context=update.message.chat_id, name=str(update.message.chat.id))

def stopTimer(update, context):
    for job in context.job_queue.get_jobs_by_name(str(update.message.chat.id)):
        job.schedule_removal()
    update.message.reply_text("Job removed.")

def store_dict():
    with open("trackedData.json", "w") as f:
        f.write(pprint.pformat(collection, indent=4, sort_dicts=False))

def load_file():
    try:
        with open("trackedData.json", "r") as f:
            dic = eval(f.read())
    except:
        dic = {}
    return dic

def checkFloor(userID):
    res = []
    if str(userID) in collection:
        for key in collection[userID]:
            sleep(0.5)
            url = "http://api-mainnet.magiceden.dev/v2/collections/" + key + "/stats"
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload).json()
            prc = response['floorPrice']/1000000000
            if collection[userID][key] <= 0.0 or (collection[userID][key] > 0.0 and prc <= collection[userID][key]):
                res.append(key.replace("_", " ").title() + ": " + str(prc) + " SOL")
    else:
        res.append("You have nothing to track.")

    return '\n'.join(map(str, res))

def main():
    updater = Updater(botToken, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("id", id))
    dp.add_handler(CommandHandler('addCollection', addCollection))
    dp.add_handler(CommandHandler('removeCollection', removeCollection))
    dp.add_handler(CommandHandler('getCollection', getCollection))
    dp.add_handler(CommandHandler('changeFloor', changeFloor))
    dp.add_handler(CommandHandler('start', startTimer, pass_job_queue=True))
    dp.add_handler(CommandHandler('stop', stopTimer, pass_job_queue=True))


    dp.add_error_handler(error)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    while True:
        sleep(5)

if __name__ == '__main__':
    collection = load_file()
    main()