from easy_pil import Canvas, Editor, Font

class user():
    id = 0
    level = 1
    exp = 0
    def __init__(self,id , level = 1, exp = 0):
        self.id = id
        self.level = level
        self.exp = exp

db = [user(9002,1,20)]

next_level_xp = db[0].level * 100
current_level_xp = db[0].exp
xp_per_cent = current_level_xp / next_level_xp * 100
width =  300 * xp_per_cent / 100

background = Editor("./img/bg1.jpg").resize((600,300))
fontname = Font('font1.ttf', size=25)
fontlv = Font('font1.ttf', size=20)
profile = Editor("./img/avt.jpg").resize((100, 100)).circle_image()
border = Editor("./img/40.png").resize((150,150))
poppins = Font().poppins(size=40)
poppins_small = Font().poppins(size=30)


square = Canvas((500,500), "#06FFBF")
square = Editor(square)
square.rotate(30, expand=True)



background.rectangle((100, 150), width=600, height=2, fill="#17F3F6")
background.rectangle((120, 220), width=300, height=25, fill="#17F3F6", radius=10)
background.rectangle((120, 220), width=width, height=25, fill="#BD1536", radius=10)
background.paste(square.image, (350,-300))
background.paste(profile.image, (24,23))
background.paste(border.image, (0,0))
background.text((165,100), 'Theng#9002', font=fontname, color='#51E4E4')
background.text((165,175), f'Level: {db[0].level} EXP: {db[0].level}/100', font=fontlv, color='#51E4E4')
background.show()