import asyncio,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from legendar import export
TEXTS=json.loads((ROOT/'textos.json').read_text())
async def main():
 for i,text in enumerate(TEXTS,1):
  frames=ROOT/f'filme_rapido{i}'
  count=len(list(frames.glob('frame_*.png')))
  if count!=132:raise RuntimeError(f'Filme {i}: {count}/132 quadros')
  clip=ROOT/f'cena{i}.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-framerate','12','-i',str(frames/'frame_%04d.png'),'-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clip)],check=True)
  final=await export(f'Zeey_{i:02}',[clip],text)
  print(final,flush=True)
asyncio.run(main())
