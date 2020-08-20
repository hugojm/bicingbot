
import datetime
import telegram
import data as d
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from geopy.geocoders import Nominatim
import os


def start(bot, update, user_data):
    name = update.message.chat.first_name
    message = "Hey " + str(name) + "!😊\nI've been programmed to satisfy " +\
        "your desires about bicing in Barcelona.\n"\
        + "If by any chance you feel lost in any possible way, do not " +\
        "hesitate to ask for /help and I'll try to help" \
        + " you.😉"
    bot.send_message(chat_id=update.message.chat_id, text=message)
    G = d.CreateGraph()
    user_data['graph'] = G


def help(bot, update):
    message = "Oops! I notice someone is a bit lost here... Let's see if " +\
        "this helps you out!😝\n" +\
        "These are the commands which can be used:\n" +\
        "/start: It will initialize the bot\n" +\
        "/graph *<distance>*: It will create a graph in which two stations " +\
        "are connected if they are, at most, the given distance.\n" +\
        "/plotgraph: It will create and display a map with the nodes" +\
        "and the edges of the graph.\n" +\
        "/nodes: It will return the number of nodes of the graph.\n" +\
        "/edges: It will return the number of edges of the graph.\n" +\
        "/components: It will return the number of connected components " +\
        "of the graph.\n" +\
        "/route *<origin, target>*: Given the directions, it will return " +\
        "the shortest path. *NOTE:* In case it only receives one adress, " +\
        "it will take your location as the origin and the given one as a " +\
        "destination. ⚠️_Ensure that you have send your location before._\n" +\
        "/authors: It will return the name and the emails of the authors " +\
        "of this bot.\n" +\
        "/distribute *<bikes> <docks>*: It will return the total cost " +\
        "of the transfer and the transportation with more cost."
    bot.send_message(chat_id=update.message.chat_id, parse_mode="Markdown",
                     text=message)


def hour_to_min(t):
    hour = int(t // 1)
    min = int(((t - hour) * 60) + 0.5)
    return hour, min


def graph(bot, update, user_data, args):
    if (args):
        try:
            dist = int(args[0])
        except ValueError:
            message = "Please enter an integer"
            bot.send_message(chat_id=update.message.chat_id,
                             text=message)
            return
        # we check if the arguments are correctly given
        if len(args) > 1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="It seems you have introduced more than one value, " +
                "so I'll just consider the first one.")
        if int(args[0]) >= 0:
            # we have concluded that the quadratic algorithm works better for
            # a distance 250 or less
            if int(args[0]) >= 250:
                G = d.CreateGraph(dist)
            else:
                G = d.Graph(dist)
            bot.send_message(chat_id=update.message.chat_id,
                             text="Graph created with distance " +
                             str(dist) + "!")
        # in case no arguments are given, the default distance is 1000
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Really? Negative distance?")

    # in case no arguments are given, the default distance is 1000
    else:
        G = d.CreateGraph()
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Since no distance was received, the graph by default, " +
            "which has been created, has distance 1000.")
    user_data['graph'] = G


def plotgraph(bot, update, user_data):
    filename = str(update.message.chat.username) + '.png'
    d.print_map(user_data['graph'], filename)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Creating the map...🚲🚲🚲🚲🚲")
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text="There you go!")
    os.remove(filename)

# 2 adresses given


def addressesTOcoordinates(addresses):
    geolocator = Nominatim(user_agent="bicing_bot")
    address1, address2 = addresses.split(',')
    location1 = geolocator.geocode(address1 + ', Barcelona')
    location2 = geolocator.geocode(address2 + ', Barcelona')
    return (location1.longitude,
            location1.latitude), (location2.longitude, location2.latitude)

# only 1 adress is given


def addressTOcoordinate(address):
    geolocator = Nominatim(user_agent="bicing_bot")
    location1 = geolocator.geocode(address + ', Barcelona')
    return (location1.longitude,
            location1.latitude)


def route(bot, update, args, user_data):
    error = False
    if args:
        filename = str(update.message.chat.username) + '_path.png'
        cami = " ".join(args)
        # if there is a , in the message, it gives 2 adresses
        if "," in cami:
            address1, address2 = cami.split(',')
            try:
                coord1, coord2 = addressesTOcoordinates(cami)
            except BaseException:
                bot.send_message(chat_id=update.message.chat_id,
                                 text="Unknown location.")
                return
            t = d.route(user_data['graph'], coord1, coord2, filename)
            hour, min = hour_to_min(t)
            message = "Going from " + address1 + " to" + address2 + \
                " will take you " + str(hour) + " hour(s) " + \
                str(min) + " min(s)."
        # only 1 adress given
        elif "," not in cami:
            if 'lat' in user_data:
                try:
                    coord2 = addressTOcoordinate(cami)
                except BaseException:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="Unknown location.")
                    return
                t = d.route(
                    user_data['graph'],
                    (user_data['lon'],
                     user_data['lat']),
                    coord2,
                    filename)
                hour, min = hour_to_min(t)
                message = "Going from your location to " + str(cami) + \
                    " will take you " + str(hour) + " hour(s) " + \
                    str(min) + " min(s)."
            else:
                message = "Please, either you give me an origin and a " +\
                    "destination"\
                    + " or you give me your location and a destination."
                error = True
        if not error:
            bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(filename, 'rb'))
            os.remove(filename)
    else:
        # no given arguments
        message = "No destination was given and, unfortunately, " +\
            "I've not been trained to guess it... yet.🤔"

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


def authors(bot, update):
    authors = d.authors()
    bot.send_message(chat_id=update.message.chat_id, parse_mode="Markdown",
                     text=str(authors))


def distribute(bot, update, args, user_data):
    if not args:
        # no arguments given
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Oh, no! No conditions were given... Do not try to bug me.😏")
        return
    if len(args) == 1:
        # more values than necessary
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Please introduce 2 numbers")
        return
    try:
        valor1 = int(args[0])
        valor2 = int(args[1])
    except ValueError:
        message = "Please enter integers"
        bot.send_message(chat_id=update.message.chat_id,
                         text=message)
        return
    if len(args) > 2:
        # more values than necessary
        bot.send_message(
            chat_id=update.message.chat_id,
            text="It seems you have introduced more than two values, " +
            "so I'll just consider the first two.")
    requiredBikes, requiredDocks = valor1, valor2
    if (requiredBikes < 0 or requiredDocks < 0):
        # invalid arguments
        bot.send_message(chat_id=update.message.chat_id,
                         text="Are you kidding? Values can't be negative!")
    else:
        message = "Let's see what I can do, I can't promise anything...\n" +\
            "Computing the distribution needed to satisfy " +\
            "the conditions..."
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(message))
        try:
            flowCost, aresta1, aresta2, bikes, dist = d.bicing_flow(
                user_data['graph'], requiredBikes, requiredDocks)
        except BaseException:
            # no solution found
            bot.send_message(chat_id=update.message.chat_id,
                             text="I warned you... I 'm not good at this.")
            return

        tcost = "In order to guarantee, at least, " + str(requiredBikes) +\
            " bikes and " \
            + str(requiredDocks) + " docks at every station, a " +\
            "total distance of  " + str(flowCost / 1000) + " km of " \
            + "transportations will be necessary."
        mcost = "The transfer with the highest cost (distance * bikes) will "\
            + "be from station " + str(aresta1) + " to station " \
            + str(aresta2) + ". The number of bikes will be " + \
            str(bikes) + " and the distance " + str(dist) + " m."
        bot.send_message(chat_id=update.message.chat_id, text=str(tcost))
        bot.send_message(chat_id=update.message.chat_id, text=str(mcost))

# unrecognized command


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry! I can't deal with that.")

# save the currently location


def where(bot, update, user_data):
    user_data['lat'], user_data['lon'] = update.message.location.latitude, \
        update.message.location.longitude
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Your coordinates are %f %f' % (user_data['lat'],
                                             user_data['lon']))


updater = Updater(token='682625912:AAF9lZUU8IKvHQj6nGPwmLVweq2kT0hSfL0')
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'graph', graph, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler(
    'plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'route', route, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler(
    'components', connectivity, pass_user_data=True))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler(
    'distribute', distribute, pass_args=True, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(
    Filters.location, where, pass_user_data=True))


updater.start_polling()
