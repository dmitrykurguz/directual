import time
import sys
import pickle
import allure
from datetime import datetime
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from step_utils  import addCookieToCache, readCookieFromCache, appAddress, paramFromConfig, debug, logError

#FIXME remove all .pickle files on start

def before_all(context):
  context.implicitly_wait(10)

def before_feature(context, feature):
  context.browser.implicitly_wait(5)
  # print('remove vars')
  # context.vars = {}


# def after_feature(context, feature):
#   print('remove vars')
#   context.vars = {}



@given('directual page {path}')
@given('открыли мы страницу платформы {path}')
def step_impl(context, path):
  try:
    context.browser.get(appAddress(context) + path)
    allure.attach(context.browser.get_screenshot_as_png(),
                  name='open_page_%s' % path, attachment_type=allure.attachment_type.PNG)
  except Exception:
    logError()
    assert False
  # pass


@given('IF we on enter licence page')
@given('это оказалась страница ввода лицензии')
def step_impl(context):
  if not isEnterLicenceKeyPage(context.browser):
    context.scenario.skip(reason='current page is not Enter licence page')


@given('IF we on login page')
@given('это оказалась страница входа в систему')
def step_impl(context):
  if not isLoginPage(context.browser):
    context.scenario.skip(reason='current page is not Enter licence page')



#---------WHEN-------------


@when('we submit licence {key} as a key for user {email}')
@when('мы вводим {key} в качестве ключа для пользователя {email}')
def step_impl(context, key, email):

  waitForLicensePageBeingReady()

  context.browser.find_element_by_css_selector('input[name=email]').send_keys(email)
  context.browser.find_element_by_css_selector('textarea[name=key]').send_keys(key)
  context.browser.find_element_by_css_selector('input[type=submit]').click()


@when('мы пытаемся ввойти в систему под логином {login} и паролем {pwd}')
def step_impl(context, login, pwd):
  waitForLoginPageBeingReady()

  now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  # context.browser.get_screenshot_as_file('screenshot-%s.png' % now)

  context.browser.find_element_by_css_selector('#email').send_keys(login)
  context.browser.find_element_by_css_selector('#password').send_keys(pwd)

  allure.attach(context.browser.get_screenshot_as_png(), name='before_login', attachment_type=allure.attachment_type.PNG)
  context.browser.find_element_by_css_selector('input[type=submit]').click()
  waitForDashboardPageBeingReady()
  time.sleep(25) # FIXME remove
  allure.attach(context.browser.get_screenshot_as_png(), name='after_login', attachment_type=allure.attachment_type.PNG)
  waitForLoaderHide()
  

@when('обновляем страницу')
def step_impl(context):
  context.browser.refresh()
  # time.sleep(3)


#---------THEN-------------

@then('we must be on page {path}')
@then('отображается страница по пути {path}')
def step_impl(context, path):
  print(context.browser.current_url)
  result_path = appAddress(context) + path
  assert result_path in context.browser.current_url


@then('system show us error message')
@then('отображается ошибка')
def step_impl(context):
  waitForLicensePageBeingReady()
  assert "Произошла ошибка" in context.browser.page_source
  assert context.failed is False


@then('system show us login page')
@then('отображается страница входа')
def step_impl(context):
  waitForLoginPageBeingReady()
  if not isLoginPage(context.browser):
    fail('login form not found')
  
  assert context.failed is False


@then('установлена cookie с именем {name}')
def step_impl(context, name):
  print(context.browser.get_cookies())
  assert context.browser.get_cookie(name) is not None
  
@then('сохраним значение cookie {name} в кеш')
def step_impl(context, name):
  cookie = context.browser.get_cookie(name)
  # context.execute_steps('add cookie %s value %s to cache' % (name, cookie))
  addCookieToCache(context, name, cookie)


#------------------HELPER--------------

def waitForLoginPageBeingReady():
  EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type=submit]'))


def waitForLicensePageBeingReady():
  EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type=submit]'))

def waitForDashboardPageBeingReady():
  EC.visibility_of_element_located((By.CSS_SELECTOR, '.avatar'))


def waitForLoaderHide():
  EC.invisibility_of_element_located((By.CSS_SELECTOR, 'img.loader'))


def isEnterLicenceKeyPage(browser):
  try:
    browser.find_element_by_css_selector('input[name=email]')
    browser.find_element_by_css_selector('textarea[name=key]')
  except NoSuchElementException:
    return False
  return True


def isLoginPage(browser):
  try:
    browser.find_elements_by_css_selector('form.login_form')
  except NoSuchElementException:
    return False
  return True






