import sys
import os
from os.path import join
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def before_all(context):
  os = 'mac'
  hub = None
  if 'os' in context.config.userdata:
    os = context.config.userdata['os']
  if 'hub' in context.config.userdata:
    # http://127.0.0.1:4444/wd/hub
    hub = context.config.userdata['hub']

  removePickleCaches()
  # print('before_all')
  # desired_capabilities['client_key'] = 'key'
  # desired_capabilities['client_secret'] = 'secret'

  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')

  if hub is not None:
    capabilities = {
      "browserName": "chrome",
      "version": "62.0"
    }
    # context.browser = webdriver.Remote(command_executor=hub, desired_capabilities=DesiredCapabilities.CHROME)
    context.browser = webdriver.Remote(command_executor=hub, desired_capabilities=capabilities)
  else:
    desired_capabilities = webdriver.DesiredCapabilities.CHROME
    desired_capabilities['version'] = 'latest'
    desired_capabilities['platform'] = 'WINDOWS'
    desired_capabilities['name'] = 'Testing Selenium with Behave'
    context.browser = webdriver.Chrome('./bin/%s/chromedriver' % os, chrome_options=chrome_options)

  # context.browser.maximize_window()



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

