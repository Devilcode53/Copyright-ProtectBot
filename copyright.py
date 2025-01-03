import os
import re
import sys
import time
import datetime
import random 
import asyncio
from pytz import timezone
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.raw.types import UpdateEditMessage, UpdateEditChannelMessage
import traceback

from apscheduler.schedulers.background import BackgroundScheduler

API_ID = 24727770
API_HASH = "b29e54a12450d2bf91e23b5d90d5378e"
BOT_TOKEN = "7507526474:AAH7fK6DF80YtyubDQx49ES4-3QmtqxRpUw"
DEVS = [7526005252, 7401546867, 6323813930]
BOT_USERNAME = "copyright_safebot"  # Change your bot username without @

ALL_GROUPS = []
TOTAL_USERS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}

DELETE_MESSAGE = [
    "1 Hour complete, I'm doing my work...",
    "Its time to delete all medias!",
    "No one can Copyright until I'm alive 😤",
    "Hue hue, let's delete media...",
    "I'm here to delete medias 🙋", 
    "😮‍💨 Finally I delete medias",
    "Great work done by me 🥲",
    "All media cleared!",
    "hue hue medias deleted by me 😮‍💨",
    "medias....",
    "it's hard to delete all medias 🙄",
]

START_MESSAGE = """
**Hello {}, I'm Anti - CopyRight Bot**

 > **I can save your groups from Copyrights 😉**

 **Work:** I'll Delete all medias of your group in every 1 hour ➰
 
 **Process?:** Simply add me in your group and promote as admin with delete messages right!
"""

BUTTON = [
    [InlineKeyboardButton("+ Add me in group +", url=f"http://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages")],
    [InlineKeyboardButton("Owner", url="https://t.me/japu7")]  # Replace with your actual username
]

bot = Client('bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_user(user_id):
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)

@bot.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
    start = datetime.datetime.now()
    add_user(e.from_user.id)
    rep = await e.reply_text("**Pong !!**")
    end = datetime.datetime.now()
    ms = (end-start).microseconds / 1000
    await rep.edit_text(f"🤖 **PONG**: {ms}ᴍs")

@bot.on_message(filters.command(["help", "start"]))
async def start_message(_, message: Message):
    add_user(message.from_user.id)
    await message.reply(START_MESSAGE.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(BUTTON))

@bot.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
    await e.reply("**Restarting.....**")
    try:
        await bot.stop()
    except Exception:
        pass
    args = [sys.executable, "copyright.py"]
    os.execl(sys.executable, *args)
    quit()

@bot.on_message(filters.user(DEVS) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
    wait = await message.reply("Fetching.....")
    stats = "**Here is total stats of me!** \n\n"
    stats += f"Total Chats: {len(ALL_GROUPS)} \n"
    stats += f"Total users: {len(TOTAL_USERS)} \n"
    stats += f"Disabled chats: {len(DISABLE_CHATS)} \n"
    stats += f"Total Media active chats: {len(MEDIA_GROUPS)} \n\n"
    await wait.edit_text(stats)

@bot.on_message(filters.command(["anticopyright", "copyright"]))
async def enable_disable(bot: bot, message: Message):
    chat = message.chat
    if chat.id == message.from_user.id:
        await message.reply("Use this command in group!")
        return
    txt = ' '.join(message.command[1:])
    if txt:
        member = await bot.get_chat_member(chat.id, message.from_user.id)
        if re.search("on|yes|enable".lower(), txt.lower()):
            if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
                if chat.id in DISABLE_CHATS:
                    await message.reply(f"Enabled anti-copyright! for {chat.title}")
                    DISABLE_CHATS.remove(chat.id)
                    return
                await message.reply("Already enabled!")
        elif re.search("no|off|disable".lower(), txt.lower()):
            if member.status == ChatMemberStatus.OWNER or member.user.id in DEVS:
                if chat.id in DISABLE_CHATS:
                    await message.reply("Already disabled!")
                    return
                DISABLE_CHATS.append(chat.id)
                if chat.id in MEDIA_GROUPS:
                    MEDIA_GROUPS.remove(chat.id)
                await message.reply(f"Disable Anti-CopyRight for {chat.title}!")
            else:
                await message.reply("Only chat Owner can disable anti-copyright!")
                return 
        else:
            if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
                if chat.id in DISABLE_CHATS:
                    await message.reply("Anti-Copyright is disable for this chat! \n\ntype /anticopyright enable to enable Anti-CopyRight")
                else:
                    await message.reply("Anti-Copyright is enable for this chat! \n\ntype /anticopyright disable to disable Anti-CopyRight")
    else:
        if chat.id in DISABLE_CHATS:
            await message.reply("Anti-Copyright is disable for this chat! \n\ntype /anticopyright enable to enable Anti-CopyRight")
        else:
            await message.reply("Anti-Copyright is enable for this chat! \n\ntype /anticopyright disable to disable Anti-CopyRight")

@bot.on_message(filters.all & filters.group)
async def watcher(_, message: Message):
    chat = message.chat
    user_id = message.from_user.id
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if chat.id not in ALL_GROUPS:
            ALL_GROUPS.append(chat.id)
        if chat.id in DISABLE_CHATS:
            return
        if chat.id not in MEDIA_GROUPS:
            if chat.id in DISABLE_CHATS:
                return
            MEDIA_GROUPS.append(chat.id)
        if (message.video or message.photo or message.animation or message.document):
            check = GROUP_MEDIAS.get(chat.id)
            if check:
                GROUP_MEDIAS[chat.id].append(message.id)
                print(f"Chat: {chat.title}, message ID: {message.id}")
            else:
                GROUP_MEDIAS[chat.id] = [message.id]
                print(f"Chat: {chat.title}, message ID: {message.id}")

import random

from pyrogram import Client
import random
import traceback

from pyrogram.raw.types import UpdateEditMessage, UpdateEditChannelMessage
from pyrogram.errors import UserNotParticipant

@bot.on_raw_update(group=-1)
async def better(client, update, _, __):
    if isinstance(update, UpdateEditMessage) or isinstance(update, UpdateEditChannelMessage):
        e = update.message
        try:
            if not getattr(e, 'edit_hide', False):      
                user_id = e.from_id.user_id
                if user_id in DEVS:
                    return

                chat_id = e.peer_id.channel_id

                # Check if the user is an admin or owner
                try:
                    participants = await client.get_chat_members(chat_id)
                    is_admin_or_owner = any(member.user.id == user_id and (member.status == 'administrator' or member.status == 'creator') for member in participants)
                except UserNotParticipant:
                    is_admin_or_owner = False

                if is_admin_or_owner:
                    return  # Do not delete the message if the user is an admin or owner

                await client.delete_messages(chat_id=chat_id, message_ids=e.id)

                user = await client.get_users(e.from_id.user_id)

                await client.send_message(
                    chat_id=chat_id,
                    text=f"{user.mention} just edited a message, and I deleted it 🐸."
                )
        except Exception as ex:
            print("Error occurred:", traceback.format_exc())


def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
       return

    for i in MEDIA_GROUPS:
       if i in DISABLE_CHATS:
         return
       message_list = list(GROUP_MEDIAS.get(i))
       try:
          hue = bot.send_message(i, random.choice(DELETE_MESSAGE))
          bot.delete_messages(i, message_list, revoke=True)
          time.sleep(1)
          hue.delete()
          GROUP_MEDIAS[i].delete()
          gue = bot.send_message(i, text="Deleted All Media's")
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all medias ✓")
    print("waiting for 1 hour")

scheduler = BackgroundScheduler(timezone=timezone('Asia/Kolkata'))
scheduler.add_job(AutoDelete, "interval", seconds=3600)
scheduler.start()

from pyrogram import Client, filters
from pyrogram.types import Message

@bot.on_message(filters.user(DEVS) & filters.command(["broadcast"]))
async def broadcast(_, message: Message):
    # Ensure that the message has content to broadcast
    if len(message.command) < 2:
        await message.reply("Please provide a message to broadcast.")
        return

    # The message text is everything after the /broadcast command
    broadcast_message = " ".join(message.command[1:])
    
    # Check if the message is a reply and get the original message
    if message.reply_to_message:
        replied_message = message.reply_to_message
        try:
            # Check if the replied message is a media, file, or simple text
            if replied_message.text:
                broadcast_message = replied_message.text  # For text message
            elif replied_message.audio or replied_message.document or replied_message.video:
                # For media or file (audio, video, document)
                broadcast_message = replied_message
            elif replied_message.photo:
                # For images
                broadcast_message = replied_message.photo
            else:
                # Handle other types of content, if necessary
                broadcast_message = "Cannot broadcast this content type."
        except Exception as e:
            print(f"Error handling replied message: {e}")

    # Send the message to all groups where the bot is added
    for group_id in ALL_GROUPS:
        try:
            if isinstance(broadcast_message, str):
                await bot.send_message(group_id, broadcast_message)
            elif isinstance(broadcast_message, Message):
                if broadcast_message.text:
                    await bot.send_message(group_id, broadcast_message.text)
                elif broadcast_message.photo:
                    await bot.send_photo(group_id, broadcast_message.photo.file_id)
                elif broadcast_message.audio:
                    await bot.send_audio(group_id, broadcast_message.audio.file_id)
                elif broadcast_message.document:
                    await bot.send_document(group_id, broadcast_message.document.file_id)
                elif broadcast_message.video:
                    await bot.send_video(group_id, broadcast_message.video.file_id)
            else:
                await bot.send_message(group_id, "Unable to broadcast this content.")
        except Exception as e:
            print(f"Failed to send broadcast to group {group_id}: {e}")

    # Send the message to all users who have interacted with the bot
    for user_id in TOTAL_USERS:
        try:
            if isinstance(broadcast_message, str):
                await bot.send_message(user_id, broadcast_message)
            elif isinstance(broadcast_message, Message):
                if broadcast_message.text:
                    await bot.send_message(user_id, broadcast_message.text)
                elif broadcast_message.photo:
                    await bot.send_photo(user_id, broadcast_message.photo.file_id)
                elif broadcast_message.audio:
                    await bot.send_audio(user_id, broadcast_message.audio.file_id)
                elif broadcast_message.document:
                    await bot.send_document(user_id, broadcast_message.document.file_id)
                elif broadcast_message.video:
                    await bot.send_video(user_id, broadcast_message.video.file_id)
            else:
                await bot.send_message(user_id, "Unable to broadcast this content.")
        except Exception as e:
            print(f"Failed to send broadcast to user {user_id}: {e}")

    await message.reply("Broadcast message sent to all users and groups!")

def starter():
    print('Starting Bot...')
    bot.start()
    print('Bot Started ✓')
    idle()

if __name__ == "__main__":
    starter()
