from PIL.Image import TRANSPOSE, frombuffer
import discord
from discord import File
from discord import user
from discord.ext import commands
from discord.ext.commands.core import check
from pytube import YouTube
from easy_pil import Canvas, Editor, Font, load_image_async
import os
import sqlite3 as lite
import sys
import datetime
import config

from discord.player import FFmpegPCMAudio
TOKEN = 'ODg0NzQzMzA5MjIwNzk0NDI5.YTc7ag.D7Mac5y1rj2sHABE4yU_wdlZWUU'


bot = commands.Bot(command_prefix = '.')
bot.lava_nodes = [{
    'host': 'lava.link',
    'port': 80,
    'rest_uri':f'http://lava.link:80',
    'identifier':'MAIN',
    'password':'anything',
    'region':'vietnam'
}]


def insert(query):
    con = None
    path = os.path.dirname(__file__) + "\\database\\dbuser.db"
    con = lite.connect(path)
    with con:

        cur = con.cursor()    
        cur.execute(query)

def selectall(query):
    con = None
    
    try:
        path = os.path.dirname(__file__) + "\\database\\dbuser.db"
        con = lite.connect(path)
        
        cur = con.cursor()    
        cur.execute(query)
        while True:
        
            data = cur.fetchall()
            if data == None:
                return None
            return data
    except lite.Error as e:
        print ("Error %s:" % e.args[0])
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()

def select(query):
    con = None
    
    try:
        path = os.path.dirname(__file__) + "/database/dbuser.db"
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
    if con:
        con.close()

@bot.event
async def on_ready():
    print('I logged in as {0.user}'.format(bot))
    bot.load_extension('dismusic')


@bot.command(pass_context=True)
async def hd(ctx):
    
    help = """
    Music commands

    Commands:
    `connect`    Gọi nó vào phòng
    `disconnect` Sút ẻm đi
    `equalizer`  Chỉnh âm
    `loop`       Chỉnh để lập lại `NONE`, `CURRENT` or `PLAYLIST`
    `pause`      Dừng
    `play [query]`       Phát hoặc thêm bài hát vào hàng đợi có thể dùng link youtube hoặc tên bài 
    `queue`      Xem hàng đợi
    `resume`     Tiếp tục
    `skip`       Chuyển sang bài tiếp theo
    `volume`     chỉnh volume 0-100

    
    """
    await ctx.send(help)
    # `nowplaying` What's playing now?


def write_log(mess):
    path = os.path.dirname(__file__)
    time = datetime.datetime.now()
    f = open(path + "/log.txt", "a", encoding="utf-8")
    f.write("" + str(time) +": "+ mess + '\n')
    f.close()


@bot.event
async def on_message(ctx):
    id = str(ctx.author).split('#')[1]
    data = select(f'SELECT * FROM USER WHERE id = "{id}"')
    status = False

    username = str(ctx.author.nick)
    if username == 'None':
        username = str(ctx.author).split("#")[0]
    elif len(username) > 20:
        username = str(ctx.author).split("#")[0]

    check_command = False
    if len(ctx.content) != 0:
        if str(ctx.content)[0] == '.':
            check_command = True
        else:
            check_command = False
    if id != '7964' and check_command == False  :
        if data != None:
            id_db = data[0]
            level = data[1]
            exp = data[2]
            mess = ''
            if str(id) == id_db:
                if id in config.id_admin and status == True:
                    exp += config.exp_admin
                    update(f'UPDATE USER SET EXP = {exp} WHERE id = "{id}"') # exp admin
                    mess = f"Member {username} collect {config.exp_admin} exp"
                else:
                    exp_collect = config.exp_colect + (level * 5) 
                    exp += exp_collect
                    update(f'UPDATE USER SET EXP = {exp} WHERE id = "{id}"') # exp cộng thêm
                    mess = f"Member {username} collect {exp_collect} exp"
                    write_log(mess)
                if exp >= level * config.exp_need: # Nếu exp có hơn exp cần level up
                    while True:
                        level += 1
                        update(f'UPDATE USER SET LVL = {level} WHERE id = "{id}"')
                        expex = exp - (level - 1) * 100 # tính exp thừa
                        
                        update(f'UPDATE USER SET EXP = {expex} WHERE id = "{id}"')
                        if expex <= level * 100 or exp == 0:
                            break
                    mess = f"Member {username} level up {level}"
                    if level % 10 == 0:
                     await ctx.channel.send(f"Chúc mừng bé `{username}` đã lên level {level} và nhận khung mới")
                    else:
                        await ctx.channel.send(f"Chúc mừng bé `{username}` đã lên level {level} nói nhiều lên để được lên cấp tiếp nhé")
                    write_log(mess)
        else:
            if id != '7964':
                insert(f'INSERT INTO USER VALUES("{id}",1,0,"{username}")')
                mess = f"Add member {username}"
                write_log(mess)
                await ctx.channel.send(f"Chào mừng bé `{username}` đã đến nơi hội tụ các con nghiện tương tác để lên cấp nhóe!")
    await bot.process_commands(ctx)


@bot.command(pass_context=True)
async def rank(cxt):
    
    id = str(cxt.author).split('#')[1]
    data = select(f'SELECT * FROM USER WHERE id = "{id}"')

    level = data[1]
    exp = data[2]
    lvlborder = str(int(level / 10))


    next_level_xp = level * 100
    current_level_xp = exp
    xp_per_cent = current_level_xp / next_level_xp * 100
    width =  300 * xp_per_cent / 100

    username = str(cxt.author.nick) 
    
    if username == "None":
        username = str(cxt.author).split('#')[0]
    path = os.path.dirname(__file__) + '/img/'
    path_font = os.path.dirname(__file__) 

    path_img = path + "bg1.jpg"
    path_border = path + f"{lvlborder}0.png"
    path_font = path_font + '/font11.ttf'
    # if id == '3010':
    #     path_img = "./img/bgdong.jpg"

    if level >= 50:
        path_border =path + f"50.png"

    background = Editor(f"{path_img}").resize((600,300))
    border = Editor(path_border).resize((150,150))
    profile = await load_image_async(str(cxt.author.avatar_url)) # lấy avr
    profile = Editor(profile).resize((100, 100)).circle_image()

    fontname = Font(path= path_font , size=23)
    fontlv = Font(path= path_font, size=20)    

    square = Canvas((500,500), "#06FFBF")
    square = Editor(square)
    square.rotate(30, expand=True)

    background.rectangle((100, 150), width=600, height=2, fill="#17F3F6")

    # exp bar
    background.rectangle((120, 220), width=300, height=25, fill="#17F3F6", radius=10)
    background.rectangle((120, 220), width=width, height=25, fill="#BD1536", radius=10)

    background.paste(square.image, (350,-300))
    # avt
    background.paste(profile.image, (24,23))
    background.paste(border.image, (0,0))

    txt_name = background.text((155,100), f'{username}#{id}', font=fontname, color='#FFF')
    txt_exp = background.text((165,175), f'Level: {level} EXP: {exp}/{next_level_xp}', font=fontlv, color='#51E4E4')

    file = File(fp=background.image_bytes, filename='card.png')
    await cxt.send(file = file)


@bot.command(pass_context=True)
async def lvl(ctx,id,lvl):

    iid = str(ctx.author).split("#")[1]
    if id == ".":
        update(f'UPDATE USER SET LVL = {lvl}, exp = 0 WHERE id = "{iid}"')
        mess = f"lvl: Up level ID:{iid}"
        write_log(mess)
        await ctx.channel.send(f'ID {iid} đã lên level {lvl}')
    else:
        update(f'UPDATE USER SET LVL = {lvl}, exp = 0 WHERE id = "{id}"')
        mess = f".lvl: Up {lvl} level ID:{id}"
        write_log(mess)
        await ctx.channel.send(f'ID {id} đã lên level {lvl}')


@bot.command(pass_context=True)
async def exp(ctx,id,exp):
    lvl = 0
    exppp = 0
    iid = str(ctx.author).split("#")[1]
    i = 0
    username = str(ctx.author.nick)
    if id == ".":
        i = int(iid)
    else:
        i = id
    if username == 'None':
        username = str(ctx.author)

    if id == ".":
        data = select(f'SELECT * FROM USER WHERE ID = "{iid}"')
        expp = data[2]
        lvl = data[1]
        exppp = expp + int(exp)
        update(f'UPDATE USER SET EXP = {exppp} WHERE id = "{iid}"')
        mess = f".exp: Buff {exppp}exp ID:{iid}"
        write_log(mess)
        await ctx.channel.send(f'ID {iid} đã nhập {exppp} exp')
    else:
        data = select(f'SELECT * FROM USER WHERE ID = "{id}"')
        expp = data[2]
        lvl = data[1] # lấy dữ liệu

        exppp = expp + int(exp) 
        
        update(f'UPDATE USER SET EXP = {exppp} WHERE id = "{id}"')
        mess = f".exp: Buff {exppp} exp ID:{id}"
        write_log(mess)
        await ctx.channel.send(f'ID {id} đã nhập {exppp} exp')

    if exppp >= lvl * config.exp_need: # Nếu exp có hơn exp cần level up
        while True:
            lvl += 1
            update(f'UPDATE USER SET LVL = {lvl} WHERE id = {i}')
            expex = exppp - (lvl - 1) * 100 # tính exp thừa
            update(f'UPDATE USER SET EXP = {expex} WHERE id = {i}')
            if expp <= lvl * 100 or exp == 0:
                break
        mess = f"Member {username} level up {lvl}"
        write_log(mess)
        await ctx.channel.send(f"Chúc mừng bé `{username}` đã lên level {lvl} nói nhiều lên để được lên cấp tiếp nhé")
        

@bot.command(pass_context=True)
async def setexp(ctx,id):

    iid = str(ctx.author).split("#")[1]

    if id == ".":
        update(f'UPDATE USER SET EXP = 0 WHERE id = "{iid}"')
        mess = f".setexp: Set 0 exp ID:{iid}"
        write_log(mess)
        await ctx.channel.send(f'ID {iid} đã về 0 exp')
    else:
        update(f'UPDATE USER SET EXP = 0 WHERE id = "{id}"')
        mess = f".setexp: Set 0 exp ID:{id}"
        write_log(mess)
        await ctx.channel.send(f'ID {id} đã về 0 exp')

class datauser():
    id = 0
    lvl = 1
    exp = 0
    name = ""
    def __init__(self,id , level = 1, exp = 0,name = ""):
        self.id = id
        self.lvl = level
        self.exp = exp
        self.name = name

def sort_rank():
    datas = selectall('select* from user')
    Luser = []

    for data in datas:
        Luser.append(datauser(data[0],data[1],data[2],data[3]))

    for i in range(len(Luser)):
        for j in range(len(Luser)):
            if i != j:
                if Luser[i].lvl == Luser[j].lvl:
                    if Luser[i].exp > Luser[j].exp:
                            temp = Luser[i]
                            Luser[i] = Luser[j]
                            Luser[j] = temp
                elif Luser[i].lvl > Luser[j].lvl:
                    temp = Luser[i]
                    Luser[i] = Luser[j]
                    Luser[j] = temp
    return Luser
@bot.command(pass_context=True)
async def board(ctx):
    path = os.path.dirname(__file__)
    id = str(ctx.author).split('#')[1]
    background = Editor(path + "/img/rank/board.jpg").resize((1920,1080)).rotate(90, expand=True)
    font = Font(path + "/font11.ttf",size=52)

    rank = sort_rank()

    data = select(f'SELECT * FROM USER WHERE id = "{id}"')
    level = data[1]
    lvlborder = str(int(level / 10))

    if level >= 50:
        border = Editor(path + "/img/50.png").resize((300,300))
    else:
        border = Editor(path + "/img/{lvlborder}.png").resize((300,300))

    profile = await load_image_async(str(ctx.author.avatar_url)) # lấy avr
    profile = Editor(profile).resize((180, 180)).circle_image()
    
    background.paste(profile.image, (62,60))
    background.paste(border.image, (0,0))

    Y = 350
    X = 100
    X_img = X - 20
    X_txt = X + 100
    top = 1
    for i in rank:
        Y_img = Y - 30
        rank = Editor(path + f"/img/rank/top{top}.png").resize((120,120))
        background.rectangle((X, Y), width=950, height=60, fill="#17F3F6",radius=30)
        background.paste(rank.image, (X_img, Y_img))
        txt_name = background.text((X_txt,Y),f"{i.name}",font,color='black')
        txt_lvl = background.text((725,Y),f"Level: {i.lvl}",font,color='black')
        Y += 130
        top += 1

    file = File(fp=background.image_bytes, filename='card.png')
    await ctx.send(file = file)
    
bot.run(TOKEN)