import os
import discord
import asyncio
import aiosqlite
from dotenv import load_dotenv
from agent.agent_service import ModerationAgent

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = "warnings.db"

# Check if token is available
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required. Please set it in your .env file.")

# Initialize SQLite database and warnings table (scoped by guild)
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id  TEXT NOT NULL,
                guild_id TEXT NOT NULL,
                count    INTEGER NOT NULL,
                PRIMARY KEY (user_id, guild_id)
            );
        """)
        await db.commit()

# Bootstrap DB before running the bot
asyncio.get_event_loop().run_until_complete(init_db())

# Discord client setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
agent = ModerationAgent()

# Helpers for warning counts
async def increment_warning(user_id: str, guild_id: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT count FROM warnings WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        )
        row = await cursor.fetchone()

        if row is None:
            count = 1
            await db.execute(
                "INSERT INTO warnings (user_id, guild_id, count) VALUES (?, ?, ?)",
                (user_id, guild_id, count)
            )
        else:
            count = row[0] + 1
            await db.execute(
                "UPDATE warnings SET count = ? WHERE user_id = ? AND guild_id = ?",
                (count, user_id, guild_id)
            )

        await db.commit()
        return count

async def reset_warnings(user_id: str, guild_id: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM warnings WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        )
        await db.commit()

# Event handlers
@client.event
async def on_ready():
    print(f"🤖 Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user or not message.guild:
        return

    text     = message.content
    user_id  = str(message.author.id)
    guild_id = str(message.guild.id)
    print(f"📩 ({message.guild.name}) {message.author}: {text}")

    # Command to update moderation rules
    if text.startswith("!update_rules "):
        rules_text = text[len("!update_rules "):]
        agent.update_rules_text(rules_text)
        await message.channel.send("✅ Rules updated.")
        return

    # Ask agent for action
    action = agent.moderate_message(text)

    # Handle warning
    if action == "Warn":
        new_count = await increment_warning(user_id, guild_id)
        await message.channel.send(f"⚠️ Warning {new_count}/3")
        # Ban and reset if over threshold
        if new_count >= 3:
            await message.channel.send(f"🚫 {message.author.mention} banned.")
            await message.author.ban(reason="Exceeded warning limit")
            await reset_warnings(user_id, guild_id)
        return

    # Handle delete
    if action == "Delete":
        await message.delete()
        await message.channel.send("Message deleted")
        return

    # Handle immediate ban
    if action == "Ban":
        await message.channel.send(f"🚫 {message.author.mention} banned.")
        await message.author.ban(reason="Violation of rules")
        await reset_warnings(user_id, guild_id)
        return

    # OK → do nothing

# Run the bot
client.run(TOKEN)
