import sys
import os
from os.path import join
from selenium import webdriver

def before_all(context):
  removePickleCaches()
  # print('before_all')
  desired_capabilities = webdriver.DesiredCapabilities.CHROME
  desired_capabilities['version'] = 'latest'
  desired_capabilities['platform'] = 'WINDOWS'
  desired_capabilities['name'] = 'Testing Selenium with Behave'
  # desired_capabilities['client_key'] = 'key'
  # desired_capabilities['client_secret'] = 'secret'

  context.browser = webdriver.Chrome('./bin/mac/chromedriver')
  context.browser.maximize_window()



def after_all(context):
  removePickleCaches()
  # context.server.shutdown()
  # context.thread.join()
  context.browser.quit()





def removePickleCaches():
  dir = "./"
  files = os.listdir(dir)

  for item in files:
    if item.endswith(".pickle"):
      os.remove(join(dir, item))

