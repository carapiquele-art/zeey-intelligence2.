"""Locução, legenda por palavra e exportação; sem geração ou cobrança externa de vídeo."""
import asyncio, json, os, subprocess
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parent

def run(args):
 r=subprocess.run(args,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-1800:])
 return r.stdout

def stamp(s):
 cs=round(max(0,s)*100)
 return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'

def escape(s):return s.replace('\\','').replace('{','').replace('}','')

def write_ass(words,path):
 text='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Zeey Switzer,62,&H00FFFFFF,&H00FF5B07,&H00201108,&H90000000,-1,0,0,0,100,100,0,0,1,2,1,5,90,90,350,1
Style: Brand,Zeey Switzer,34,&H00FFFFFF,&H00FFFFFF,&H00201108,&H90000000,-1,0,0,0,100,100,2,0,1,1.5,0,7,74,90,108,1
Style: Link,Zeey Switzer,34,&H00FFFFFF,&H00FFFFFF,&H00201108,&H90000000,0,0,0,0,100,100,0,0,1,1.5,0,2,90,90,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 groups=[]; current=[]
 connectors={'a','o','as','os','de','do','da','dos','das','ao','aos','para','com','e'}
 for w in words:
  current.append(w)
  if len(current)>=4 or w['text'][-1:] in '.?!,;:':
   carry=None
   if len(current)>=4 and current[-1]['text'].lower() in connectors:carry=current.pop()
   groups.append(current);current=[carry] if carry else []
 if current:groups.append(current)
 for gi,group in enumerate(groups):
  for wi,w in enumerate(group):
   start=group[0]['start'] if wi==0 else w['start']
   if wi+1<len(group):end=group[wi+1]['start']
   elif gi+1<len(groups):end=groups[gi+1][0]['start']
   else:end=w['end']+.35
   rendered=' '.join(('{\\c&H00FF5B07&}' if n==wi else '{\\c&H00FFFFFF&}')+escape(v['text']) for n,v in enumerate(group))
   text+=f'Dialogue: 2,{stamp(start)},{stamp(end)},Caption,,0,0,0,,{{\\an5\\pos(540,1510)}}'+rendered+'\n'
 text+='Dialogue: 1,0:00:00.00,0:10:00.00,Brand,,0,0,0,,ZEEY DIGITAL\n'
 text+='Dialogue: 1,0:00:00.00,0:10:00.00,Link,,0,0,0,,zeeydigital.com.br\n'
 path.write_text(text,encoding='utf-8')

async def narration(text,voice,path):
 c=edge_tts.Communicate(text,voice=voice,rate='+20%',pitch='+4Hz',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'))
 words=[]
 with path.open('wb') as f:
  async for chunk in c.stream():
   if chunk['type']=='audio':f.write(chunk['data'])
   elif chunk['type']=='WordBoundary':words.append({'text':chunk['text'],'start':chunk['offset']/1e7,'end':(chunk['offset']+chunk['duration'])/1e7})
 # O texto de exibição preserva a pontuação quando o TTS emite uma marca por palavra.
 tokens=text.split()
 if len(tokens)==len(words):
  for token,w in zip(tokens,words):w['text']=token
 return words

async def export(name,clips,text,voice='pt-BR-AntonioNeural'):
 out=ROOT/'saida';out.mkdir(exist_ok=True)
 mp3=out/(name+'.mp3');words=await narration(text,voice,mp3)
 (out/(name+'-palavras.json')).write_text(json.dumps(words,ensure_ascii=False,indent=2))
 ass=out/(name+'.ass');write_ass(words,ass)
 listing=out/(name+'-lista.txt');listing.write_text(''.join("file '"+str(c.resolve())+"'\n" for c in clips))
 duration=sum(float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(c)])) for c in clips)
 speech_dur=float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(mp3)]))
 if words[-1]['end']+.1>duration:raise RuntimeError(f'Locução falada maior que animação ({duration:.1f}s); encurtar o texto sem congelar a cena.')
 # Interpolação no tamanho de origem; exportação 1080p é ampliação, não detalhe nativo.
 vf=f"minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.25:5:5:0,drawbox=x=65:y=1438:w=950:h=148:color=0x07101f@0.76:t=fill,subtitles='{ass}':fontsdir='{ROOT/'fonts'}'"
 final=out/(name+'.mp4')
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(mp3),'-i',str(ROOT/'assets/trilha.mp3'),'-filter_complex',f'[0:v]{vf}[v];[1:a]apad[a];[2:a]volume=0.23[b];[a][b]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[aout]','-map','[v]','-map','[aout]','-t',str(max(0,duration-.08)),'-r','30','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-b:a','192k','-movflags','+faststart',str(final)])
 run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'])
 print('Exportado e verificado:',final,flush=True)
 return final

if __name__=='__main__':
 asyncio.run(export('Zeey_teste_legenda_V2',[ROOT/'saida/03_atelie_c0.mp4',ROOT/'saida/03_atelie_c1.mp4'],'Tudo ao mesmo tempo? O Z conecta as informações, para sua equipe continuar. Zeey.'))
