from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W=H=1024
img=Image.new('RGB',(W,H),(8,16,32)); d=ImageDraw.Draw(img)

def font(size,bold=False):
    paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    return ImageFont.truetype(paths[0],size)

def text(xy,s,size,fill=(235,242,250),bold=False,anchor=None):
    d.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)

def rounded(box,r,fill,outline=None,w=1): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=w)

# editorial night-sky canvas
for y in range(H):
    c=(8+int(10*y/H),16+int(12*y/H),32+int(24*y/H)); d.line((0,y,W,y),fill=c)
# faint globe
cx,cy,r=512,560,280
d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(16,43,69),outline=(74,145,170),width=4)
# latitude/longitude lines
for k in (-2,-1,0,1,2):
    yy=cy+k*85
    d.arc((cx-r,yy-35,cx+r,yy+35),0,360,fill=(39,87,110),width=2)
for k in (-2,-1,0,1,2):
    xx=cx+k*90
    d.arc((xx-50,cy-r,xx+50,cy+r),90,270,fill=(39,87,110),width=2)
# rough continents / hotspots
continents=[[(355,430),(430,390),(485,415),(465,475),(410,500),(370,470)],[(510,390),(600,405),(650,460),(620,520),(550,500),(520,450)],[(650,570),(720,610),(690,690),(625,720),(590,650)],[(415,575),(480,600),(500,720),(455,790),(410,700)]]
for poly in continents: d.polygon(poly,fill=(31,86,73),outline=(64,145,104))
# conflict / crisis markers
markers=[(570,468,(255,93,73)),(652,636,(255,164,73)),(436,657,(245,84,84)),(705,470,(255,205,79))]
for x,y,c in markers:
    d.ellipse((x-17,y-17,x+17,y+17),fill=c,outline=(255,240,190),width=3)
    d.line((x-28,y,x+28,y),fill=c,width=2); d.line((x,y-28,x,y+28),fill=c,width=2)
# top title
text((60,54),'THE WORLD, IN ONE DAY',38,(255,255,255),True)
text((62,102),'TUESDAY 24 NOVEMBER 2026',20,(125,195,211),True)
d.line((62,140,962,140),fill=(70,145,165),width=2)
# headline bands
cards=[
 ('WAR & POWER','Ukraine strikes Russian oil sites;\nMideast violence and uncertainty persist.',(255,102,83)),
 ('TRADE & TECH','New US tariffs loom as Jensen Huang\nreturns to Nvidia amid China tensions.',(255,193,84)),
 ('CLIMATE & HEALTH','King tides flood California;\nmeasles and Ebola strain public health.',(92,205,171)),
 ('PEOPLE ON THE MOVE','~175 migrants missing off Senegal;\nHong Kong still remembers its fire.',(132,164,255)),
]
positions=[(50,180),(530,180),(50,820),(530,820)]
for (label,body,col),(x,y) in zip(cards,positions):
    rounded((x,y,x+444,y+112),18,(18,34,55),col,3)
    d.ellipse((x+22,y+22,x+46,y+46),fill=col)
    text((x+60,y+18),label,18,col,True)
    for i,line in enumerate(body.split('\n')): text((x+22,y+53+i*25),line,17,(231,238,245))
# connecting arcs
for a,b in [((494,350),(530,350)),((494,855),(530,855))]: d.line((*a,*b),fill=(104,166,180),width=3)
# footer
text((512,974),'A crowded planet: conflict, power, weather, movement.',19,(180,208,218),anchor='ms')
# deterministic PNG metadata-free save
outdir='/output' if os.access('/',os.W_OK) else os.path.join(os.path.dirname(__file__),'output')
os.makedirs(outdir,exist_ok=True)
img.save(os.path.join(outdir,'entry.png'),format='PNG',optimize=False)
