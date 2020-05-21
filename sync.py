import json
from time import sleep
import os
import requests

base = 'http://xdmoan.org'
sleeptime = 1
folder = 'pictures'


def read_data(f):
	with open(f, 'r') as df:
		return json.loads(df.read())

def dump_data(f, d):
	with open(f, 'w') as df:
		json.dump(d, df, indent=4)


def post_file(filename):
	with open(f'{folder}/{filename}', 'rb') as handle:
		requests.post(f'{base}/sync', files={filename: handle})


terminate = False
data = read_data('files.json')
change = False
print(f'Scanning for Files in {folder}')
while not terminate:
	for file in os.listdir(folder):
		if file not in data['files']:
			print(f'New File Found: {file}')
			print(f'Uploading {file} to Cloud')
			post_file(file)
			print(f'{file} Successfully uploaded to Server')
			data['files'].append(file)
			change = True
	if change:
		dump_data('files.json', data)
		print('Data Added to Local Cache')
		data = read_data('files.json')
		change = False
	sleep(sleeptime)