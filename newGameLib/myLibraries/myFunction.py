import bpy
import Blender,os	
from Blender.Mathutils import *
import types
from Blender.Draw import *
import math
from math import *

blendDir=os.path.dirname(Blender.Get('filename'))
toolDir=None
if os.path.exists(blendDir+os.sep+'tools')==True:
	toolDir=blendDir+os.sep+'tools'
elif os.path.exists(blendDir+os.sep+'newgameLib/tools')==True:
	toolDir=blendDir+os.sep+'newgameLib/tools'

#invert string string[::-1]

def safe(count):
	COUNT=0
	if count<100000:
		COUNT=count
	else:
		print 'WARNING:count:',count
	return COUNT	
	
	
class Input(object):
	def __init__(self,flagList):
		self.flagList=flagList
		self.type=None
		self.debug=None
		self.imageList=[]
		if type(flagList)==types.InstanceType:
			self.type='instance'
			self.filename=flagList.assetPath
			self.output=flagList
			self.returnList=self.flagList.returnList
			self.returnKey=self.flagList.returnKey
		if type(flagList)==types.StringType:
			self.type='string'
			self.filename=flagList
			
def Input1(object):
	return object	
			
def Output(object):	
	return object
			
		

def Float255(data):
	list=[]
	for get in data:
		list.append(get/255.0)
	return list	


def pm(message,n):
	print ' '*4*n,message

	
	
if toolDir is not None:	
	bmsDir=toolDir+os.sep+'quickbms'
	bmsExe=bmsDir+os.sep+'quickbms.exe'
	bmsScriptDir=bmsDir+os.sep+'scripts'
	
class Bms(object):
	def __init__(self):
		self.input=input
		self.output=''
		self.bms=None
		self.command=' '#' -d -o '
		
	def run(self):
		if self.bms is not None:
			self.bms=bmsScriptDir+os.sep+self.bms
			commandline = bmsExe +self.command+self.bms+ ' ' + self.input + ' '+self.output
			print commandline
			os.system(commandline)
			
		
	
class Sys(object):
	def __init__(self,input):
		self.input=input
		if '.' in os.path.basename(input):
			self.ext=os.path.basename(input).split('.')[-1]
		else:
			self.ext=''
		if '.' in os.path.basename(input):
			self.base=os.path.basename(input).split('.'+self.ext)[0]
		else:
			self.base=os.path.basename(input)+'Dir'
		self.dir=os.path.dirname(input)
		self.blendFile=Blender.Get('filename')
	def	Dir(self,base):
		newDir=self.dir+os.sep+base
		if os.path.exists(newDir)==False:
			os.makedirs(newDir)
	def	addDir(self,base):
		newDir=self.dir+os.sep+base
		if os.path.exists(newDir)==False:
			os.makedirs(newDir)
	
	
def isQuat(quat):
	sum=quat[1]**2+quat[2]**2+quat[3]**2
	return quat[0]**2-sum	
	
	
	
def quatDecompress3(s0,s1,s2):  
	tmp0= s0>>15 
	tmp1= (s1*2+tmp0) & 0x7FFF
	s0= s0 & 0x7FFF ;
	tmp2= s2*4 ;
	tmp2= (s2*4+ (s1>>14)) & 0x7FFF ;
	s1= tmp1 ;
	AxisFlag= s2>>13 ;
	#AxisFlag = ((s1 & 1) << 1) | (s2 & 1)
	s2= tmp2 ;
	f0 = 1.41421*(s0-0x3FFF)/0x7FFF ;
	f1 = 1.41421*(s1-0x3FFF)/0x7FFF ;
	f2 = 1.41421*(s2-0x3FFF)/0x7FFF ;  
	f3 = sqrt(1.0-(f0*f0+f1*f1+f2*f2)) 
	#print AxisFlag
	if AxisFlag==3:
		x= f2
		y= f1
		z= f0
		w= f3
	if AxisFlag==2:x= f2;y= f1;z= f3;w= f0
	if AxisFlag==1:x= f2;y= f3;z= f1;w= f0
	if AxisFlag==0:x= f3;y= f2;z= f1;w= f0
	print x,y,z,w  
	return x,y,z,w  

	
	
def quatDecompress(s0,s1,s2):  
	tmp0= s0>>15 
	tmp1= (s1*2+tmp0) & 0x7FFF
	s0= s0 & 0x7FFF ;
	tmp2= s2*4 ;
	tmp2= (s2*4+ (s1>>14)) & 0x7FFF ;
	s1= tmp1 ;
	AxisFlag= s2>>13 ;
	#AxisFlag = ((s1 & 1) << 1) | (s2 & 1)
	s2= tmp2 ;
	f0 = 1.41421*(s0-0x3FFF)/0x7FFF ;
	f1 = 1.41421*(s1-0x3FFF)/0x7FFF ;
	f2 = 1.41421*(s2-0x3FFF)/0x7FFF ;  
	f3 = sqrt(1.0-(f0*f0+f1*f1+f2*f2)) 
	#print AxisFlag
	if AxisFlag==3:
		x= f2
		y= f1
		z= f0
		w= f3
	if AxisFlag==2:x= f2;y= f1;z= f3;w= f0
	if AxisFlag==1:x= f2;y= f3;z= f1;w= f0
	if AxisFlag==0:x= f3;y= f2;z= f1;w= f0
	#print x,y,z,w  
	return x,y,z,w  
	
def QuatMatrix(quat):
	return Quaternion(quat[3],quat[0],quat[1],quat[2]).toMatrix()	
	
	
def VectorMatrix(vector):
	return TranslationMatrix(Vector(vector))		
	
	
def roundVector(vec,dec=17):
	fvec=[]
	for v in vec:
		fvec.append(round(v,dec))
	return Vector(fvec)
	
	
def roundMatrix(mat,dec=17):
	fmat = []
	for row in mat:
		fmat.append(roundVector(row,dec))
	return Matrix(*fmat)

def Matrix4x4(data):
	return Matrix(  data[:4],\
					data[4:8],\
					data[8:12],\
					data[12:16])	

def Matrix3x3(data):
	return Matrix(  data[:3],\
					data[3:6],\
					data[6:9])
	
	
		

def VectorMatrixScale(scale):
	mat = Blender.Mathutils.Matrix(
			[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1],
			)
	mat *= Blender.Mathutils.ScaleMatrix(scale[0], 4, Blender.Mathutils.Vector([1, 0, 0]))
	mat *= Blender.Mathutils.ScaleMatrix(scale[1], 4, Blender.Mathutils.Vector([0, 1, 0]))
	mat *= Blender.Mathutils.ScaleMatrix(scale[2], 4, Blender.Mathutils.Vector([0, 0, 1]))	
	return mat
	
	
def decrypt_string(string):
	'''Return the decrypted string. XOR each character in the string by
	FF to get the actual character. Strings are null-terminated.'''
	#string =B(count )
	inverted = ""
	print len(string)
	#for m in range(len(string)-1):
	for m in string:
		#pass
		#inverted += chr(string[i] ^ 0xFF)
		inverted += chr(m ^ 0x55)
	return inverted
	
class Script:
	"""
	init
		self.input=None
		self.VISUALISER=False
	object
		run()
	"""
	def __init__(self):
		self.input=None
		self.VISUALISER=False
		self.TEATIMEDECODER=False
	def run(self):
		if self.VISUALISER==True:
			textList=[]
			for text in Blender.Text.Get():
				if text.name not in textList:
					textList.append(text.name)
			scn = Blender.Scene.GetCurrent()
			self.input="gameLib\\scripts\\visualiser.py"
			txt=Blender.sys.basename(self.input)
			if txt not in textList:
				text=Blender.Text.Load(self.input)
			scn.addScriptLink(txt,'Redraw')			
				

class Searcher():
	"""
		init:
			self.dir=None
			self.list=[]
			self.what=None
			
		object:
			run()
	"""
	def __init__(self):
		self.dir=None
		self.list=[]
		self.what=None
	def run(self):
		dir=self.dir	
		def tree(dir):
			list_dir = os.listdir(dir)
			olddir = dir
			for m in list_dir:
				if self.what.lower() in m.lower():
					self.list.append(olddir+os.sep+m)				
				if os.path.isdir(olddir+os.sep+m)==True:
					dir = olddir+os.sep+m
					tree(dir)
		tree(dir)	
	

def szukacz(what,bufor):
	plik.seek(0,2)
	filesize=plik.tell()
	plik.seek(0)
	while(True):
		t=plik.tell()
		data=plik.read(bufor)
		tell=data.find(what)
		#print tell,t
		if tell!=-1:
			print 'mam',what,t+tell
			plik.seek(t+tell+len(what))
		else:
			plik.seek(t+bufor)	
		if plik.tell()>=filesize:break


							
							
class Vertex:
		def __init__(self):
			self.pos=[]
			self.uv=[]
			self.boneweight=[]
			self.boneindice=[]
		
class Face:
		def __init__(self):
			self.indices=[]
			self.matID=None
			self.uv=[]
			
	
		
def ParseID():
		#0-0-0 - oznacza kolejno meshID - matID - objectID
		ids = []
		objectID=0
		modelID=0
		matID=0
		scene = bpy.data.scenes.active
		
		#for meshID
		for object in scene.objects:
			if object.getType()=='Mesh':
				try:
					meshID = int(object.getData(mesh=1).name.split('-')[0])
					ids.append(meshID)
				except:pass 
		"""for mesh in bpy.data.meshes:
				try:
					model_id = int(mesh.name.split('-')[0])
					ids.append(model_id)
				except:pass   
				
				
		for mat in Blender.Material.Get():
			#print mat.name
			try:
				model_id = int(mat.name.split('-')[0])
				ids.append(model_id)
			except:pass"""
		try:
			meshID = max(ids)+1
		except:
			meshID = 0
		return meshID


class SceneIDList:
	def __init__(self):
		meshIDList=[]
		objectIDList=[]
		scene = bpy.data.scenes.active
		for object in scene.objects:
			if object.getType()=='Mesh':
				try:
					meshID = int(object.getData(mesh=1).name.split('-')[0])
					meshIDList.append(meshID)
				except:pass 
				try:
					objectID = int(object.getData(mesh=1).name.split('-')[2])
					objectIDList.append(objectID)
				except:pass 
		for mesh in bpy.data.meshes:
				try:
					objectID = int(mesh.name.split('-')[2])
					objectIDList.append(objectID)
				except:pass   
		try:
			self.meshID = max(meshIDList)+1
		except:
			self.meshID = 0
		try:
			self.objectID = max(objectIDList)+1
		except:
			self.objectID = 0
			
		
		
		
		
FLT_EPSILON=0
def quatDecompress1(s0,s1,s2):

	which = ((s1 & 1) << 1) | (s2 & 1);
	s1 &= 0xfffe;
	s2 &= 0xfffe;

	scale = 1.0/32767.0/1.41421

	if which == 3:
		x = s0 * scale
		y = s1 * scale
		z = s2 * scale

		w = 1 - (x*x) - (y*y) - (z*z);
		if (w > FLT_EPSILON):
			w = sqrt(w);
	elif (which == 2):# {
		x = s0 * scale;
		y = s1 * scale;
		w = s2 * scale;

		z = 1 - (x*x) - (y*y) - (w*w);
		if (z > FLT_EPSILON):
			z = sqrt(z);
	elif (which == 1):# {
		x = s0 * scale;
		z = s1 * scale;
		w = s2 * scale;

		y = 1 - (x*x) - (z*z) - (w*w);
		if (y > FLT_EPSILON):
			y = sqrt(y);
	else:
		y = s0 * scale;
		z = s1 * scale;
		w = s2 * scale;

		x = 1 - (y*y) - (z*z) - (w*w);
		if (x > FLT_EPSILON):
			x = sqrt(x);
	return x,y,z,w		


	
def quatDecompress2(s0,s1,s2):

	AxisFlg = ((s1 & 1) << 1) | (s2 & 1)

	s0 = 1.41421*(s0-32767)/0x7FFF
	s1 = 1.41421*(s1-0x3FFF)/0x7FFF
	s2 = 1.41421*(s2-0x3FFF)/0x7FFF
	s3=1-(s0*s0+s1*s1+s2*s2)
	if s3>0:
		s3 = sqrt(s3)
	print s0,s1,s2,s3,AxisFlg

	if AxisFlg==3:return s2, s1, s0, s3
	elif AxisFlg==2:return s2, s1 ,s3 ,s0
	elif AxisFlg==1:return s2, s3, s1 ,s0
	elif AxisFlg==0:return s3, s2, s1 ,s0
	
		
		