from discord.ext import commands

TOKEN = 'ODg0NzQzMzA5MjIwNzk0NDI5.YTc7ag.8CWkysbkYSqeWlH7M4ooJ8qu-MU'

bot = commands.Bot(command_prefix = '.')
bot.lava_nodes = [{
    'host': 'lava.link',
    'port': 80,
    'rest_uri':f'http://lava.link:80',
    'identifier':'MAIN',
    'password':'anything',
    'region':'vietnam'
}]
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
bot.run(TOKEN)