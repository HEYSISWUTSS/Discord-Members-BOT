import os
import discord
from discord.ext import commands
from cachetools import TTLCache
import asyncio

# Define all intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize the bot with command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

member_cache = TTLCache(maxsize=1, ttl=300)  # Cache for 5 minutes

TOKEN = os.environ.get("TOKEN", "your_bot_token_here")

@bot.event
async def on_ready():
    guild = bot.get_guild(1475204966607229081)  # Your server ID
    if guild is None:
        print("Unable to find guild.")
        return

    if 'members' not in member_cache:
        members = []
        async for member in guild.fetch_members(limit=None):
            members.append(member)
        member_cache['members'] = members

    for member in member_cache['members']:
        print(member.name)

@bot.command(name="members")
async def list_members(ctx):
    """List all members in the server"""
    if 'members' in member_cache:
        members = member_cache['members']
        member_list = "\n".join([m.name for m in members])
        await ctx.send(f"**Members ({len(members)}):**\n{member_list}")
    else:
        await ctx.send("No members cached yet.")

@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

bot.run(TOKEN)

