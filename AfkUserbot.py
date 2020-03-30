"""
Edit This
"""
apiId =
apiHash = ""

"""
Afk message. {original_msg} is the text
of message sent by the user
"""
afkMessage = ""



"""
Boring stuff
"""

from pyrogram import Client, Filters
import time
from pyrogram.errors import *
from threading import Timer,Thread
import uuid
from subprocess import Popen,PIPE
from pyrogram.api import functions

users = {}
afk = False
accepted_users = []
banned_users = []
bot = Client(
    "UserbotAfk",
    api_id=apiId,
    api_hash=apiHash)


@bot.on_message(Filters.private)
def check_saved(Client, msg):
    global users
    if not msg.from_user.id in users:
        users[msg.from_user.id] = 0
    msg.continue_propagation()


@bot.on_message(Filters.private & ~Filters.user("self"))
def logger(Client, msg):
    print("[PM] Got a new message from: {}. Text: {}".format(
        "@" + msg.from_user.username if msg.from_user.username else msg.from_user.first_name,
        str(msg.text)[0:20]))
    msg.continue_propagation()


@bot.on_message(Filters.user("self") & Filters.command("afk", prefixes=[".", "/", "!", "#"]))
def afk_command(Client, msg):
    global afk
    global accepted_users
    accepted_users = []
    if len(msg.command) == 1:
        msg.edit_text("You are afk" if afk else "You are not afk")
    else:
        if msg.command[1] == "on":
            afk = True
            msg.edit_text("Afk enabled.")
        elif msg.command[1] == "off":
            afk = False
            msg.edit_text("Afk disabled.")
        elif msg.command[1] == "on":
            afk = True
            msg.edit_text("La modalità AFK è stata resettata.")
        else:
            msg.edit_text("You are afk" if afk else "You are not afk")



@bot.on_message(Filters.user("self") & Filters.command("online","."))
def on_user(client, message):
    msg = message
    chat_id = msg.chat.id
    first_name = msg.from_user.first_name
    user = msg.from_userfirst_name if not msg.from_user.username else msg.from_user.username
    client.send(functions.account.UpdateProfile(last_name="✅𝕆ℕ𝕃𝕀ℕ𝔼✅"))
    try:
      bot.send_message(chat_id,"Il tuo stato ora è ✅ONLINE")
    except FloodWait as fw:
       time.sleep(fw.x)
    try:
       msg.delete()
    except RPCError:
       pass

@bot.on_message(Filters.user("self") & Filters.command("offline","."))
def off_user(client, message):
    msg = message
    first_name = msg.from_user.first_name
    chat_id = msg.chat.id
    user = msg.from_userfirst_name if not msg.from_user.username else msg.from_user.username
    client.send(functions.account.UpdateProfile(last_name=" ⛔️𝕆𝔽𝔽𝕃𝕀ℕ𝔼⛔️"))
    try:
      bot.send_message(chat_id,"Il tuo stato ora è 🚫OFFLINE")
    except FloodWait as fw:
       time.sleep(fw.x)
    try:
       msg.delete()
    except RPCError:
       pass


@bot.on_message(Filters.user("self") & Filters.command("accept", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global accepted_users
    accepted_users.append(msg.chat.id)
    msg.edit_text("Accepted {}.")


@
@bot.on_message(Filters.user("self") & Filters.command("ban", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global banned_users
    banned_users.append(msg.chat.id)
    if msg.chat.id in accepted_users: accepted_users.remove(accepted_users)
    msg.edit_text("Banned {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("unaccept", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global accepted_users
    accepted_users.remove(msg.chat.id)
    msg.edit_text("Removed {} from accepted list.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("unban", prefixes=[".", "/", "!", "#"]))
def accept_command(Client, msg):
    global banned_users
    banned_users.remove(msg.chat.id)
    if msg.chat.id in accepted_users: accepted_users.remove(accepted_users)
    msg.edit_text("Unbanned {}.".format(msg.chat.first_name))


@bot.on_message(Filters.user("self") & Filters.command("commands", prefixes=[".", "/", "!", "#"]))
def commands_command(Client, msg):
    msg.edit_text("Avaiable Commands:\n"
                  "/afk - see if you are afk\n"
                  "/afk on - turn on afk\n"
                  "/afk off - turn off afk\n"
                  "/accept - in private, this person can now talk as much as he wants\n"
                  "/ban - in private, every message will be deleted and he'll not get any answer\n"
                  "\n"
                  "Prefixes: . / ! #")


@bot.on_message(Filters.private & ~Filters.user("self"))
def on_private_afk_message(Client, msg):
    global accepted_users
    if not msg.from_user.id in accepted_users and afk:
            if users[msg.from_user.id] + 0 < int(time.time()) and not msg.from_user.id in banned_users:
                bot.send_message(msg.chat.id,
                                 afkMessage.replace("{original_msg}", str(msg.text)),
                                 disable_web_page_preview=True)
                users[msg.from_user.id] = int(time.time())
    accepted_users.append(msg.from_user.id)


bot.run()
