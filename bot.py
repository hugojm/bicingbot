
import datetime
# importa l'API de Telegram
import telegram
import data as d
from telegram.ext import Updater
from telegram.ext import CommandHandler

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Benvingut al bicing_bot!")


def graph(bot, update, user_data,args):
    if (args):
        G = d.Graph(int(args[0]))
    else:
        G = d.Graph()
    user_data['graph'] = G
    bot.send_message(chat_id=update.message.chat_id, text="Graph created 🚀🚀🚀🚀")


def hora(bot, update):
    missatge = str(datetime.datetime.now())
    bot.send_message(chat_id=update.message.chat_id, text=missatge)

def plotgraph(bot,update,user_data):
    d.print_map(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text="Creant mapa..🚲🚲🚲🚲🚲")
    bot.send_photo(chat_id=update.message.chat_id, photo=open('map.png', 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text="Mapa creat‼")


def route(bot,update,args):
    d.route(Graph(),args[0])
    bot.send_photo(chat_id=update.message.chat_id, photo=open('path.png', 'rb'))

def nodes(bot, update, user_data):
    nodes = d.Nodes(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=str(nodes))

def edges(bot, update, user_data):
    edges = d.Edges(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=str(edges))

def connectivity(bot, update, user_data):
    components = d.components(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=str(components))

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start,pass_user_data=True))
dispatcher.add_handler(CommandHandler('graph', graph,pass_user_data=True,pass_args=True))
dispatcher.add_handler(CommandHandler('hora', hora))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph,pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route,pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes,pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges,pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', connectivity,pass_user_data=True))

# engega el bot
updater.start_polling()
