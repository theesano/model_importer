import newGameLib
from newGameLib import *
import Blender	

########################
# IMPORT
########################
			
	
def xmlParser(filename):
	matFile=filename.split('.model')[0]+'.model_data'+os.sep+'materials.xml'
	if os.path.exists(matFile)==True:
		materials={}
		xml=Xml()
		xml.input=open(matFile,'r')
		xml.parse()	
		materialNodeList=xml.find(xml.root,'Material')
		for materialNode in materialNodeList:
			chunks=materialNode.chunks
			materials[chunks['name']]={}
			materials[chunks['name']]['diffuse']=None
			materials[chunks['name']]['normalmap']=None
			materials[chunks['name']]['specularmap']=None
			if 'diffuse' in chunks:
				materials[chunks['name']]['diffuse']=chunks['diffuse']
			if 'normalmap' in chunks:	
				materials[chunks['name']]['normalmap']=chunks['normalmap']
			if 'specularmap' in chunks:	
				materials[chunks['name']]['specularmap']=chunks['specularmap']
		return materials
	else:
		return None
	
def modelParser(filename,g):
	matList=[]	
	g.seek(8)
	mesh=None
	skeleton=None
	skin=None
	material=None
	while(True):
		chunk = g.i(1)[0]
		if chunk==0:
			name = g.word(4)
			seek = g.i(1)[0]
			back = g.tell() 
			if name=='SRTM':
				materials=xmlParser(filename)				
				g.tell()
				matCount=g.i(1)[0]
				for m in range(matCount):
					material=Mat()
					g.i(1)
					g.word(4)
					g.i(1)
					g.H(1)
					matName=g.word(g.i(1)[0])
					g.i(1)
					g.seek(26,1)
					texDir=g.dirname
					diffuse=texDir+os.sep+g.word(g.i(1)[0])
					specular=texDir+os.sep+g.word(g.i(1)[0])
					normal=texDir+os.sep+g.word(g.i(1)[0])
					g.tell()
					g.i(1)
					g.word(g.i(1)[0])
					g.i(7)
					g.word(g.i(1)[0])
					g.word(g.i(1)[0])
					g.read(g.i(1)[0])
					g.i(4)
					g.tell()
					if materials!=None:
						texDir=g.dirname
						if matName in materials:
							if materials[matName]['diffuse'] is not None:
								material.diffuse=texDir+os.sep+materials[matName]['diffuse']
							if materials[matName]['normalmap'] is not None:
								material.normal=texDir+os.sep+materials[matName]['normalmap']
							if materials[matName]['specularmap'] is not None:
								material.specular=texDir+os.sep+materials[matName]['specularmap']
					matList.append(material)
					g.word(4)
			if name == 'HSMV':
				g.word(4)
				g.i(1)[0],g.f(1)[0],g.i(1)[0]
				v=g.B(15*4)
				nVerts = g.i(1)[0]
				g.B(13)
				nFaces = g.i(1)[0] 
				g.seek(back+108)
				mesh=Mesh()
				mesh.filename=filename
				mesh.mod=True
				mesh.TRIANGLE=True
				for m in range(nVerts):
					t=g.tell()
					mesh.vertPosList.append(g.f(3))
					mesh.vertModList.append([m,t,'f'])
					g.seek(t+v[16])
					mesh.vertUVList.append(g.f(2))
					g.seek(t+v[8])
				mesh.indiceList=g.H(nFaces*3)
			if name == 'LEKS':
				skeleton=Skeleton()
				skeleton.BONESPACE=True
				g.H(1)[0]
				nBones = g.H(1)[0]
				for m in range(nBones):
					bone=Bone()
					bone.name=g.word(g.i(1)[0])[-25:]
					bone.parentID=g.h(1)[0]
					g.f(3)
					g.f(4)
					bone.posMatrix=TranslationMatrix(Vector(g.f(3)))
					qx,qy,qz,qw = g.f(4)
					bone.rotMatrix=Quaternion(qw,qx,qy,qz).toMatrix().invert()
					skeleton.boneList.append(bone)
				skeleton.draw()	
			if name == 'THGW':
				g.H(2)
				skin=Skin()
				for m in range(nVerts):
					nGr = g.H(1)[0]
					indices=[]
					weights=[]
					for n in range(nGr):
						indices.append(g.H(1)[0])
						g.B(1)
						weights.append(g.B(1)[0]/255.0)
					mesh.skinIndiceList.append(indices)
					mesh.skinWeightList.append(weights)
					
			if name=='MBUS':
				g.i(3)
				for m in range(g.i(1)[0]):
					v=g.i(8)
					g.f(6)
					w=g.i(2)
					matID=w[0]
					if len(matList)!=0:
						material=matList[matID]
						material.TRIANGLE=True
						material.IDStart=v[0]
						material.IDCount=v[1]
						mesh.matList.append(material)
						
				
			g.seek(back+seek)
			g.i(1)[0]
			g.word(4)
		elif chunk==-1:break
		else:
			print 'unknow chunk',chunk
			break 
		
		
	if mesh is not None:
		if skeleton is not None:
			if skin is not None:
				skin.boneMap=skeleton.boneNameList
				mesh.skinList.append(skin)	
		if skeleton is not None:
			mesh.BINDSKELETON='armature'
		#if material is not None:	
		#	mesh.facesgroupslist.append(material)		
		mesh.draw()
	
		
	
def SOPB(boneCount,g):
	actionFile.write('SOPB')
	frameCount=g.i(1)[0]
	p.i([frameCount])
	for m in range(frameCount):
		actionFile.write(g.read(4+boneCount*12))
			
		
def TORB(boneCount,g):
	actionFile.write('TORB')
	frameCount=g.i(1)[0]
	p.i([frameCount])
	for m in range(frameCount):
		actionFile.write(g.read(4+boneCount*16))
	
	
		
def DAEH(g):
	chunk = g.i(1)[0]
	name = g.word(4)
	size = g.i(1)[0]
	back = g.tell()
	animCount=g.i(1)[0]
	g.seek(back+size)	
	chunk = g.i(1)[0]
	name = g.word(4)
	return animCount

def LEKS(g):
	global skeleton
	chunk = g.i(1)[0]
	name = g.word(4)
	size = g.i(1)[0]
	back = g.tell()
	A=g.H(2)
	skeleton=Skeleton()
	skeleton.BONESPACE=True
	for m in range(A[1]):
		bone=Bone()
		skeleton.boneList.append(bone)
		bone.name=g.word(g.i(1)[0])
		bone.parentID=g.h(1)[0]
		parentPosMatrix=VectorMatrix(g.f(3))
		parentRotMatrix=QuatMatrix(g.f(4)).resize4x4()
		parentMatrix=parentRotMatrix.invert()*parentPosMatrix
		posMatrix=VectorMatrix(g.f(3))
		rotMatrix=QuatMatrix(g.f(4)).resize4x4()
		matrix=rotMatrix.invert()*posMatrix
		bone.matrix=matrix#*parentMatrix
	skeleton.draw()	
	g.H(1)[0]
	chunk = g.i(1)[0]
	name = g.word(4)
	
		
		
def INAB(g):
	global actionFile,p
	chunk = g.i(1)[0]
	name = g.word(4)
	size = g.i(1)[0]
	back = g.tell()
	value=g.H(3)
	boneCount=value[2]
	animName=g.word(g.i(1)[0])	
	actionPath=g.dirname+os.sep+g.basename+'_animfiles'
	if os.path.exists(actionPath)==False:
		os.makedirs(actionPath)
	actionFile=open(actionPath+os.sep+animName+'.action','wb')
	p=BinaryReader(actionFile)	
	p.i([len(skeleton.boneNameList)])
	for name in skeleton.boneNameList:
		actionFile.write(name+'\x00')
	
	start=g.tell()
	sum=0
	while(True):
		g.i(1)[0]
		iname = g.word(4)
		isize = g.i(1)[0]
		iback = g.tell()
		if iname=='SOPB':SOPB(boneCount,g)
		elif iname=='TORB':TORB(boneCount,g)
		
		g.seek(iback+isize)
		g.i(1)[0]
		g.word(4)
		sum+=4+4+4+4+4+isize
		if sum>=size-20:break	
	g.seek(start)	
	
	actionFile.close()
		
		
	g.seek(back+size)
	chunk = g.i(1)[0]
	name = g.word(4)
	
			
		
def MINA(size,g):
	sum=0
	g.H(1)		
	animCount=DAEH(g)
	LEKS(g)
	for m in range(animCount):
		INAB(g)
	
def animParser(filename,g):
	g.seek(8)
	while(True):
		if g.tell()>=g.fileSize():break
		chunk = g.i(1)[0]
		if chunk==0:
			name = g.word(4)
			size = g.i(1)[0]
			back = g.tell()
			if size!=-1:
				if name=='MINA':	
					MINA(size,g)
				g.seek(back+size)
				
	g.tell()
		
		
def actionParser(filename,g):
	action=Action()
	action.name=g.basename
	action.BONESPACE=True
	action.BONESORT=True
	boneCount=g.i(1)[0]
	for n in range(boneCount):
		bone=ActionBone()
		bone.name=g.find('\x00')
		action.boneList.append(bone)
	while(True):
		if g.tell()>=g.fileSize():break
		chunk=g.word(4)
		if chunk=='TORB':
			frameCount=g.i(1)[0]
			for m in range(frameCount):
				time=g.f(1)[0]*33
				for n in range(boneCount):
					value=g.f(4)
					bone=action.boneList[n]
					bone.rotFrameList.append(time)
					bone.rotKeyList.append(QuatMatrix(value).invert().resize4x4())
		if chunk=='SOPB':
			frameCount=g.i(1)[0]
			for m in range(frameCount):
				time=g.f(1)[0]*33
				for n in range(boneCount):
					value=g.f(3)
					bone=action.boneList[n]
					bone.posFrameList.append(time)
					bone.posKeyList.append(VectorMatrix(value))
	action.draw()
	action.setContext()
				
			
	
def Parser(filename):	
	ext=filename.split('.')[-1].lower()	
	
	
		
	if ext=='model':
		file=open(filename,'rb')
		g=BinaryReader(file)
		modelParser(filename,g)
		file.close()
	
	if ext=='anim':
		file=open(filename,'rb')
		g=BinaryReader(file)
		animParser(filename,g)
		file.close()
		
	if ext=='action':
		file=open(filename,'rb')
		g=BinaryReader(file)
		#g.logOpen()
		actionParser(filename,g)
		#g.logClose()
		file.close()
		
	if ext=='bak':
		file=open(filename,'rb')
		g=BinaryReader(file)
		modelParser(filename,g)
		file.close()
	
 
	
Blender.Window.FileSelector(Parser,'import','SELECT: *.model, *.anim, *.action, *.bak') 
	