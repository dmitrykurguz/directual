import argparse
import os
import sys



app_id = "test_app_id"
app_secret = "test_app_secret_12!@"

scale = ""

parser = argparse.ArgumentParser()
parser.add_argument('--datasource', help='pg | hbase | mongodb')
parser.add_argument('--webui', help='image tag')
args = vars(parser.parse_args())

ds = args['datasource']


f = open('.env', 'w')

f.write("TEST_APP_ID=" + app_id + "\n")
f.write("TEST_APP_SECRET=" + app_secret + "\n")


webui = args['webui']
if webui is not None:
  f.write("WEB_UI_IMAGE=" + webui + "\n")
  scale = scale + " --scale web_ui=1 "

if(ds == 'mongodb'):
	f.write("DATASOURCE=datasources:mongodb\n")
	f.write("DATASOURCE_PARAMS=mongodb://mongodb:27017\n")
	scale = scale + " --scale mongodb=1 --scale postgres=0 "

if(ds == 'pg'):
	f.write("DATASOURCE=PostgreSQLDS\n")
	f.write("DATASOURCE_PARAMS=\n")
	scale = scale + " --scale mongodb=0 --scale postgres=1 "


f.close()

command = 'docker-compose up --force-recreate ' + scale
print 'executing: ' + command

os.system(command)
