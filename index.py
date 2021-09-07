import discord
import time
TOKEN = 'ODg0ODA1MjA4OTU2MzU0NTcw.YTd1EA.8IYjKju4ag9HubbLXHfnNrivlzM'

client = discord.Client()

@client.event
async def on_ready():
    print('I logged in as {0.user}'.format(client))

@client.event
async def on_message(ctx):
    username = str(ctx.author).split('#')[0]
    user_mess = str(ctx.content)
    channel = str(ctx.channel.name)
    print(f'{username}: {user_mess} {channel}')

    
    if user_mess.lower() == "hello":
        await ctx.channel.send(f'Hello {username} lắm trò hê lô he lủng')
        return
    elif user_mess.lower() == 'chào' or user_mess.lower() == 'xin chào':
        await ctx.channel.send(f'Dạ con chào bố `{username}` ')
        return
    
client.run(TOKEN)