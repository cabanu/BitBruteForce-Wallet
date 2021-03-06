#!/usr/bin/python

'''
Change Cores=# of how many cores do you want to use (371 K/s/Core - Used settings = 6 Cores - 6 * 371 * 60 * 60 * 24 = 192.326.400 addresses / day = 70.199.136.000 addresses / year)
Take into account VM as well (i3 with 2 cores but 4VM -> 8 threads). More cores is just more demanding for OS scheduler
(worth playing around, even above number of CPU cores)
'''

import time
import datetime as dt
import os
import multiprocessing
from multiprocessing import Pool
import binascii, hashlib, base58, ecdsa
import pandas as pd


# begin mysql connector

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="DBUSER",
  password="DBPASSWORD",
  database="btc"
)

#end mysql


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


r = 0
cores=6

def seek(r, df_handler):
	global num_threads
	LOG_EVERY_N = 15000
	start_time = dt.datetime.today().timestamp()
	i = 0
	print("Core " + str(r) +":  Generating Private Key..")
	while True:

		i=i+1
		#generate private key , uncompressed WIF starts with "5"
		priv_key = os.urandom(32)
		fullkey = '80' + binascii.hexlify(priv_key).decode()
		sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
		sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
		WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))

		# get public key , uncompressed address starts with "1"
		sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
		hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
		publ_addr_a = b"\x00" + hash160
		checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
		publ_addr_b = base58.b58encode(publ_addr_a + checksum)
		priv = WIF.decode()
		global pub
		pub = publ_addr_b.decode()
		mycursor = mydb.cursor()
		sql = 'UPDATE btc SET secret = "'+ priv +'" WHERE address = "'+ pub +'"'
		mycursor.execute(sql)
		mydb.commit()
		time_diff = dt.datetime.today().timestamp() - start_time

 
		if (i % LOG_EVERY_N) == 0:
			print('Core :'+str(r)+" K/s = "+ str(i / time_diff))
		#print ('Worker '+str(r)+':'+ str(i) + '.-  # '+pub + ' # -------- # '+ priv+' # ')
        


	contador=0
if __name__ == '__main__':
	jobs = []
	df_handler = pd.read_csv(open('bit.txt', 'r'))
	for r in range(cores):
		p = multiprocessing.Process(target=seek, args=(r,df_handler))
		jobs.append(p)
		p.start()	
