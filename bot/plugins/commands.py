from hydrogram import filters
from hydrogram.types import Message
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user

from hydrogram.errors import (
    PeerIdInvalid, FloodWait, ChatWriteForbidden,
    UserDeactivated, RPCError
)

from bot.plugins.db import add_user, get_all_users, remove_user

import asyncio

# ADD USER + START COMMAND
@TelegramBot.on_message(filters.command(['start', 'help']) & filters.private)
@verify_user
async def start_command(_, msg: Message):

    user_id = msg.from_user.id
    name = msg.from_user.first_name

    # Save user (no duplicates)
    new = add_user(user_id, name)

    # Send new user log
    if new:
        await TelegramBot.send_message(
            Telegram.CHANNEL_ID,
            f"🔔 New User Joined in File2Link\n"
            f"👤 Name: `{name}`\n"
            f"🆔 ID: `{user_id}`"
        )

    await msg.reply(
        text=WelcomeText % {'first_name': name},
        quote=True
    )



# PRIVACY COMMAND
@TelegramBot.on_message(filters.command('privacy') & filters.private)
@verify_user
async def privacy_command(_, msg: Message):
    await msg.reply(text=PrivacyText, quote=True, disable_web_page_preview=True)



# LOG COMMAND
@TelegramBot.on_message(filters.command('log') & filters.chat(Telegram.OWNER_ID))
async def log_command(_, msg: Message):
    await msg.reply_document('event-log.txt', quote=True)


@TelegramBot.on_message(filters.command("broadcast") & filters.user(Telegram.OWNER_ID))
async def broadcast_command(_, msg: Message):

    if len(msg.text.split()) < 2:
        return await msg.reply("❗ Usage: `/broadcast your message`")

    text = msg.text.split(" ", 1)[1]

    users = get_all_users()
    sent = 0
    failed = 0
    removed = 0

    await msg.reply("📢 Broadcast Started...")

    for user in users:
        uid = user["_id"]

        try:
            await TelegramBot.send_message(uid, text)
            sent += 1
            await asyncio.sleep(0.1)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except (PeerIdInvalid, ChatWriteForbidden, UserDeactivated):
            remove_user(uid)        # <── AUTO REMOVE USER
            removed += 1
            failed += 1

        except RPCError:
            failed += 1

    await msg.reply(
        f"📣 **Broadcast Completed**\n"
        f"✅ Sent: `{sent}`\n"
        f"❌ Failed: `{failed}`\n"
        f"🗑 Removed Blocked Users: `{removed}`"
    )