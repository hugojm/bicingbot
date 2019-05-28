
import datetime
# importa l'API de Telegram
import telegram
import data as d
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from geopy.geocoders import Nominatim
import os

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update, user_data):
    name = update.message.chat.first_name
    bot.send_message(chat_id=update.message.chat_id, text="Hey " + name + "! What can I do for you?")
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
    filename = str(update.message.chat.username)+'.png'
    d.print_map(user_data['graph'],filename)
    bot.send_message(chat_id=update.message.chat_id, text="Creant mapa...🚲🚲🚲🚲🚲")
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text="Mapa creat‼")
    os.remove(filename)

def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.longitude,
                location1.latitude), (location2.longitude, location2.latitude)
    except BaseException:
        return None

def addressTOcoordinate(address):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        location1 = geolocator.geocode(address + ', Barcelona')
        return (location1.longitude,
                location1.latitude)
    except BaseException:
        return None

def route(bot,update,args,user_data):
    if (len(args) <= 4):
        cami = " ".join(args)
        coord2 = addressTOcoordinate(cami)
        filename = str(update.message.chat.username)+'_path.png'
        bot.send_message(chat_id=update.message.chat_id, text="Computing the shortest path...")
        t = d.route(user_data['graph'],(user_data['lon'],user_data['lat']),coord2,filename)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
        os.remove(filename)
        hour,min = hour_to_min(t)
    if (len(args) > 4):
        filename = str(update.message.chat.username)+'_path.png'
        cami = " ".join(args)
        address1, address2 = cami.split(',')
        coord1, coord2 = addressesTOcoordinates(cami)
        bot.send_message(chat_id=update.message.chat_id, text="Computing the shortest path...")
        t = d.route(user_data['graph'],coord1,coord2,filename)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
        os.remove(filename)
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

def distribute(bot, update, args):
    requiredBikes, requiredDocks = int(args[0]) , int(args[1])
    flowCost, flowDict, G = d.bicing_flow(0.6, requiredBikes, requiredDocks)
    message = "The total cost of transferring bikes is " + str(flowCost/1000) + " km."
    bot.send_message(chat_id=update.message.chat_id, text=str(message))
    for src in flowDict:
        if src[0] != 'g': continue
        idx_src = int(src[1:])
        for dst, b in flowDict[src].items():
            if dst[0] == 'g' and b > 0:
                idx_dst = int(dst[1:])
                line = str(idx_src) + " -> " + str(idx_dst) + " " + str(b) + " bikes, distance " + str(G.edges[src, dst]['weight'])
                bot.send_message(chat_id=update.message.chat_id, text=str(line))

def unknown(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="No command found")

def where(bot, update, user_data):
    user_data['lat'], user_data['lon'] = update.message.location.latitude, update.message.location.longitude
    bot.send_message(chat_id=update.message.chat_id, text='Ets a les coordenades %f %f' % (user_data['lat'], user_data['lon']))

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
dispatcher.add_handler(CommandHandler('distribute', distribute, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))

# engega el bot
updater.start_polling()
