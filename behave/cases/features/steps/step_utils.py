import sys
import os
import pickle
from behave import given, when, then
import allure


#----------------------UTILS---------------
#@when('add cookie {name} value {value} to cache')
def addCookieToCache(context, name, value):
  addToCache('cookie.' + name, value)


def readCookieFromCache(name):
  cookieName = 'cookie.' + name
  if(cacheNameExists(cookieName)):
    return readFromCache(cookieName)
  else:
    return None  


def addToCache(cacheName, obj):
  with open(cacheName + '.pickle', 'wb') as f:
    pickle.dump(obj, f)


def readFromCache(cacheName):
  with open(cacheName + '.pickle', 'rb') as f:
    return pickle.load(f)


def cacheNameExists(name):
  filename = name + '.pickle'
  print('filename for search: %s' % filename)

  dir = "./"
  files = os.listdir(dir)

  for item in files:
    print(item)
    if item == filename:
      return True
  return False

def appAddress(context):
  return paramFromConfig(context, 'app_address')

def paramFromConfig(context, name):
  return context.config.userdata[name]

def debug(name, text = 'trace'):
  allure.attach(text, name=name, attachment_type='text/plain')




@when('есть кешированое значение cookie с именем {name}')
@then('есть кешированое значение cookie с именем {name}')
def step_impl(context, name):
  assert cacheNameExists('cookie.' + name) is True

@given('работает шаг "{step_name}"')
@when('работает шаг "{step_name}"')
def step_impl(context, step_name):
  print('execute step %s' % step_name)
  context.execute_steps(step_name)
  

@when('указаны app_id и app_secret')
@given('указаны app_id и app_secret')
def step_impl(context):
  app_id = context.config.userdata['app_id']
  app_secret = context.config.userdata['app_secret']
  assert len(app_id) > 0
  assert len(app_secret) > 0