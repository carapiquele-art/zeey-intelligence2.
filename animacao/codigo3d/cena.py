import bpy,sys,math,json,os
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parent
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
K=int(args[0]) if args else 0
PREVIEW='--preview' in args
FPS=12;TOTAL=132
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.display.shading.curvature_ridge_factor=1.3;scene.display.shading.curvature_valley_factor=1.1;scene.render.film_transparent=False
scene.render.resolution_x=480;scene.render.resolution_y=832;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=TOTAL
scene.world.color=(.08,.10,.16);scene.view_settings.view_transform='AgX'
scene.render.film_transparent=False
M={}
def mat(name,c,metal=0,rough=.55,emit=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emit:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=emit
 M[name]=m;return m
for n,c in [('navy',(.018,.035,.10)),('blue',(.012,.16,.95)),('white',(.86,.90,.98)),('skin',(.58,.30,.16)),('hair',(.042,.022,.014)),('black',(.005,.008,.015)),('wood',(.25,.11,.045)),('wall',(.075,.11,.20)),('grey',(.16,.21,.3)),('cream',(.92,.78,.54)),('pink',(.75,.3,.27)),('green',(.03,.55,.24))]:mat(n,c)
mat('glow',(.03,.35,1),.1,.25,3);mat('lamp',(1,.67,.26),0,.3,4);mat('screen',(.025,.16,.5),0,.2,.6);M['blue'].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.27

def empty(name,loc=(0,0,0),parent=None):
 o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);o.location=loc
 if parent:o.parent=parent
 return o

def cube(name,loc,dim,material='navy',bevel=.04,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(M[material])
 if bevel:
  m=o.modifiers.new('Bordas suaves','BEVEL');m.width=bevel;m.segments=2
  o.modifiers.new('Normais','WEIGHTED_NORMAL')
 if parent:o.parent=parent
 return o

def sphere(name,loc,dim,material='black',parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=loc);o=bpy.context.object;o.name=name;o.scale=dim;o.data.materials.append(M[material]);bpy.ops.object.shade_smooth()
 if parent:o.parent=parent
 return o

def text(body,loc,size=.2,material='white',parent=None):
 bpy.ops.object.text_add(location=loc);o=bpy.context.object;o.data.body=body;o.data.size=size;o.data.align_x='CENTER';o.data.extrude=.001;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(M[material])
 if parent:o.parent=parent
 return o

def key(o,frame,loc=None,rot=None,scale=None):
 if loc is not None:o.location=loc;o.keyframe_insert('location',frame=frame)
 if rot is not None:o.rotation_euler=rot;o.keyframe_insert('rotation_euler',frame=frame)
 if scale is not None:o.scale=scale;o.keyframe_insert('scale',frame=frame)

def hero(loc=(0,0,0),woman=False):
 root=empty('Pessoa',loc);cube('sapato E',(-.23,0,.18),(.37,.65,.3),'black',parent=root);cube('sapato D',(.23,0,.18),(.37,.65,.3),'black',parent=root)
 cube('perna E',(-.23,.04,.65),(.32,.42,.8),'navy',parent=root);cube('perna D',(.23,.04,.65),(.32,.42,.8),'navy',parent=root)
 cube('tronco',(0,0,1.36),(.94,.54,.9),'blue',parent=root);cube('camisa',(0,-.28,1.5),(.35,.025,.55),'white',.01,parent=root)
 head=empty('cabeca',(0,0,2.03),root);cube('rosto',(0,-.025,.13),(.9,.69,.85),'skin',.1,parent=head)
 cube('cabelo',(0,.01,.54),(1,.73,.33),'hair',.07,parent=head);cube('franja',(-.27,-.35,.45),(.47,.1,.22),'hair',.015,parent=head)
 if woman:
  cube('coque',(0,.41,.57),(.52,.4,.5),'hair',.09,parent=head)
  cube('avental',(0,-.31,1.24),(.7,.025,.68),'white',.02,parent=root)
 for x in [-.22,.22]:
  cube('olho',(x,-.379,.17),(.12,.025,.105),'black',.02,parent=head)
  brow=cube('sobrancelha',(x,-.385,.34),(.20,.04,.065),'hair',.02,parent=head)
  if x<0:
   key(brow,1,rot=(0,0,0));key(brow,46,rot=(0,math.radians(-20),0));key(brow,92,rot=(0,math.radians(10),0))
 cube('nariz',(0,-.4,.04),(.13,.13,.14),'skin',.04,parent=head)
 cube('boca',(0,-.385,-.13),(.18,.025,.05),'black',.02,parent=head)
 arms=[]
 for side in [-1,1]:
  arm=empty('braco',(.63*side,0,1.63),root);cube('manga',(0,0,-.17),(.29,.4,.42),'blue',parent=arm);cube('antebraco',(0,-.02,-.53),(.27,.31,.38),'skin',parent=arm);cube('mao',(0,-.04,-.76),(.30,.34,.28),'skin',parent=arm);arms.append(arm)
 return root,head,arms

# Cenário
cube('piso',(0,1,-.10),(12,10,.2),'grey');cube('parede fundo',(0,3,2.2),(12,.18,4.6),'wall');cube('parede lateral',(-4.8,.2,2.2),(.18,6,4.6),'navy')
for x in [-3.7,-1.9,.0,1.9,3.7]:
 cube('janela',(x,2.89,2.9),(1.5,.08,1.6),'navy',.02)
 for z in [2.5,3.15]:cube('reflexo janela',(x+.25,2.83,z),(.16,.035,.35),'screen',.01)
cube('viga azul',(0,2.72,4.17),(10,.2,.16),'blue')
for z in [1.1,1.8,2.5]:
 cube('prateleira',(3.6,2.1,z),(1.6,.7,.09),'wood')
 for j in range(4):cube('caixa',(3.05+j*.35,2.1,z+.19),(.24,.30,.3),['white','blue','cream','navy'][j],.02)
# Luminária acima
cube('luz teto',(0,0,4.2),(2.2,.8,.1),'lamp')

def laptop(loc,parent=None):
 cube('base notebook',loc,(.95,.65,.07),'navy',parent=parent)
 screen=cube('tela notebook',(loc[0],loc[1]+.24,loc[2]+.36),(.95,.07,.67),'navy',parent=parent)
 cube('tela azul',(loc[0],loc[1]+.195,loc[2]+.36),(.83,.014,.53),'screen',.015,parent=parent)
 for i in range(3):cube('linha interface',(loc[0]+.1,loc[1]+.182,loc[2]+.49-i*.12),(.46,.009,.035),'white',.005,parent=parent)

person,head,arms=hero((-.65,.2,0),woman=K==1)
# Móveis e adereços de cada negócio
if K==0:
 cube('carro',(-2.4,.8,1.3),(2.1,2.8,.85),'white',.14);cube('cabine',(-2.4,1.2,1.95),(1.7,1.35,.65),'navy',.12)
 for x in [-3.35,-1.45]:
  for y in [-.25,1.65]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.4,depth=.23,location=(x,y,.92),rotation=(0,math.pi/2,0));bpy.context.object.data.materials.append(M['black'])
 cube('bancada',(1.7,.6,1.05),(2.5,1,.18),'wood');cube('base bancada',(1.7,.6,.5),(2.2,.8,1),'navy')
 cube('armario ferramentas',(-.3,2.6,1.5),(1.3,.18,1.5),'navy')
 for i in range(6):cube('ferramenta',(-.8+i*.2,2.45,1.6),(.05,.06,.65),'white',.015)
 laptop((2.25,.55,1.18));text('OFICINA',(-2.5,2.72,3.98),.32)
elif K==1:
 cube('balcao',(0,-.5,1.05),(3.6,1.15,.17),'wood');cube('base balcao',(0,-.5,.5),(3.4,1.0,1),'navy')
 for z,r in [(1.2,.55),(1.46,.48),(1.68,.4)]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=.22,location=(-.55,-.63,z));o=bpy.context.object;o.data.materials.append(M['cream']);o.modifiers.new('bordas','BEVEL').width=.04
 for a in range(8):sphere('morango',(-.55+.34*math.cos(a*math.pi/4),-.63+.34*math.sin(a*math.pi/4),1.83),(.065,.065,.07),'pink')
 laptop((1.1,-.4,1.17));text('FEITO COM CARINHO',(-1.0,2.76,3.98),.24)
else:
 cube('mesa',(0,-.4,1.05),(3.5,1.3,.17),'wood');cube('gaveteiro',(-1.0,-.25,.49),(.7,1.0,1),'navy');cube('perna mesa',(1.4,-.2,.5),(.12,.8,1),'blue')
 laptop((-.5,-.45,1.17))
 for j in range(4):
  paper=cube('papel',(j*.33-.3,-.83,1.17+j*.014),(.55,.4,.015),'white',0)
  paper.rotation_euler[2]=j*.21
  key(paper,1);key(paper,50,loc=(j*.33-.3,-.83,1.17+j*.014));key(paper,94,loc=(1.13,-.15,1.2+j*.035))
 text('SEU NEGÓCIO',(-1.0,2.76,3.98),.29)
# Celular e notificação
phonepos=(1.4,-.72,1.18) if K!=0 else (1.15,.23,1.18)
cube('celular',phonepos,(.35,.63,.07),'black',.06);cube('tela celular',(phonepos[0],phonepos[1],phonepos[2]+.045),(.29,.52,.016),'screen',.03)

# Z a partir do contorno real da marca
Z=empty('Z vivo',(1.9,-.6,2.22))
curve=bpy.data.curves.new('forma da marca','CURVE');curve.dimensions='2D';curve.fill_mode='BOTH';curve.extrude=.12;curve.bevel_depth=.055;curve.bevel_resolution=3
points=json.loads((ROOT/'z-contorno.json').read_text());spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
for pt,(x,z) in zip(spline.points,points):pt.co=(x,z,0,1)
spline.use_cyclic_u=True
obj=bpy.data.objects.new('símbolo Z',curve);scene.collection.objects.link(obj);obj.rotation_euler[0]=math.pi/2;obj.data.materials.append(M['blue']);obj.parent=Z
for x in [-.22,.22]:
 sphere('olho Z',(x,-.205,.42),(.075,.045,.12),'black',Z);sphere('brilho Z',(x-.025,-.245,.47),(.021,.01,.03),'white',Z)
mouth=sphere('boca Z',(.14,-.21,.10),(.10,.03,.07),'black',Z)
for side in [-1,1]:cube('mao Z',(side*.78,-.04,.02),(.20,.22,.20),'white',.055,Z)
for f in range(1,TOTAL+1,6):
 sec=f/FPS
 z=2.22+.09*math.sin(sec*3)
 x=1.9-.45*min(max((sec-4)/3,0),1)
 key(Z,f,loc=(x,-.65,z),rot=(0,.06*math.sin(sec*2),.05*math.sin(sec*2.5)))
 key(mouth,f,scale=(.10,.03,.04+.06*abs(math.sin(sec*7))))
# Cartes qui visualisent l'information transférée
for j in range(3):
 card=empty('demande '+str(j),(phonepos[0],phonepos[1],phonepos[2]+.2));cube('carte',(0,0,0),(.80,.06,.46),'screen',.07,card)
 for n in range(2):cube('ligne',(.07,-.042,.1-n*.14),(.43,.012,.025),'white',.006,card)
 cube('puce',(-.27,-.047,.03),(.10,.014,.1),'blue',.015,card)
 start=25+j*16;end=80+j*15
 key(card,1,scale=(.001,.001,.001));key(card,start,scale=(.001,.001,.001));key(card,start+5,scale=(1,1,1));key(card,start+9,loc=(phonepos[0],-.8,2.45+j*.12));key(card,end,loc=(.35,.35,2.0+j*.22));key(card,130,scale=(.1,.1,.1))
# La liaison bleue apparaît lorsque Z explique
c=bpy.data.curves.new('pont des informations','CURVE');c.dimensions='3D';c.bevel_depth=.035;c.bevel_resolution=2;s=c.splines.new('BEZIER');s.bezier_points.add(2)
for v,co in zip(s.bezier_points,[(phonepos[0],phonepos[1],1.3),(1.45,-.1,2.6),(.0,.3,1.9)]):v.co=co;v.handle_left_type='AUTO';v.handle_right_type='AUTO'
o=bpy.data.objects.new('pont bleu',c);scene.collection.objects.link(o);c.materials.append(M['glow']);c.bevel_factor_end=0;c.keyframe_insert('bevel_factor_end',frame=1);c.keyframe_insert('bevel_factor_end',frame=60);c.bevel_factor_end=1;c.keyframe_insert('bevel_factor_end',frame=97)
# Gestes du personnage
for f in range(1,TOTAL+1,6):
 sec=f/FPS
 angle= -.7-.20*math.sin(sec*7) if sec<3 else -.15 if sec<5 else -.45
 key(arms[0],f,rot=(angle,0,-.15));key(arms[1],f,rot=(angle*.8,0,.12))
 key(head,f,rot=(.03*math.sin(sec*3),0,.0 if sec<3 else -.18 if sec<6 else .12))
# Éclairage
for name,loc,power,size,color in [('principale',(2,-4,7),1000,5,(.72,.84,1)),('chaude',(-4,-1,4),800,3,(1,.59,.28)),('fond',(0,3,4),1000,3,(.13,.36,1))]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.name=name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.data.color=color;l.rotation_euler=(Vector((0,0,1.4))-l.location).to_track_quat('-Z','Y').to_euler()
# Caméra douce; le cadrage laisse une marge aux sous-titres
bpy.ops.object.camera_add(location=(6,-10,6));cam=bpy.context.object;scene.camera=cam;cam.data.lens=56
focus=empty('cible',(0,.25,1.65));constraint=cam.constraints.new('TRACK_TO');constraint.target=focus;constraint.track_axis='TRACK_NEGATIVE_Z';constraint.up_axis='UP_Y'
for f,pos in [(1,(6,-10,5.8)),(44,(5.4,-9.4,5.2)),(84,(5.6,-9.2,5.15)),(TOTAL,(5,-8.7,4.8))]:key(cam,f,loc=pos)
for action in bpy.data.actions:
 for fc in action.fcurves:
  for k in fc.keyframe_points:k.interpolation='BEZIER'
scene.render.filepath=str(ROOT/f'filme_rapido{K+1}'/'frame_');(ROOT/f'filme_rapido{K+1}').mkdir(exist_ok=True)
if PREVIEW:
 scene.frame_set(72);scene.render.filepath=str(ROOT/f'previa_rapida{K+1}.png');bpy.ops.render.render(write_still=True)
else:bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'filme{K+1}.blend'));bpy.ops.render.render(animation=True)
