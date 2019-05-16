
import datetime
# importa l'API de Telegram
import telegram
import data as d
from telegram.ext import Updater
from telegram.ext import CommandHandler

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Hey! What can I do for you?")
    G = d.Graph()
    user_data['graph'] = G

def help(bot,update):
    message='These are the commands which can be used: \n\
/start: It will initialize the bot \n\
/graph <distance>: It will create a graph whose edges distance are, at most, the given distance\n\
/plotgraph: It will create and display a map with the nodes and the edges of the graph\n\
/nodes: It will return the number of nodes of the graph\n\
/edges: It will return the number of edges of the graph\n\
/components: It will return the number of connected components of the graph\n\
/route <origin, target>: Given the directions, it will return the shortest path.\n\
/authors: It will return the name and the emails of the authors of this bot.'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def hour_to_min(t):
    hour = int(t//1)
    min = int(((t-hour) * 60)+0.5)
    return hour, min

def graph(bot, update, user_data, args):
    if (args):
        G = d.Graph(int(args[0]))
        bot.send_message(chat_id=update.message.chat_id, text="Graph created with distance " + str(args[0])) + "!"
    else:
        G = d.Graph()
        bot.send_message(chat_id=update.message.chat_id, text="Since no distance was received, the graph by default, which has been created, has distance 1000")
    user_data['graph'] = G



def hora(bot, update):
    missatge = str(datetime.datetime.now())
    bot.send_message(chat_id=update.message.chat_id, text=missatge)

def plotgraph(bot,update,user_data):
    d.print_map(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text="Creant mapa...🚲🚲🚲🚲🚲")
    bot.send_photo(chat_id=update.message.chat_id, photo=open('map.png', 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text="Mapa creat‼")


def route(bot,update,args,user_data):
    cami = " ".join(args)
    address1, address2 = cami.split(',')
    bot.send_message(chat_id=update.message.chat_id, text="Computing the shortest path...")
    t = d.route(user_data['graph'],cami)
    bot.send_photo(chat_id=update.message.chat_id, photo=open('path.png', 'rb'))
    hour,min = hour_to_min(t)
    message = "Going from " + address1 + " to"+ address2+ " will take you " + str(hour) +" hour(s) "+ str(min) + " min(s)."
    bot.send_message(chat_id=update.message.chat_id, text=message)

def nodes(bot, update, user_data):
    nodes = d.Nodes(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=str(nodes))

def edges(bot, update, user_data):
    edges = d.Edges(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=str(edges))

def connectivity(bot, update, user_data):
    components = d.components(user_data['graph'])
    bot.send_message(chat_id=update.message.chat_id, text=str(components))

def authors(bot, update, user_data):
    authors = d.authors()
    bot.send_message(chat_id=update.message.chat_id, text=str(authors))


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
dispatcher.add_handler(CommandHandler('route', route,pass_user_data=True,pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes,pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges,pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', connectivity,pass_user_data=True))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))

# engega el bot
updater.start_polling()
