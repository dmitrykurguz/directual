import sys
import os
import pickle
import requests
import json
from flatten_json import flatten_json
from behave import given, when, then
from step_utils  import readCookieFromCache, appAddress, paramFromConfig, debug



@given('отправляем авторизованный запрос на "{path}"')
def step_impl(context, path):
  sessionid = readCookieFromCache("sessionid")
  
  assert sessionid is not None
  
  uri = '%s%s?%s=%s' % (appAddress(context), path, 'sessionid', sessionid['value'])
  debug('request %s with sessionId' % uri)
  
  r = requests.post(uri, data=context.text)
  handleResponse(r)
  
  
@when('сохраняем объект структуры "{struct_name}"')
def step_impl(context, struct_name):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  debug('use app_id %s and app_secret %s' % (app_id, app_secret))

  uri = '%s/good/api/v3/struct/%s/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)
  debug('call: %s' % uri)
  r = requests.post(uri, data=context.text)
  handleResponse(r)
  

@given('существует объект структуры "{struct_name}" с id "{id}"')
@when( 'существует объект структуры "{struct_name}" с id "{id}"')
@then( 'существует объект структуры "{struct_name}" с id "{id}"')
def step_impl(context, struct_name, id):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  debug('use app_id %s and app_secret %s' % (app_id, app_secret))

  body = '{"filters":[{"operator":"AND","field":"id","value":"%s","exp":"="}],"fetch":"","fields":"","pageSize":10,"page":0,"ref":"","allObjects":true,"orders":[]}' % id
  uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)

  debug('call: %s' % uri)
  r = requests.post(uri, data=body)
  handleResponse(r)

  response = json.loads(r.text)
  debug(response)

  assert 'result' in response
  results = response['result']
  assert 'list' in results
  assert len(results['list']) == 1



@then('объект структуры "{struct_name}" имеет поля')
def step_impl(context, struct_name):
  app_id = paramFromConfig(context, 'app_id')
  app_secret = paramFromConfig(context, 'app_secret')
  
  step_params = json.loads(context.text)
  filters = step_params['filter']
  assertion = flatten_json(step_params['assert'])

  uri = '%s/good/api/v3/struct/%s/search/?appID=%s&appSecret=%s' % (appAddress(context), struct_name, app_id, app_secret)  
  debug('looking %s with filters: %s' % (struct_name, filters))
  debug('call: %s' % uri)
  r = requests.post(uri, data=json.dumps(filters))
  handleResponse(r)

  result = json.loads(r.text)
  resultList = result['result']['list']
  assert len(resultList) == 1
  item = resultList[0]['obj']
  debug('item = %s' % item)
  debug(assertion)

  flattenItem = flatten_json(item)
  for assertKey, assertValue in assertion.items():
    assert flattenItem[assertKey] == assertValue


def handleResponse(r):
  debug('status: %s - \n%s' % (r.text, r.status_code))
  r.raise_for_status()





