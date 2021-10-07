from os import terminal_size
from easy_pil import Canvas, Editor, Font


background = Editor("./img/rank/board.jpg").resize((1920,1080)).rotate(90, expand=True)
font = Font("./font11.ttf",size=52)
rank = Editor("./img/rank/top1.png").resize((120,120))

profile = Editor("./img/avt.jpg").resize((180, 180)).circle_image()
border = Editor("./img/50.png").resize((300,300))

background.paste(profile.image, (62,60))
background.paste(border.image, (0,0))

rec = Canvas((200,200),'black',)
rec = Editor(rec)
rec.rotate(30,True)

background.paste(rec.image,(500,500))
background.rectangle((500,482),200,200,'red',radius=100)

background.show()