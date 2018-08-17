import sys
import os
import time
from os.path import join
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def before_all(context):
  time.sleep(10) # wait for selenoid

  os = 'mac'
  hub = None
  if 'os' in context.config.userdata:
    os = context.config.userdata['os']
  if 'hub' in context.config.userdata:
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


def before_feature(context, feature):
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
        return

    # Whatever other things you might want to do in this hook go here.


def before_scenario(context, scenario):
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
        return

    # Whatever other things you might want to do in this hook go here.
