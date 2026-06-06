import os
import discord
from discord.ext import commands

# Define all intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize the bot with command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ.get("TOKEN", "your_bot_token_here")
GUILD_ID = 1475204966607229081


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    print(f"Connected to guild: {GUILD_ID}")


@bot.command(name="pull")
async def pull(ctx, guild_id: int = None):
    """Pull all members from a guild"""
    if guild_id is None:
        guild_id = GUILD_ID
    
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"❌ Unable to find guild with ID: {guild_id}")
        return
    
    await ctx.send(f"📥 Pulling members from guild {guild_id}...")
    
    members = []
    async for member in guild.fetch_members(limit=None):
        members.append(member)
    
    await ctx.send(f"✅ Successfully pulled {len(members)} members from {guild.name}")
    
    # Print member list
    member_list = "\n".join([f"  • {member.name}" for member in members[:10]])
    if len(members) > 10:
        member_list += f"\n  ... and {len(members) - 10} more"
    
    await ctx.send(f"```\n{member_list}\n```")


@bot.command(name="auth")
async def auth(ctx):
    """Check bot authentication status"""
    await ctx.send(f"✅ Bot is authenticated as **{bot.user}**\n🔐 Token is valid and active")


bot.run(TOKEN)

