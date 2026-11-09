import asyncio,json,math,os,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import edge_tts
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'v2';OUT.mkdir(exist_ok=True)
W,H,FPS=540,960,15
FONT=str(ROOT.parent/'fonts/switzer-700.ttf')
REG=str(ROOT.parent/'fonts/switzer-500.ttf')
BLUE='#075BFF';WHITE='#FFFFFF';NAVY='#081429';GREY='#AAB9D4';RED='#FF6B66';GREEN='#57DDA5'
STORIES=[
 dict(name='01_oficina', business='OFICINA', person='Rafael', time='19:40', customer='Meu carro falhou. Consegue olhar amanhã?', lost='Quarenta minutos sem resposta.\nO cliente chama outra oficina.', fields=['Modelo do carro','O que aconteceu?','Melhor horário'], data=['Onix 2019','Falha ao ligar','Amanhã, 9h'], objection='“Vai dar preço errado?”', answer='Não. A equipe aprova o orçamento.', result='Pedido organizado.\nRafael responde com contexto.', parts=[
  'São sete e quarenta da noite. Rafael está com a mão no motor. Um cliente escreve: meu carro falhou, consegue olhar amanhã?',
  'Quarenta minutos se passam. Sem resposta, o cliente chama outra oficina. Rafael sabe consertar. Só não viu a mensagem a tempo.',
  'Com a Zeey, uma página simples pergunta o modelo, o sintoma e o melhor horário. O pedido chega organizado para a equipe.',
  'Mas uma automação pode dar um preço errado? Não. Ela recolhe as informações. Rafael analisa o caso e aprova o orçamento.',
  'O cliente recebe a confirmação, e Rafael continua trabalhando. A tecnologia cuida da passagem; o serviço continua sendo dele. Zeey.'
 ]),
 dict(name='02_confeitaria', business='CONFEITARIA', person='Joana', time='09:12', customer='Faz bolo para sábado? Quanto custa?', lost='O pedido chega durante a produção.\nFaltam detalhes para responder.', fields=['Data da festa','Tamanho do bolo','Sabor desejado'], data=['Sábado, 16h','20 pessoas','Chocolate'], objection='“Vai prometer o que não faço?”', answer='Não. Joana define opções e disponibilidade.', result='Detalhes completos.\nJoana confirma a encomenda.', parts=[
  'Joana está terminando três bolos quando chega uma mensagem: faz bolo para sábado? Quanto custa? Ela não consegue parar agora.',
  'Sem data, tamanho e sabor, qualquer preço seria um chute. A cliente espera, procura outro perfil e a encomenda esfria.',
  'A Zeey mostra os modelos disponíveis, pergunta a data, o tamanho e o sabor. Joana recebe um pedido completo para avaliar.',
  'Mas o sistema vai prometer um bolo que ela não consegue fazer? Não. Joana define as opções e confirma a disponibilidade.',
  'A cliente sabe o próximo passo. Joana continua criando e só entra quando a decisão precisa dela. Zeey, do jeito do seu negócio.'
 ]),
 dict(name='03_servicos', business='SERVIÇOS', person='Camila', time='14:06', customer='Já contei tudo ontem. Vou repetir?', lost='Site, WhatsApp e papel.\nO histórico se espalhou.', fields=['Nome e contato','Serviço pedido','Etapa da conversa'], data=['Cliente Ana','Instalação','Aguardando visita'], objection='“O atendimento fica robótico?”', answer='Não. A pessoa assume com o histórico.', result='Histórico reunido.\nCamila continua de onde parou.', parts=[
  'Ana escreveu no site. Depois chamou no WhatsApp. Hoje recebe uma ligação e pergunta: vou ter que contar tudo de novo?',
  'Camila procura a conversa, a anotação e a planilha. O problema não é falta de cuidado. A informação está espalhada.',
  'A Zeey reúne o pedido, o contato e a etapa da conversa num fluxo que a equipe entende. Camila vê o histórico antes de responder.',
  'Mas isso deixa o atendimento robótico? Não. A automação organiza e avisa. Camila assume a conversa quando importa.',
  'Ana não precisa repetir. A equipe sabe o próximo passo. Cada negócio tem seu jeito; a solução acompanha esse jeito. Zeey.'
 ])]

def font(n,bold=False):return ImageFont.truetype(FONT if bold else REG,n)
def rr(d,box,r,fill,outline=None,width=2):d.rounded_rectangle(box,r,fill=fill,outline=outline,width=width)
def fit(d,text,x,y,maxwidth,size=30,color=WHITE,bold=True,spacing=6):
 f=font(size,bold); words=text.split();lines=[];line=''
 for w in words:
  cand=(line+' '+w).strip()
  if d.textlength(cand,font=f)>maxwidth and line:lines.append(line);line=w
  else:line=cand
 if line:lines.append(line)
 for line in lines:d.text((x,y),line,font=f,fill=color);y+=size+spacing
 return y

def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def bg3d(i,frame,zoom=1):
 p=ROOT/f'filme_rapido{i+1}'/f'frame_{frame:04d}.png'
 im=Image.open(p).convert('RGB')
 if zoom!=1:
  w,h=im.size;cw=int(w/zoom);ch=int(h/zoom);im=im.crop(((w-cw)//2,(h-ch)//2,(w+cw)//2,(h+ch)//2))
 return im.resize((W,H),Image.Resampling.LANCZOS)

def paint(i,story,stage,progress,word,total,frame_num):
 if stage in (0,3,4):
  idx=1+int((frame_num*2.7)%132)
  im=bg3d(i,min(idx,132),1.06 if stage==4 else 1)
  dim=Image.new('RGBA',(W,H),(3,10,28,90 if stage==0 else 130))
  im=Image.alpha_composite(im.convert('RGBA'),dim)
 else:
  im=Image.new('RGBA',(W,H),NAVY)
 d=ImageDraw.Draw(im)
 d.text((32,34),'ZEEY',font=font(26,True),fill=WHITE)
 d.text((122,39),'DIGITAL',font=font(17,True),fill=BLUE)
 d.text((W-35,43),story['business'],anchor='ra',font=font(14,True),fill=GREY)
 if stage==0:
  rr(d,(30,105,235,153),14,NAVY);d.text((46,116),story['time'],font=font(23,True),fill=WHITE)
  y=189+int(8*math.sin(frame_num*.15));rr(d,(28,y,W-28,y+116),22,WHITE)
  d.ellipse((43,y+20,83,y+60),fill=BLUE);d.text((55,y+26),'?',font=font(20,True),fill=WHITE)
  fit(d,story['customer'],98,y+20,W-145,22,NAVY,True,4)
  fit(d,'UM PEDIDO NO MEIO DO TRABALHO',32,734,W-64,32,WHITE,True)
 elif stage==1:
  d.text((35,118),'A CONVERSA PAROU',font=font(30,True),fill=WHITE)
  rr(d,(32,200,W-32,592),30,'#14243C')
  d.text((56,225),'Cliente',font=font(20,True),fill=GREY)
  rr(d,(55,279,W-82,389),19,BLUE)
  fit(d,story['customer'],73,296,W-181,22,WHITE,True)
  timer=int(progress*40);d.text((57,428),f'{timer:02}:00 sem resposta',font=font(24,True),fill=RED)
  if progress>.55:
   rr(d,(55,487,W-82,553),16,'#25364E');d.text((70,507),'Cliente saiu da conversa',font=font(19,True),fill=GREY)
  fit(d,story['lost'],35,660,W-70,27,WHITE,True)
 elif stage==2:
  d.text((35,115),'O Z ORGANIZA O PEDIDO',font=font(27,True),fill=WHITE)
  rr(d,(33,191,W-33,698),30,'#14243C')
  d.text((57,219),'NOVO PEDIDO',font=font(18,True),fill=BLUE)
  for j,(field,value) in enumerate(zip(story['fields'],story['data'])):
   y=276+j*120
   appear=ease(progress*3.8-j*.8)
   if appear<=0:continue
   dx=int((1-appear)*W)
   rr(d,(56+dx,y,W-56+dx,y+95),17,'#223651')
   d.text((74+dx,y+11),field,font=font(17),fill=GREY)
   d.text((74+dx,y+43),value,font=font(23,True),fill=WHITE)
  d.text((55,728),'DADOS CERTOS → EQUIPE',font=font(22,True),fill=GREEN)
 elif stage==3:
  rr(d,(30,112,W-30,244),22,NAVY)
  d.text((50,134),'PAINEL DA EQUIPE',font=font(27,True),fill=WHITE)
  d.text((50,186),story['person']+' recebe o contexto',font=font(20),fill=GREY)
  for j,(field,value) in enumerate(zip(story['fields'],story['data'])):
   x=32+int((1-ease(progress*2.4-j*.35))*W)
   y=306+j*100
   rr(d,(x,y,x+W-64,y+80),15,WHITE)
   d.text((x+16,y+10),field,font=font(16),fill='#5B687F')
   d.text((x+16,y+35),value,font=font(21,True),fill=NAVY)
 elif stage==4:
  rr(d,(28,116,W-28,292),22,NAVY)
  fit(d,story['objection'],48,137,W-96,30,WHITE,True)
  if progress>.27:
   rr(d,(28,321,W-28,483),22,BLUE)
   fit(d,story['answer'],48,348,W-96,27,WHITE,True)
  d.text((34,690),'AUTOMAÇÃO + DECISÃO HUMANA',font=font(22,True),fill=WHITE)
 else:
  d.text((36,120),'PRÓXIMO PASSO CLARO',font=font(28,True),fill=WHITE)
  rr(d,(35,208,W-35,565),27,'#173052')
  d.ellipse((W//2-41,255,W//2+41,337),fill=GREEN)
  d.text((W//2,264),'✓',anchor='mt',font=font(47,True),fill=NAVY)
  fit(d,story['result'],67,377,W-134,28,WHITE,True)
  d.text((36,651),'Cada empresa tem seu jeito.',font=font(26,True),fill=WHITE)
  d.text((36,693),'A solução acompanha.',font=font(27,True),fill=GREEN)
  d.text((36,755),'zeeydigital.com.br',font=font(20,True),fill=BLUE)
 # Legenda com progressão por palavra
 if word:
  rr(d,(20,817,W-20,914),18,'#07101FE8')
  fit(d,word,34,840,W-68,24,WHITE,True,4)
 return im.convert('RGB')

async def produce(i,story):
 text=' '.join(story['parts']);voice=OUT/(story['name']+'.mp3');words=[]
 comm=edge_tts.Communicate(text,'pt-BR-AntonioNeural',rate='+35%',pitch='+4Hz',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'))
 with voice.open('wb') as f:
  async for c in comm.stream():
   if c['type']=='audio':f.write(c['data'])
   elif c['type']=='WordBoundary':words.append(dict(text=c['text'],start=c['offset']/1e7,end=(c['offset']+c['duration'])/1e7))
 if not words:raise RuntimeError('Sem tempos de voz')
 counts=[len(p.split()) for p in story['parts']]
 if sum(counts)!=len(words):
  print('word mismatch',story['name'],sum(counts),len(words),flush=True)
  # Distribuição proporcional quando a voz agrupa termos.
  cumul=[round(sum(counts[:j+1])*len(words)/sum(counts)) for j in range(5)]
 else:cumul=[sum(counts[:j+1]) for j in range(5)]
 bounds=[0]+[words[min(c-1,len(words)-1)]['end'] for c in cumul]
 duration=words[-1]['end']+.8
 raw=OUT/(story['name']+'_sem_audio.mp4');final=OUT/(story['name']+'.mp4')
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(raw)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(math.ceil(duration*FPS)):
  t=n/FPS; stage=next((j for j in range(5) if t<bounds[j+1]),5)
  start=bounds[stage];end=bounds[stage+1] if stage<5 else duration
  progress=(t-start)/max(.1,end-start)
  active=[w['text'] for w in words if w['start']<=t<w['end']+.10]
  wi=next((j for j,w in enumerate(words) if w['start']<=t<w['end']+.10),None)
  caption=' '.join(w['text'] for w in words[max(0,(wi or 0)//4*4):min(len(words),((wi or 0)//4+1)*4)]) if wi is not None else ''
  frame=paint(i,story,stage,progress,caption,duration,n)
  proc.stdin.write(frame.tobytes())
 proc.stdin.close()
 if proc.wait():raise RuntimeError('ffmpeg frames failed')
 track=ROOT.parent/'assets/trilha.mp3'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(voice),'-stream_loop','-1','-i',str(track),'-filter_complex','[1:a]volume=1.0[a];[2:a]volume=0.15[b];[a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[o]','-map','0:v','-map','[o]','-t',str(duration),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(final)],check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'],check=True)
 print(story['name'],round(duration,1),str(final),flush=True)

async def main():
 for i,s in enumerate(STORIES):await produce(i,s)
asyncio.run(main())
