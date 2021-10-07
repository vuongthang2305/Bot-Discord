import discord
from discord import File, Member,ClientUser
from discord.ext import commands
from discord.ext.commands.core import check
from pytube import YouTube
from easy_pil import Canvas, Editor, Font, load_image_async
import os
import sqlite3 as lite
import sys
from . import config
from discord.player import FFmpegPCMAudio

TOKEN = 'ODg0NzQzMzA5MjIwNzk0NDI5.YTc7ag.D7Mac5y1rj2sHABE4yU_wdlZWUU'

bot = commands.Bot(command_prefix = '.')
exp_collect = 20


def insert(query):
    con = None
    path = os.path.dirname(__file__) + "\\database\\dbuser.db"
    con = lite.connect(path)
    with con:

        
        cur = con.cursor()    
        cur.execute(query)


def select(query):
    con = None
    
    try:
        path = os.path.dirname(__file__) + "\\database\\dbuser.db"
        con = lite.connect(path)
        
        cur = con.cursor()    
        cur.execute(query)
        while True:
        
            data = cur.fetchone()
            if data == None:
                return None
            return data
    except lite.Error as e:
        print ("Error %s:" % e.args[0])
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()


def update(query):
    path = os.path.dirname(__file__) + "\\database\\dbuser.db"
    con = lite.connect(path) 
    
    with con:
        cur = con.cursor()    
    
        cur.execute(query)        
        con.commit()


@bot.event
async def on_ready():
    print('I logged in as {0.user}'.format(bot))

@bot.event
async def on_message(ctx):
    id = str(ctx.author).split('#')[1]
    data = select(f'SELECT * FROM USER WHERE id = {id}')
    if data != None:
        id_db = data[0]
        level = data[1]
        exp = data[2]
        print(id_db, level, exp)

        if int(id) == id_db:
            if id == config.id_admin:
                exp += config.exp_admin
                update(f'UPDATE USER SET exp = {exp} WHERE id = {id}') # exp admin
            else:
                exp += config.exp_colect
                update(f'UPDATE USER SET exp = {exp} WHERE id = {id}') # exp cộng thêm
            if exp >= level * config.exp_need:
                while True:
                    level += 1
                    update(f'UPDATE USER SET level = {level} WHERE id = {id}')
                    expex = exp - (level - 1) * 100 # tính exp thừa
                    update(f'UPDATE USER SET exp = {expex} WHERE id = {id}')
                    if exp <= level * 100 or exp == 0:
                        break
                await ctx.channel.send(f"Chúc mừng bé `{str(ctx.author.nick)}` đã lên level {level} nói nhiều lên để được lên cấp tiếp nhé")
    else:
        if id != '7964':
            insert(f'INSERT INTO USER VALUES({id},1,1,)')
            await ctx.channel.send(f"Chào mừng bé `{str(ctx.author.nick)}` đã đến nơi hội tụ các con nghiện tương tác để lên cấp nhóe!")
    await bot.process_commands(ctx)

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


@bot.command(pass_context=True)
async def rank(cxt):
    
    id = str(cxt.author).split('#')[1]
    data = select(f'SELECT * FROM USER WHERE id = {id}')
    level = data[1]
    exp = data[2]

    next_level_xp = level * 100
    current_level_xp = exp
    xp_per_cent = current_level_xp / next_level_xp * 100
    width =  300 * xp_per_cent / 100

    username = str(cxt.author.nick)
    
    background = Editor("./img/bg1.jpg").resize((600,300))
    profile = await load_image_async(str(cxt.author.avatar_url)) # lấy avr
    fontname = Font('font11.ttf', size=23)
    fontlv = Font('font11.ttf', size=20)
    profile = Editor(profile).resize((130, 130)).circle_image()

    square = Canvas((500,500), "#06FFBF")
    square = Editor(square)
    square.rotate(30, expand=True)

    background.rectangle((100, 150), width=600, height=2, fill="#17F3F6")

    # exp bar
    background.rectangle((120, 220), width=300, height=25, fill="#17F3F6", radius=10)
    background.rectangle((120, 220), width=width, height=25, fill="#BD1536", radius=10)

    background.paste(square.image, (350,-300))

    # avt
    background.paste(profile.image, (0,0))

    txt_name = background.text((155,100), f'{username}#{id}', font=fontname, color='#FFF')
    txt_exp = background.text((165,175), f'Level: {level} EXP: {exp}/{next_level_xp}', font=fontlv, color='#51E4E4')

    file = File(fp=background.image_bytes, filename='card.png')
    await cxt.send(file = file)

@bot.command(pass_context=True)
async def test(ctx):
    ctx.author.mention()

bot.run(TOKEN)