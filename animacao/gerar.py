"""Geração animada gratuita, com autenticação local e retomada por cena."""
import argparse,asyncio,getpass,json,os,shutil,subprocess,sys,urllib.request,urllib.error,uuid
from pathlib import Path
from legendar import export,run

ROOT=Path(__file__).resolve().parent
BASE='https://cbensimon-wan2-2-fp8da-aoti-preview2.hf.space'
TOKEN_FILE=Path.home()/'.config/zeey/hf_token'

class GenerationUnavailable(RuntimeError):pass

def token():
 value=os.environ.get('HF_TOKEN','').strip()
 if not value and TOKEN_FILE.exists():value=TOKEN_FILE.read_text().strip()
 return value

def login():
 value=getpass.getpass('Cole seu token de LEITURA do Hugging Face (fica oculto): ').strip()
 if not value.startswith('hf_'):raise SystemExit('Token inválido. Crie um token de leitura em https://huggingface.co/settings/tokens .')
 req=urllib.request.Request('https://huggingface.co/api/whoami-v2',headers={'Authorization':'Bearer '+value})
 try:
  with urllib.request.urlopen(req,timeout=25) as r:json.load(r)
 except Exception:raise SystemExit('Não foi possível autenticar. Confira o token e a conexão; nenhum token foi salvo.')
 TOKEN_FILE.parent.mkdir(parents=True,exist_ok=True)
 fd=os.open(TOKEN_FILE,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
 with os.fdopen(fd,'w') as f:f.write(value)
 os.chmod(TOKEN_FILE,0o600)
 print('Conta autenticada. Token salvo somente neste aparelho, fora do repositório.')

def call(path,value,body=None,ctype=None,timeout=60):
 # Credencial enviada apenas ao Space selecionado. Downloads de resultado não levam token.
 headers={'User-Agent':'Zeey-Animation','X-HF-Authorization':'Bearer '+value}
 if ctype:headers['Content-Type']=ctype
 req=urllib.request.Request(BASE+path,data=body,headers=headers)
 with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()

def animate(image,prompt,dest,value):
 boundary='Zeey'+uuid.uuid4().hex
 data=(f'--{boundary}\r\nContent-Disposition: form-data; name="files"; filename="{image.name}"\r\nContent-Type: image/jpeg\r\n\r\n').encode()+image.read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
 uploaded=json.loads(call('/gradio_api/upload',value,data,'multipart/form-data; boundary='+boundary))[0]
 f={'path':uploaded,'url':BASE+'/gradio_api/file='+uploaded,'orig_name':image.name,'meta':{'_type':'gradio.FileData'}}
 inputs=[f,None,prompt,6,'blurry, distorted, watermark, text, extra limbs, static',3.5,1,1,42,True,6,'UniPCMultistep',3.0,16,False,True]
 event=json.loads(call('/gradio_api/call/generate_video',value,json.dumps({'data':inputs,'session_hash':uuid.uuid4().hex}).encode(),'application/json'))['event_id']
 stream=call('/gradio_api/call/generate_video/'+event,value,timeout=240).decode()
 result=None
 for block in stream.split('\n\n'):
  if block.startswith('event: error'):
   # O serviço também retorna erro nulo ao acabar a cota. Parar, sem tentativas em loop.
   raise GenerationUnavailable('O Space interrompeu a geração. Verifique a cota da conta ou o estado do serviço. As cenas prontas foram preservadas.')
  if block.startswith('event: complete'):
   raw=next(x[6:] for x in block.splitlines() if x.startswith('data: '));result=json.loads(raw);break
 if not result or not result[0]:raise GenerationUnavailable('O serviço não devolveu um vídeo; produção pausada sem perder cenas concluídas.')
 item=result[0];url=item.get('url') if isinstance(item,dict) else BASE+'/gradio_api/file='+str(item)
 if not url:raise GenerationUnavailable('O serviço terminou sem endereço de vídeo.')
 tmp=dest.with_suffix('.partial.mp4')
 try:
  with urllib.request.urlopen(url,timeout=90) as r, tmp.open('wb') as f:shutil.copyfileobj(r,f)
  run(['ffmpeg','-v','error','-i',str(tmp),'-f','null','-']);tmp.replace(dest)
 finally:
  if tmp.exists():tmp.unlink()

def gallery(path):
 movies=Path.home()/'storage/movies'
 if not movies.is_dir():return
 try:
  folder=movies/'Zeey';folder.mkdir(exist_ok=True);dest=folder/path.name;shutil.copy2(path,dest)
  if shutil.which('termux-media-scan'):subprocess.run(['termux-media-scan',str(dest)],capture_output=True)
  print('Cópia em Movies/Zeey:',dest.name,flush=True)
 except OSError:print('Vídeo salvo na pasta saida; não foi possível copiar para a galeria.',flush=True)

async def main():
 parser=argparse.ArgumentParser();parser.add_argument('--login',action='store_true');parser.add_argument('--historia',choices=['todas','1','2','3'],default='todas');parser.add_argument('--diagnostico',action='store_true');args=parser.parse_args()
 if args.login:login();return
 stories=json.loads((ROOT/'historias.json').read_text());out=ROOT/'saida';out.mkdir(exist_ok=True)
 if args.diagnostico:
  for tool in ['ffmpeg','ffprobe']:
   if not shutil.which(tool):raise SystemExit('Falta instalar '+tool)
  for s in stories:
   if not (ROOT/'assets'/(s['name']+'.jpg')).is_file():raise SystemExit('Falta imagem de '+s['name'])
  print('Arquivos e ferramentas disponíveis. Token local:', 'configurado' if token() else 'não configurado');return
 value=token()
 if not value:raise SystemExit('Primeiro execute: python gerar.py --login . Não envie seu token na conversa ou no GitHub.')
 selected=range(3) if args.historia=='todas' else [int(args.historia)-1]
 for i in selected:
  s=stories[i];final=out/(s['name']+'_Zeey.mp4')
  if final.exists():print('Já concluído:',final.name);gallery(final);continue
  frame=ROOT/'assets'/(s['name']+'.jpg');clips=[]
  for j,prompt in enumerate(s['prompts']):
   clip=out/f"{s['name']}_c{j}.mp4"
   if not clip.exists():
    print(f"Gerando {s['name']}, cena {j+1}/4...",flush=True)
    try:await asyncio.to_thread(animate,frame,prompt,clip,value)
    except Exception as e:
     message=str(e).replace(value,'[credencial ocultada]')
     raise SystemExit(message)
   clips.append(clip)
   if j<3:
    frame=out/f"{s['name']}_quadro{j}.jpg";run(['ffmpeg','-v','error','-y','-sseof','-0.08','-i',str(clip),'-frames:v','1','-q:v','2',str(frame)])
  final=await export(s['name']+'_Zeey',clips,s['voice']);gallery(final)

if __name__=='__main__':asyncio.run(main())
