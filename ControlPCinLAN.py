from bottle import Bottle, run, get, post, request
import os

import pyautogui as keyboard
app = Bottle()

os.startfile('host_ip.bat')

# validate respective files from sub-folders in parent inside folder
def validFile(file,fileExtensions):
	for fileExtension in fileExtensions:
		if file.endswith(fileExtension) or file.endswith('.lnk'):
			return True

def files(path,fileType):
	files = []
	if fileType == 'audio':
		fileExtensions = ['.mp3','.m4a','.webm']
	elif fileType == 'video':
		fileExtensions = ['.mp4','.mkv']
	elif fileType == 'image':
		fileExtensions = ['.jpeg','.jpg','.png']
	elif fileType == 'docx':
		fileExtensions = ['.ppt','.pptx','.doc','.docx','.xls','.xlsx','.pdf','.txt']
	for file in os.listdir(path):
		if validFile(file,fileExtensions) : 
			files.append(str(file))
		
	return files	

# returns HTML template
def convertToHTML(files):
	ul = "<ul id='ul'>"
	for fileName in files:
		ul += "<li onclick='playMedia(this.innerHTML);'>"+fileName+"</li><hr/>"
	ul += "</ul>"
	return "<h5 id='h5' >Available files: </h5>"+ul


# create and update text file with currently clicked button
# as variables are not accessible in this framework we used files
def updateClicked(cmd):
	with open('clickedButtonFile.txt','w') as file:
		file.write(cmd)

def buttonClicked():
	with open('clickedButtonFile.txt','r') as file:
		return [i for i in file][0]

updateClicked('null')



@app.route('/')
def mainUI():

	return ''' 
 <head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	 <style>
	
		.control{
		
			padding-left:6%;
			padding-right:5%;
			display: inline-grid;
			grid-template-columns: repeat(3, 1fr);
			grid-column-gap: 5px;
			grid-row-gap: 5px;
			text-align: center;
			grid-template-rows: 40px auto 40px;
				 
			}	
	
		.menu{
			
			padding-left:8%;
		
			display: inline-grid;
			grid-column-gap: 5px;
			grid-row-gap: 5px;
			grid-template-rows: 70px 70px 70px;
			grid-template-columns: repeat(3, 1fr);
			
	
			}
			
		button{
			font-family:monospace;
			box-shadow: 2px -1px 13px 3px #e91e1e82;
			text-shadow: 3px 1px 7px black;
			background-color:inherit;
			border-radius:40px;
			color: white;
			border-color: indianred;
			}

	@media screen and (max-width :640px) {
		.control{padding-left:8%; padding-right:8%;}
		.menu{padding-left:12%;}
	}
	

	 </style>
	<script>

		function formSubmit(cmdValue){
		
			document.getElementById('form').setAttribute("style","display:none");
			document.getElementsByTagName('input').cmd.value=cmdValue
			document.getElementById('submitBtn').click();
		
		}



		function playMedia(fileName){
			// concatinating file type to 'form value' for determining type of file at server side
			// so that we will get selected media file which were generated dynamically
			formSubmit(fileName+'#@mediaFile');
		}

		function openURL(){
			document.getElementsByTagName('input').cmd.value='';
			document.getElementById('form').setAttribute('style','display:block');
			if (document.getElementById('ul') != null)
			{

			document.getElementById('ul').setAttribute('style','display:none');
			document.getElementById('h5').setAttribute('style','display:none');
			}
		}
	</script>


 </head>

 <body  style="font-family: monospace;background-color:#000000e3;color:white;">'''+"You're connected as "+request.get('REMOTE_ADDR')+'''
 <br/>
 <br/>
	
	<div  class="control" >
		<!-------------- Single click action buttons ------------------------------------------>
		
		<button id="volumeup" onclick="formSubmit(this.id)" style="font-size:13px;">vol +</button>
			<!-- this hidden button was for space in grid layout between two button in UI -->
		<button id="up" onclick="formSubmit(this.id)" style="font-size:20px;" > <b>^</b> </button>
		
		<button id="appSwitch" onclick="formSubmit(this.id)" style="font-size:15px;">switchApp</button>
		
	
		<button id="prevtrack" onclick="formSubmit(this.id)" style="font-size:20px;"> <b> &lt </b> </button>
		<button id="playpause" onclick="formSubmit(this.id)" style="font-size:15px;"> <b>OK</b></button>
		<button id="nexttrack" onclick="formSubmit(this.id)" style="font-size:20px;"> <b> &gt </b> </button>

		<button id="volumedown" onclick="formSubmit(this.id)" style="font-size:13px">vol -</button>
			<!-- this hidden button was for space in grid layout between two button in UI -->
		<button id="down" onclick="formSubmit(this.id)" style="font-size:18px;" > <b>v</b>  </button>

		<button  onclick="formSubmit(this.innerHTML)" style="font-size:16px;">fullScreen</button>
		
	</div>
	
	<hr/>
	
	<div class='menu' >
		<!----------------- Buttons ------------------>
		
		<button id="audio" onclick="formSubmit(this.id)" style="font-size:20px;">audio</button>
		<button id="video" onclick="formSubmit(this.id)" style="font-size:20px;;">video</button>
		<button id="docx" onclick="formSubmit(this.id)" style="font-size:21px;">Docs</button>
		<button id="fileUpload" onclick="formSubmit(this.id)" style="font-size:18px;">upload</button>
		<!-------------- Above buttons are for listing available files on click-------------->
		
		
		<!-------------- Single click action buttons ------------------------------------------>
		<button  id="openURL" onclick="formSubmit(this.id)"  style="font-size:30px;text-shadow: 1px 2px 9px black;">🔗</button>		
		<button   onclick="formSubmit(this.innerHTML)"  style="font-size:20px;text-shadow: 1px 2px 9px black;">type</button>		
		<button   onclick="formSubmit(this.innerHTML)"  style="font-size:18px;text-shadow: 1px 2px 9px black;">APPs</button>		
		<button   onclick="formSubmit(this.innerHTML)"  style="font-size:14px;text-shadow: 1px 2px 9px black;">backspace</button>		
		<button id="closeapp" onclick="formSubmit(this.id)" style="color:white;background-color:inherit;"><b>close app</b></button>		

	</div>
	<hr/>
	<form  action="/action" method="POST" id="form" style="display:none;">
		<input name="cmd" style="border-radius:40px;box-shadow: -1px 0px 14px 4px #8e2c2c;" type="text" placeholder="Paste the link"/>
		
		<input id="submitBtn" type="submit" style="background-color:inherit;border-radius:40px;color: white;" value="GO"/>
	
	</form>
	

	
	<script>
		if(window.history.replaceState){
			window.history.replaceState("","",window.location.origin);
			document.getElementsByTagName('input').cmd.value='';
		}
	</script>
	
	'''


@app.route('/action', method='POST')

def action():
	
	cmd = request.forms.get('cmd')
	typeCmd = request.forms.get('type')
	upload = request.files.get('fileUpload')
	#print(cmd,typeCmd,buttonClicked())
	textbox_Form = '''
		<form action="/action" method="POST">
			<textarea  name="type" style="border-radius:10px;box-shadow: -1px 0px 14px 4px #8e2c2c;width: 74%;height:10% "  placeholder="Start Typing"></textarea>
			<input id="submitBtn2" type="submit" style="background-color:inherit;border-radius:40px;color: white;" value="Send"/>
		</form>
		'''

	file_Upload_Form = '''
		<form id="form3" action="/action" method="POST" enctype="multipart/form-data">
			<input type="file" name="fileUpload" />
        	<input type="submit" value="Upload"/>
		</form>
		'''

	# ########## control buttons action ###############
	if typeCmd != None:
		keyboard.write(typeCmd,interval=0.25)
		updateClicked(typeCmd)
		return mainUI()+textbox_Form
	
	# Upload files from control device to host device, the uploaded files will get stored according to it's file types.
	# Default path would be c:\\Users\\current_User_Profile
	
	if upload!= None:
	
		filename,ext = os.path.splitext(upload.filename)
		ext = ext.lower()
		userDir = os.path.expanduser('~')

		# defining file path according to file type
	
		if ext in (".jpg",".jpeg",".png"):
			path = userDir +'\\Pictures'
		elif ext in (".mp4",".mkv"):
			path = userDir +'\\Videos'
		elif ext in (".mp3",'.m4a','.wav'):
			path = userDir +'\\Music'
		else:
			path = userDir +'\\Documents'
	
		try:
			upload.save(path)
		except IOError :
			return mainUI()+"File already Exists "
		except FileNotFoundError:
			return mainUI() + " Make sure you allowed this app through protected folders in Windows Security "

		return mainUI()+"File Uploaded to :" + path

	if cmd in ("volumeup" , "volumedown") :
		keyboard.press(cmd)
		return mainUI()
	
	elif cmd in ("up" ,"down"):
		keyboard.press(cmd)
		return mainUI()

	elif cmd == "playpause" :
		if buttonClicked() in ("audio","video"):
			keyboard.press(cmd)
		else:
			keyboard.press('enter')

			# to remove previous value on start of application 
			# we're updating file value as soon as our requirement is completed
			updateClicked('null')
		return mainUI()

	elif cmd in ( "prevtrack","nexttrack")  :
	
		if buttonClicked() in ("audio" ,'video'):
			keyboard.press(cmd)
			
		else:
			if cmd == "prevtrack":
				keyboard.press('left')
			elif cmd== "nexttrack":
				keyboard.press('right')
			
		return mainUI()


	elif cmd == "appSwitch":
		keyboard.hotkey('ctrl','alt','tab')
		updateClicked(cmd)
		return mainUI()

	elif cmd == "fullScreen":
		if buttonClicked() == 'docx':
			keyboard.press('f5')
		else:
			keyboard.press('f11')
		updateClicked(cmd)
		return mainUI()
	

	# ########## Menu buttons action ###############

	elif cmd == "audio" :
		#  update current UI with all available file list
		updateClicked(cmd)
		return mainUI()+convertToHTML(files(os.path.expanduser('~')+'\\Music',cmd))

	elif cmd == "video" :
		updateClicked(cmd)
		return mainUI()+convertToHTML(files(os.path.expanduser('~')+"\\Videos",cmd))

	elif cmd == "fileUpload":
		return mainUI()+file_Upload_Form
		

	elif cmd == "docx":
		updateClicked(cmd)
		return mainUI()+convertToHTML(files(os.path.expanduser('~')+"\\Documents",cmd))
	

	elif "#@mediaFile" in cmd:
		dir=""
		clickedButton = buttonClicked()
		if clickedButton == 'audio':
			dir = "\\Music"
		elif clickedButton == "video":
			dir = "\\Videos"
	
		elif clickedButton == "docx":
			dir = "\\Documents"
		os.startfile(os.path.expanduser('~')+dir+'\\'+cmd.split("#@mediaFile")[0])
		
		return mainUI()+convertToHTML(files(os.path.expanduser('~')+dir,clickedButton))

	elif cmd == "openURL":
		updateClicked(cmd)
		return mainUI()+'''<script>
					openURL()
				  </script>
			'''
	
	elif cmd.__contains__("://") and cmd.lower().startswith(("https","http","ftp")) :
		import webbrowser
		webbrowser.open(cmd)
		updateClicked(cmd)
		return mainUI()

	elif cmd == "type":
		updateClicked(cmd)
		return mainUI()+textbox_Form

	elif cmd == "APPs":
		keyboard.press('win')
		updateClicked(cmd)
		return mainUI()+"<script>formSubmit('type')</script>"
	
	elif cmd == "backspace":
		keyboard.press('backspace')
		updateClicked(cmd)
		return mainUI()

	elif cmd=='closeapp':
		keyboard.hotkey('alt','f4')
		updateClicked(cmd)
		return mainUI()
		
	else:
		updateClicked('none')
		return "<h1>Aww.... crashed please reload or go back</h1>"

# during testing use below line
# run(app,host='0.0.0.0', port=8080,debug=True,reloader=True)
#

run(app,host='0.0.0.0', port=8080,quiet=True)




#################################      CONTROL PC VIA LAN         #################################################

#                                clone it from my github repository 
 
# 				                  www.github.com/RiyazKhanPathan

######################################################################################################################   

