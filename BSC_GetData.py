
import csv
import requests
import re
import pandas as pd


API_KEY = "ckey_641f2f898f044703a63b3338b3f"
s = 'https://api.covalenthq.com/v1/56/address/{ad}/balances_v2/?key={key}'

#0x00144a00a91abcbC7cf339ab28d9f4d9B97dD597
#https://api.covalenthq.com/v1/56/address/0x00144a00a91abcbC7cf339ab28d9f4d9B97dD597/balances_v2/?key=ckey_641f2f898f044703a63b3338b3f
file = input("File: ")
with open(file) as f:
	reader = csv.reader(f)
	data = list(reader)

addresses = []

for address in data:
	addresses.append(address[0])

res = []
f_addresses = []

def get_data(address):
	assert address == address
	#print("{pid} Working on {ad}".format(ad=address,pid= str(os.getpid()).zfill(5)))
	try:
		r = requests.get(s.format(ad=address,key=API_KEY),timeout=10)
		rexsymbol = re.compile('{"contract_decimals":([0-9]+),"contract_name":[ 0-9A-Za-z""-.]+,"contract_ticker_symbol":"(BNB|USDT)",.+?,"type":"cryptocurrency","balance":"([ 0-9]+)",')
		d = rexsymbol.findall(r.text)
		d = pd.DataFrame(d)
		d["Address"] = address
		res.append(d)
	except requests.exceptions.Timeout as err:
		print(err)
		print(address)
		f_addresses.append(address)



if __name__ == "__main__":
	counter = 0
	for address in addresses:
		get_data(address)
		counter += 1
		print(str(counter)+"/"+str(len(addresses)))
	print(f_addresses)

	f_addresses = pd.DataFrame(f_addresses)
	f_addresses.to_csv("{f}_failed_addresses.csv".format(f=file.split(".")[0]), encoding='utf-8',index=False)
	result = pd.concat(res)
	result.to_csv("{f}_data.csv".format(f=file.split(".")[0]), encoding='utf-8',index=False)