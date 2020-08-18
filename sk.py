#!/usr/bin/python3

import os, sys, getopt
import hashlib
import json, pymysql

from keystoneclient.v3 import client
from keystoneauth1 import identity
from keystoneauth1 import session
from keystoneauth1 import loading
from glanceclient import Client

# File Read Buffer
BUF_SIZE = 655366

# Database Static
db_host = 'localhost'
db_name = 'glance_hash'
tb_name = 'image_hash'
db_user = 'apptest'
db_pass = 'apptest'

# Openstack Static
url = 'http://192.168.1.201:5000/v3'
usern = 'admin'
passw = '35f2bca30449451a'
proj = 'admin'

# Glance Authentication
def glanceAuth():
	# Authentication & Session Creation
	auth = identity.V3Password(auth_url=url,
							   username=usern,
							   user_domain_name='Default',
							   password=passw,
							   project_name=proj,
							   project_domain_name='Default')
	sess = session.Session(auth=auth)
	#sk = client.Client(session=sess)
	glance = Client('2', session=sess)
	return glance

# DB Auth
def getHashes():
	hashes = []
	db_conn = pymysql.connect(db_host,db_user,db_pass,db_name)
	curs = db_conn.cursor()
	curs.execute('select hash from image_hash')
	hd = curs.fetchall()
	db_conn.close()
	for j in hd:
		hashes.append(j[0])
	return hashes

# Hash Calculation
def hashMe(myfile):
	sha = hashlib.sha512()
	with open(myfile, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha.update(data)
	return sha.hexdigest()

# List Images
def listImg(glance):
	print("\n## Current Images Present")
	allImages = []
	i = 0
	for image in glance.images.list():
		print("S.No.: " + str(i) + ",| Name: " + image.name + ",| Image ID: " + image.id + "\n---------------------")
		allImages.append(image.id)
		i = i + 1
	return allImages

# Upload Confirmation
def upConfirm(glance, inputfile):
	img = glance.images.create(name=inputfile[:-4])
	glance.images.upload(img.id, open(inputfile, 'rb'))
	return 1

# Add Image
def uploadImg(glance, inputfile):
	print("\n## Checking Hash")
	newHash = hashMe(inputfile)
	hashes = getHashes()
	try:
		c = hashes.index(newHash)
		print("Hash Found! Starting Upload")
		upConfirm(glance, inputfile)
		return 1
	except:
		ans = input("Hash Not Found in Database! Proceed Anyway(y/n) ?\n> ")
		if(ans == 'y'):
			upConfirm(glance, inputfile)
		else:
			print("Upload Cancelled!")
			return 0

# Delete Image
def deleteImg(glance):
	print("\n## Delete Image from below list")
	allImages = listImg(glance)
	ch = input("S.No. to delete: ")
	glance.images.delete(allImages[int(ch)])

# Main Function
def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
	except getopt.GetoptError:
		print('sk.py <option>\n -i <inputfile>\n')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('sk.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--file"):
			inputfile = arg
	# glance = glanceAuth()

	while(True):
		ch = input("\n# Menu:\n1. List Images | 2. Upload Image | 3. Delete Image | 4. Calc Hash | 5. Exit\n> ")
		if ch == '1':
			listImg(glance)
		elif ch == '2':
			uploadImg(glance, inputfile)
		elif ch == '3':
			deleteImg(glance)
		elif ch == '4':
			print("\nHash of Input file is: " + hashme(inputfile))
		else:
			sys.exit()

# Init
if __name__ == "__main__":
   main(sys.argv[1:])