"""Gera os assets do combo a partir das capas em _src/ (800x800, tablet no centro).
Para trocar uma capa: substitua o arquivo em _src/ e rode  python _build_assets.py"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
BOX=(170,82,629,720)  # moldura do tablet nas capas 800x800
def load(name):
    p=f'_src/{name}.png'
    if os.path.exists(p): return Image.open(p).convert('RGB').resize((800,800),Image.LANCZOS)
    return placeholder(name)
def placeholder(name):
    # capa provisória até chegar a imagem real — NÃO publicar assim
    im=Image.new('RGB',(800,800),(12,14,22)); d=ImageDraw.Draw(im)
    d.rounded_rectangle(BOX,radius=36,fill=(235,235,235))
    d.rounded_rectangle((BOX[0]+12,BOX[1]+22,BOX[2]-12,BOX[3]-22),radius=14,fill=(22,26,70))
    try: f=ImageFont.truetype('arialbd.ttf',30); g=ImageFont.truetype('arialbd.ttf',96)
    except OSError: f=g=ImageFont.load_default()
    for y,t,ft in [(250,'VADE MECUM TÁTICO',f),(300,'PCPE',g),(470,'capa pendente',f)]:
        w=d.textlength(t,font=ft); d.text(((800-w)/2,y),t,font=ft,fill=(255,255,255))
    return im
src={k:load(k) for k in ['resumo','questoes','vade']}
def tablet(im):
    t=im.crop(BOX); m=Image.new('L',t.size,0)
    ImageDraw.Draw(m).rounded_rectangle((0,0,t.size[0]-1,t.size[1]-1),radius=36,fill=255)
    t=t.convert('RGBA'); t.putalpha(m); return t
for k,im in src.items():
    im.crop((120,40,680,740)).resize((400,500),Image.LANCZOS).save(f'assets/combo-{k}.webp',quality=82)
W,H=980,760; canvas=Image.new('RGBA',(W,H),(0,0,0,0))
def place(t,w,angle,cx,cy):
    h=int(t.size[1]*w/t.size[0]); t=t.resize((w,h),Image.LANCZOS).rotate(angle,expand=True,resample=Image.BICUBIC)
    a=t.split()[3]; sh=Image.new('RGBA',t.size,(0,0,0,0)); sh.paste((0,0,0,150),mask=a)
    sh=sh.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(sh,(cx-t.size[0]//2+10,cy-t.size[1]//2+22)); canvas.alpha_composite(t,(cx-t.size[0]//2,cy-t.size[1]//2))
place(tablet(src['questoes']),330,9,250,400)
place(tablet(src['vade']),330,-9,730,400)
place(tablet(src['resumo']),380,0,490,375)
b=canvas.getbbox(); canvas=canvas.crop((b[0]-10,b[1]-10,b[2]+10,b[3]+10)); canvas.save('assets/combo.webp',quality=86)
print('combo',canvas.size)
og=Image.new('RGBA',(1200,630),(10,14,26,255)); c2=canvas.copy(); c2.thumbnail((820,600))
og.alpha_composite(c2,((1200-c2.size[0])//2,(630-c2.size[1])//2)); og.convert('RGB').save('assets/og-combo.jpg',quality=84)
# brasão da PCPE: recortado da capa do Caderno, fundo removido por preenchimento a partir das bordas
s=Image.open('_src/questoes.png').convert('RGB').crop((300,262,500,500)).resize((400,500),Image.LANCZOS)
mask=Image.new('L',s.size,255); px=s.load(); mp=mask.load(); W2,H2=s.size
stack=[(x,y) for x in range(W2) for y in (0,H2-1)]+[(x,y) for y in range(H2) for x in (0,W2-1)]
seen=set()
while stack:
    x,y=stack.pop()
    if (x,y) in seen or not(0<=x<W2 and 0<=y<H2): continue
    seen.add((x,y)); r,g,bb=px[x,y]
    if r+g+bb>330: continue          # borda clara do escudo: para aqui
    mp[x,y]=0; stack+= [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
mask=mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
s=s.convert('RGBA'); s.putalpha(mask); s=s.crop(s.getbbox()); s.thumbnail((400,240),Image.LANCZOS)
s.save('assets/brasao-pcpe.png',optimize=True); print('brasao',s.size)
