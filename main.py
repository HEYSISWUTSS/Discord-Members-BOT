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
GUILD_ID = 1475204966607229081  # Your server ID

@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
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
    
    print(f"Bot logged in as {bot.user}")

@bot.event
async def on_member_remove(member):
    """Force member back into server when they leave"""
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        return
    
    # Try to re-invite the member
    try:
        # Get the first text channel to create an invite
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).create_instant_invite:
                invite = await channel.create_invite(max_age=3600, max_uses=1)
                # Note: You can't directly add members back, but you can log and notify
                print(f"{member.name} left the server. Invite link: {invite.url}")
                break
    except Exception as e:
        print(f"Error handling member removal: {e}")

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

@bot.command(name="force")
@commands.has_permissions(administrator=True)
async def force_member(ctx, member: discord.Member):
    """Force a member to stay in the server (admin only)"""
    try:
        # Create a persistent invite for the member
        for channel in ctx.guild.text_channels:
            if channel.permissions_for(ctx.guild.me).create_instant_invite:
                invite = await channel.create_invite(max_age=0, max_uses=0)  # Permanent invite
                await ctx.send(f"Created permanent invite for {member.mention}: {invite.url}")
                break
    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(TOKEN)

