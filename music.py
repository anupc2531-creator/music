import os
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("8902670600:AAHwAIFfcrVPaYsv5uB5N6kBRXku3UHu3oY")

songs = {}
votes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Music Voting Bot\n\n"
        "/play Song Name - song request\n"
        "/queue - requests dekho"
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Example: /play Tum Hi Ho"
        )
        return

    name = " ".join(context.args)
    song_id = str(len(songs) + 1)

    songs[song_id] = name
    votes[song_id] = set()

    keyboard = [[
        InlineKeyboardButton(
            "👍 Vote (0)",
            callback_data=f"vote:{song_id}"
        )
    ]]

    await update.message.reply_text(
        f"🎵 Song request: {name}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, song_id = query.data.split(":", 1)

    if song_id not in songs:
        await query.edit_message_text("Song request nahi mila.")
        return

    user_id = query.from_user.id
    voters = votes[song_id]

    if user_id in voters:
        voters.remove(user_id)
    else:
        voters.add(user_id)

    keyboard = [[
        InlineKeyboardButton(
            f"👍 Vote ({len(voters)})",
            callback_data=f"vote:{song_id}"
        )
    ]]

    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not songs:
        await update.message.reply_text("Queue khaali hai.")
        return

    ordered = sorted(
        songs.items(),
        key=lambda item: len(votes[item[0]]),
        reverse=True
    )

    text = "🎶 Music Queue\n\n"
    for song_id, name in ordered:
        text += f"{name} — {len(votes[song_id])} votes\n"

    await update.message.reply_text(text)

def main():
    if not TOKEN:
        raise RuntimeError("8902670600:AAHwAIFfcrVPaYsv5uB5N6kBRXku3UHu3oY")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("queue", queue))
    app.add_handler(CallbackQueryHandler(vote, pattern=r"^vote:"))

    app.run_polling()

if __name__ == "__main__":
    main()
