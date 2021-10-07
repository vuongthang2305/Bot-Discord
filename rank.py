from easy_pil import Canvas, Editor, Font


background = Editor("./img/rank/board.jpg").resize((1920,1080)).rotate(90, expand=True)
font = Font("./font11.ttf",size=52)
rank = Editor("./img/rank/top1.png").resize((120,120))

profile = Editor("./img/avt.jpg").resize((180, 180)).circle_image()
border = Editor("./img/50.png").resize((300,300))

background.paste(profile.image, (62,60))
background.paste(border.image, (0,0))

Y = 350
X = 100
X_img = X - 20
X_txt = X + 100
for i in range(1,10):
    Y_img = Y - 30
    
    background.rectangle((X, Y), width=950, height=60, fill="#17F3F6",radius=30)
    background.paste(rank.image, (X_img, Y_img))
    txt = background.text((X_txt,Y),"rank",font,color='black')
    Y += 130
background.show()