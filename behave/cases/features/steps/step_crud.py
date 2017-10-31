import sys
import os
import pickle
import requests
import json
from flatten_json import flatten_json
from behave import given, when, then
from step_utils  import readCookieFromCache, appAddress, paramFromConfig



@given('отправляем авторизованный запрос на "{path}"')
def step_impl(context, path):
  sessionid = readCookieFromCache("sessionid")
  
  assert sessionid is not None
  
  uri = '%s%s?%s=%s' % (appAddress(context), path, 'sessionid', sessionid['value'])
  print('request %s with sessionId' % uri)
  
  r = requests.post(uri, data=context.text)
  handleResponse(r)
  
  
@when('сохраняем объект структуры "{struct_name}"')
def step_impl(context, struct_name):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  print('use app_id %s and app_secret %s' % (app_id, app_secret))

  uri = '%s/good/api/v3/struct/%s/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)
  print('call: %s' % uri)
  r = requests.post(uri, data=context.text)
  handleResponse(r)
  

@given('существует объект структуры "{struct_name}" с id "{id}"')
@when( 'существует объект структуры "{struct_name}" с id "{id}"')
@then( 'существует объект структуры "{struct_name}" с id "{id}"')
def step_impl(context, struct_name, id):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  print('use app_id %s and app_secret %s' % (app_id, app_secret))

  body = '{"filters":[{"operator":"AND","field":"id","value":"%s","exp":"="}],"fetch":"","fields":"","pageSize":10,"page":0,"ref":"","allObjects":true,"orders":[]}' % id
  uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)

  print('call: %s' % uri)
  r = requests.post(uri, data=body)
  handleResponse(r)

  response = json.loads(r.text)
  assert len(response['result']['list']) == 1
  # TODO check object is ok



@then('объект структуры "{struct_name}" имеет поля')
def step_impl(context, struct_name):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  
  step_params = json.loads(context.text)
  filters = step_params['filter']
  assertion = flatten_json(step_params['assert'])

  uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)  
  print('looking %s with filters: %s' % (struct_name, filters))
  print('call: %s' % uri)
  r = requests.post(uri, data=json.dumps(filters))
  handleResponse(r)

  result = json.loads(r.text)
  resultList = result['result']['list']
  assert len(resultList) == 1
  item = resultList[0]['obj']
  print('item = %s' % item)
  print(assertion)

  flattenItem = flatten_json(item)
  for assertKey, assertValue in assertion.items():
    assert flattenItem[assertKey] == assertValue


def handleResponse(r):
  print('status: %s - \n%s' % (r.text, r.status_code))
  r.raise_for_status()





