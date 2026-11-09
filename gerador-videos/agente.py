import argparse, asyncio, json, os, subprocess, tempfile, unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import edge_tts

ROOT=Path(__file__).resolve().parent
BASE=ROOT
DATA=json.loads((ROOT/'roteiros.json').read_text())
FONT=str(ROOT/'assets/DejaVuSans.ttf')
BOLD=str(ROOT/'assets/DejaVuSans-Bold.ttf')

def wrap(draw,text,font,width):
 lines=[];line=''
 for word in text.split():
  trial=(line+' '+word).strip()
  if draw.textbbox((0,0),trial,font=font)[2]>width and line: lines.append(line);line=word
  else: line=trial
 if line:lines.append(line)
 return lines

def artwork(item,index,scene,dest):
 im=Image.new('RGB',(540,960),'#ffffff');d=ImageDraw.Draw(im)
 blue='#075bff';ink='#080e1b';small=ImageFont.truetype(BOLD,17);head=ImageFont.truetype(BOLD,33);body=ImageFont.truetype(FONT,28)
 logo=Image.open(BASE/'assets/logo-blue.jpg').convert('RGB').resize((70,70));im.paste(logo,(31,45));d.text((110,60),'ZEEY DIGITAL',font=small,fill=ink)
 d.text((38,150),f'HISTÓRIAS DE NEGÓCIOS  /  {index+1:02}',font=small,fill=blue)
 for n,line in enumerate(wrap(d,item['titulo'],head,460)):d.text((38,195+n*44),line,font=head,fill=ink)
 previews=['preview-valenca.webp','preview-conversa.webp','preview-nexo.webp']
 preview=Image.open(BASE/'assets'/previews[min(scene,2)]).convert('RGB')
 preview=ImageOps.fit(preview,(464,270),method=Image.Resampling.LANCZOS,centering=(.5,0))
 im.paste(preview,(38,330));d.rectangle((38,330,502,600),outline='#d5e2f4',width=2)
 d.text((38,616),'EXEMPLO DEMONSTRATIVO · MARCA FICTÍCIA',font=ImageFont.truetype(FONT,13),fill='#61728c')
 y=680
 for line in wrap(d,item['cenas'][scene],body,462):d.text((38,y),line,font=body,fill=ink);y+=38
 d.rounded_rectangle((38,877,502,924),radius=22,fill=blue);d.text((112,887),'zeeydigital.com.br  →',font=small,fill='white')
 im.save(dest)

async def speech(text,path):
 c=edge_tts.Communicate(text,voice='pt-BR-AntonioNeural',rate='+16%',pitch='+4Hz',proxy=os.environ.get('HTTPS_PROXY'))
 await c.save(str(path))

def command(args):subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def duration(path):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)]))

def slug(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c)).replace(' ','-')

async def make(item,i):
 out=ROOT/'videos';out.mkdir(exist_ok=True);target=out/f'{i+1:02d}-{slug(item["titulo"])}.mp4'
 if target.exists():print('Já existe:',target.name,flush=True);return
 with tempfile.TemporaryDirectory(dir=ROOT) as td:
  p=Path(td); clips=[]
  for j,line in enumerate(item['cenas']):
   a=p/f'{j}.mp3';img=p/f'{j}.png';clip=p/f'{j}.mp4'
   await speech(line,a);artwork(item,i,j,img)
   command(['ffmpeg','-v','error','-y','-loop','1','-framerate','24','-i',str(img),'-i',str(a),'-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(clip)])
   clips.append(clip)
  listing=p/'lista.txt';listing.write_text(''.join("file '"+str(x)+"'\n" for x in clips))
  tmp=p/'video.mp4';command(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(tmp)])
  command(['ffmpeg','-v','error','-i',str(tmp),'-f','null','-']);tmp.replace(target)
 print('Gerado e verificado:',target.name,flush=True)

async def main():
 a=argparse.ArgumentParser();a.add_argument('--inicio',type=int,default=1);a.add_argument('--limite',type=int,default=20);a.add_argument('--vigiar',action='store_true',help='Monitora roteiros.json e gera novos itens acrescentados');args=a.parse_args()
 if not 1<=args.inicio<=len(DATA) or args.limite<1:raise SystemExit('Início ou limite inválido.')
 while True:
  before=(ROOT/'roteiros.json').read_text()
  items=json.loads(before)
  for i in range(args.inicio-1,min(len(items),args.inicio-1+args.limite)):await make(items[i],i)
  if not args.vigiar:break
  print('Aguardando novos roteiros; pressione Ctrl+C para encerrar.',flush=True)
  while (ROOT/'roteiros.json').read_text()==before:await asyncio.sleep(30)
asyncio.run(main())
