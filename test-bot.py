import discord
import string
import random
import os
import sys


from discord.ext import commands
from discord import FFmpegPCMAudio


client = commands.Bot(command_prefix = 't!')
client.remove_command('help')

players = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Zeus Cuz he pro"))
    print(f'\nLogged in as {client.user.name}#{client.user.discriminator}, User ID: {client.user.id}, Version: {discord.__version__}\n')

@client.event
async def on_member_join(member):
    print(f'{member}has joined a server.')

@client.event
async def on_member_leave(member):
    print(f'{member}has leaved the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 10000)} ms')

@client.command(aliases=['ask', 'question'])
async def _8ball(ctx, *, question):
    responses = ['u suck lol', 'maybe', 'ew no', 'yes u pro', 'yes bug is bobo']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} message has been purged!')

@ client.command(aliases=['Kick','KICK','KIck'])
@ commands.has_permissions(kick_members=True)
@commands.has_any_role('Pro Nuker', 'BOTS')
async def kick(ctx, user: discord.Member):
    if user == None or user == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself!")
        return
    await ctx.send(str(user.name)+" has been kicked from the server!")
    await user.kick()

@client.command(aliases=['BAn','BaN','BAN','Ban'])
@commands.has_permissions(ban_members=True)
@commands.has_any_role('Pro Nuker', 'BOTS')
async def ban(ctx, user: discord.Member):
    if user == None or user == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself!")
        return
    await ctx.send(str(user.name)+" has been banned from the server!")
    await user.ban()

@client.command(aliases=['unBan','UNBan','UNBAN','UnbaN'])
@commands.has_permissions(manage_roles=True)
@commands.has_any_role('Pro Nuker','BOTS')
async def unban(ctx, user: discord.Member):
    await ctx.send(str(user.name)+" has been unbanned from the server")
    await user.unban()

@client.command()
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))

    embed.add_field(name="Bot", value=member.bot)

    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member : discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            await ctx.send("{} has been has been muted!" .format(member.mention,ctx.author.mention))

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            await ctx.send("{} has been has been unmuted!".format(member.mention, ctx.author.mention))

@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='t!ping', value='Returns Pong!', inline=False)
    embed.add_field(name='t!userinfo', value='It gives the info of the specific user', inline=False)
    embed.add_field(name='t!ask', value='Ask anything!', inline=False)


    await ctx.send(embed=embed)
    
@client.command(pass_contex=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command(pass_contex=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start    


client.run('NzA3MDU2NTgzMDAzMDc4Nzg3.XrZBOQ.RLAcA9srlJLdREgYXddl0gBbOoU')
