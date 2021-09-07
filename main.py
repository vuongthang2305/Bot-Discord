import discord
from discord.ext import commands
from pytube import YouTube
import os
from discord.player import FFmpegPCMAudio

TOKEN = 'ODg0NzQzMzA5MjIwNzk0NDI5.YTc7ag.8CWkysbkYSqeWlH7M4ooJ8qu-MU'

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('I logged in as {0.user}'.format(bot))


@bot.command(pass_context=True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
    else: await ctx.send('Đang trong phòng rồi ạ')

@bot.command(pass_context=True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else: await ctx.send('Ơ kìa e có trong phòng đâu')

@bot.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('Có cái méo gì mà dừng')

@bot.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Ngáo à có gì đâu mà resume')

@bot.command(pass_context=True)
async def play(ctx,url):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        if os.path.isfile("1.mp3") == True:
            os.remove('1.mp3')
        dl(url)
        sc = FFmpegPCMAudio('1.mp3')
        voice.play(sc)

def dl(url):
    # url input from user
    yt = YouTube(url)
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='./audio/')
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = '1' + '.mp3'
    os.rename(out_file, new_file)
bot.run(TOKEN)