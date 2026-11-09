import asyncio,json,os
from pathlib import Path
import edge_tts
P=Path(__file__).resolve().parent
async def main():
 data=json.loads((P/'roteiros.json').read_text())
 for x in data:
  c=edge_tts.Communicate(x['text'],'pt-BR-FranciscaNeural' if x['id']!='Beto' else 'pt-BR-AntonioNeural',rate='+30%',pitch='+3Hz',boundary='WordBoundary',proxy=os.environ.get('HTTPS_PROXY'))
  words=[]
  with (P/'public'/f"{x['id']}.mp3").open('wb') as f:
   async for k in c.stream():
    if k['type']=='audio':f.write(k['data'])
    elif k['type']=='WordBoundary':words.append({'text':k['text'],'start':k['offset']/1e7,'end':(k['offset']+k['duration'])/1e7})
  tokens=x['text'].split()
  if len(tokens)!=len(words):raise RuntimeError(f"Tempo de palavra divergente em {x['id']}")
  for w,t in zip(words,tokens):w['text']=t
  x['words']=words;x['duration']=round(words[-1]['end']+1,2)
 (P/'src/data.json').write_text(json.dumps(data,ensure_ascii=False))
asyncio.run(main())
