import argparse
import os
import sys
import time
import datetime



def main():
  app_id = "test_app_id"
  app_secret = "test_app_secret_12!@"
  
  scale = ""
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--name', help='name suffix')
  parser.add_argument('--datasource', help='pg | hbase | mongodb')
  parser.add_argument('--webui', help='image tag')
  args = vars(parser.parse_args())
  
  name_suffix = args['name']
  ds = args['datasource']
  webui = args['webui']
  
  if name_suffix is None:
    name_suffix = int(time.time())
  
  f = open('.env', 'w')
  
  f.write("TEST_APP_ID=" + app_id + "\n")
  f.write("TEST_APP_SECRET=" + app_secret + "\n")
  
  
  
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
  
  command = ('docker-compose -p qa-core-%s -f docker-compose-infra.yml -f docker-compose-web-ui.yml up --force-recreate -d ' % name_suffix) + scale
  
  network_name = 'qacore%s_default' % name_suffix
  selenoid_container_name = 'selenoid-%s' % name_suffix
  
  syscall('docker run --rm --name %s -v /var/run/docker.sock:/var/run/docker.sock -v ${HOME}:/root -e OVERRIDE_HOME=${HOME} aerokube/cm:latest-release selenoid start --vnc --tmpfs 128 -g "--container-network %s"' % (selenoid_container_name, network_name))
  syscall(command)
  
  
  
  # TODO run wait-for-it, wait for healthcheck from web-ui
  time.sleep(150)
  
  os.system('docker network connect %s %s' % (network_name, selenoid_container_name))
  
  # os.system('docker network connect qacore_default selenoid')
  # print 'waiting for docker-compose launch..'
  #os.system('./wait-for-it.sh localhost:8080 -t 180 -- echo "started!"')
  #os.system('./waitforit-darwin_amd64  -host=localhost -port=8080 -timeout=180 -- printf "Started\!"') # TODO remove
  
  
  #report_params = ' --junit --junit-directory /usr/src/app/reports'
  report_params = ' -f allure_behave.formatter:AllureFormatter -o /usr/src/app/reports'
  current_path = os.path.dirname(os.path.abspath(__file__))
  #reports_path = current_path + '/reports/' + datetime.datetime.today().strftime('%Y-%m-%d__%H_%M_%S')
  reports_path = current_path + '/reports'
  print('report will be at %s' % reports_path)
  
  volume_params = ' -v %s:/usr/src/app/behave -v %s:/usr/src/app/reports' % (current_path + '/behave/cases', reports_path)
  # FIXME path
  behave_command = 'docker run --rm %s --name behave-cases-%s --network=%s gitlab.directual.com:5005/docker/behave:latest behave -D hub=http://%s:4444/wd/hub -Dapp_address=http://web_ui:8080 %s' % (volume_params, name_suffix, network_name, selenoid_container_name, report_params)
  print 'execute: %s '% behave_command
  os.system(behave_command)

  #FIXME run separate compose file like in run_example.sh
  
  print 'serve allure report..'
  os.system('allure serve ' + reports_path)
  
  
  os.system('docker-compose -f docker-compose-web-ui.yml -f docker-compose-infra.yml -p qa-core-%s down' % name_suffix)
  os.system('docker stop %s' % selenoid_container_name)
  




def syscall(command):
  print 'execute %s' % command
  os.system(command)


main()
