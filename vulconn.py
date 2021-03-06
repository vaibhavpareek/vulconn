import socket
import urllib.request
import sqlite3
import time
import csv
import terminal_banner
import pyfiglet
from os import system
from progress.bar import Bar
def banner():
	print("\033[1;34;48m* LINUX BASED TOOL V1.0 \033[1;32;48mDeveloped By @Vaibhav Pareek\033[1;31;48m")
	ascii_banner = pyfiglet.figlet_format("Vulconn !")
	print(ascii_banner)
	print("\033[1;32;48m")
	banner_text = "\n[+] It is a linux based tool,work as a Site Connnectivity Checker. \n[+] It always notifies you when website is ALIVE\n[+] Database utility is included so you can have collection of all the records even if you forgot."
	my_banner = terminal_banner.Banner(banner_text)
	print(my_banner)	
	
def menu():
	print("\033[1;32;48m")	
	print("SITE CONNECTIVITY CHECKER")
	print("GET NOTIFY WHEN WEBSITE IS ACTIVE")
	print("1. Single URL")
	print("2. Export URL's via text file")
	print("3. Export URL's via csv file")
	print("4. Perform updation in database")
	print("ENTER ANY OTHER KEY TO EXIT")
def code_check(code):
	if(code==200):
		res = "Active"
	elif(code>=301 and code<400):
		res = "Redirected"
	elif(code==400):
		res = "Bad Request"
	elif(code==403):
		res = "Forbidden"
	elif(code==404):
		res = "Not Found"
	elif(code==500):
		res="Internal Server Error"
	else:
		res="Unusual"
	return res
def database():
	print("1. List the Values of a Database.")
	print("2. Perform Updation in the Database.")
	print("3. Perform Deletion in the Database ")
	print("4. To Go Back ")
banner()
bar = Bar('\033[1;36;48mSetting Up database and dependencies', max=20)
raw = {1:">> Successfully created and connected..",2:">> Checking dependencies..",3:">> Establishing connection.."}
j=1
for i in range(20):
    time.sleep(.12)
    if(i%7==0):
    	print(" \n " + raw[j])
    	j = j+1
    bar.next()
bar.finish()
conn = sqlite3.connect("websitedata.db")
print(" >> Successfully created and connected")
try:
	tr = conn.execute("CREATE TABLE webcollect(website TEXT PRIMARY KEY NOT NULL);")
except sqlite3.OperationalError as e:
	print(" >> MESSAGE : ALREADY TABLE EXIST")
try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print(" >> Socket Established")
except socket.error as err:
	print(" >> Socket can't be Established now ,try again later......")
port = 80
conn.close()
while(True):
	menu()
	ch = int(input(" >> Choice : "))
	if(ch==1):
		system("clear")
		print("\033[1;33;48m")
		ascii_banner = pyfiglet.figlet_format("Check Single URL")
		print(ascii_banner)
		print("\033[1;36;48m")
		conn = sqlite3.connect("websitedata.db")
		host = input(">> Enter host name : ")
		try:
			conn.execute("INSERT INTO webcollect VALUES (\'"+str(host)+"');")
			conn.commit()
			print("URL added in the database....")
		except sqlite3.OperationalError as er :
			print("URL is already present in the database....")
		conn.close()
		try:
			ip = socket.gethostbyname(host)
		except socket.gaierror:
			print("Host name can't resolve for now ......")
		print(">>connecting ip to the port")
		start = time.time()
		c = "run"
		timer = 1
		while(c != 'q' and c!='Q' and c!='Quit' and c !='quit' and c !='QUIT'):
			code = urllib.request.urlopen("https://"+host).getcode()
			end = time.time()
			tm = (end-start)
			re = code_check(code)
			url = urllib.request.urlopen("https://"+host).geturl()
			final = url+" : "+re + " : TIME("+("%2f"%tm)+")"
			if(re=="Active"):
				system("notify-send \""+str(final)+"\"")
			print("Keep On Checking......TO STOP PRESS CTRL+Z")
			time.sleep(1)
			timer += 1
			if(timer==10):
				ree = input("Do you want to quit ?(y/n)")
				if(ree == 'y' or ree =='Y' or ree =='Yes' or ree=='yes'):
					c='q'
				else:
					timer = 1
	elif(ch==2):
		system("clear")
		print("\033[1;33;48m")
		ascii_banner = pyfiglet.figlet_format("Upload TEXT File")
		print(ascii_banner)
		print("\033[1;36;48m")
		conn = sqlite3.connect("websitedata.db")				
		host = input(">> Enter File Path : ")
		l = open(host,"r")
		ae = l.readlines()
		for i in ae:
			try:
				conn.execute("INSERT INTO webcollect VALUES (\'"+str(i)+"');")
				conn.commit()
				print("URL added in the database....")
			except sqlite3.Error as er :
				print("URL is already present in the database....")
		liste = conn.execute("SELECT * FROM webcollect")
		web = {}
		k = 1
		for i in liste:
			web[k]=i[0]
			k = k+1	
		count = len(web)
		c = "run"
		value = 1
		while(c != 'q' and c!='Q' and c!='Quit' and c !='quit' and c !='QUIT'):		
			try:
				ip = socket.gethostbyname(web[value])
			except socket.gaierror:
				print("Host name can't resolve for now ......")
			print(">>connecting ip to the port")
			start = time.time()
			code = urllib.request.urlopen("https://"+web[value]).getcode()
			print(">>>"+str(web[value]))
			end = time.time()
			tm = (end-start)
			re = code_check(code)
			url = urllib.request.urlopen("https://"+web[value]).geturl()
			final = url+" : "+re + " : TIME("+("%2f"%tm)+")"
			if(re=="Active"):
				system("notify-send \""+str(final)+"\"")
			if(value==count):
				value = 1
				c = input("Keep On Checking......TO STOP PRESS Q")		
			else:
				value = value + 1
			time.sleep(6)
		conn.close()
	elif(ch==3):
		system("clear")
		print("\033[1;33;48m")
		ascii_banner = pyfiglet.figlet_format("Upload CSV File")
		print(ascii_banner)
		print("\033[1;36;48m")
		conn = sqlite3.connect("websitedata.db")				
		host = input(">> Enter CSV FILE Path : ")
		with open(host,'r') as fin:
			dr = csv.DictReader(fin)
			to_db = [(i['website']) for i in dr]
		for k in to_db:
			try:
				conn.execute("INSERT INTO webcollect VALUES (\'"+str(k)+"');")
				conn.commit()
				print("URL added in the database....")
			except sqlite3.Error as er :
				print("URL is already present in the database....")
		liste = conn.execute("SELECT * FROM webcollect")
		web = {}
		j = 1
		for i in liste:
			web[j]=i[0]
			j = j+1	
		count = len(web)
		print(count)
		c = "run"
		value = 1
		while(c != 'q' and c!='Q' and c!='Quit' and c !='quit' and c !='QUIT'):		
			try:
				ip = socket.gethostbyname(str(web[value]))
			except socket.gaierror:
				print("Host name can't resolve for now ......")
			print(">>connecting ip to the port")
			start = time.time()
			code = urllib.request.urlopen("https://"+web[value]).getcode()
			end = time.time()
			tm = (end-start)
			re = code_check(code)
			url = urllib.request.urlopen("https://"+web[value]).geturl()
			final = url+" : "+re + " : TIME("+("%2f"%tm)+")"
			if(re=="Active"):
				system("notify-send \""+str(final)+"\"")
			if(value==count):
				value = 1
				c = input("Keep On Checking......TO STOP PRESS Q")		
			else:
				value = value + 1
			time.sleep(2)
		conn.close()		
	elif(ch==4):
		system("clear")
		print("\033[1;33;48m")
		ascii_banner = pyfiglet.figlet_format("Update Database")
		print(ascii_banner)
		print("\033[1;36;48m")
		o = 1
		while(o == 1):
			database()
			co = int(input(">> Choice : "))
			if(co==1):
				conn = sqlite3.connect("websitedata.db")				
				ls = conn.execute("SELECT * FROM webcollect")
				count = 1
				for i in ls:
					print("[+] WEBSITE "+str(count) + " : "+str(i))
					count = count +1
				conn.close()
				inu = input("Press any key to continue")
			elif(co==2):
				conn = sqlite3.connect("websitedata.db")				
				url_rep_frm = input(">> URL that you want to replace : ")
				url_rep_to = input(">> URL that you want to use instead : ")
				conn.execute("UPDATE webcollect set Website = "+str(url_rep_to)+" WHERE Website = "+str(url_rep_frm))
				conn.commit()
				conn.close()
				print(">>Updated  Successfully!")
				inu = input("Press any key to continue")
			elif(co==3):
				cg = input("Do you really want to delete all the records and database : ")
				conn = sqlite3.connect("websitedata.db")				
				if(cg=='y' or cg == 'Y' or cg == 'Yes' or cg == 'YES'):
					conn.execute("DROP TABLE webcollect;")
					conn.commit()
				conn.close()
				print(">>Table droped Successfully")
				inu = input("Press any key to continue")	
			else:
				o = 5
	else:
		exit(0)		