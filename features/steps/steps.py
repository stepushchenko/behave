from behave import when
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xpath import xpath
import share
import platform
import time
from slack_sdk import WebClient
import json
import logging
import requests


# todo actions from old code
    # select (li or option)
    # collect text or value to variable
    # compare variable value with text from a test case
    # compare value from a page with text from a test case


@when('open page {link}')
def step_impl(context, link):
    context.browser.get(share.user('selected_url_frontend') + link)


@when('click {selector}')
def step_impl(context, selector):
    wait_before_presence_of_element_located(context, selector).click()


@when('enter value {value} in {selector}')
def enter_value(context, value, selector):
    value = share.check_context_dict_or_text(context, value)
    wait_before_presence_of_element_located(context, selector).send_keys(value)  # in situation of non sting will be an error


@when('clear value in {selector}')
def step_impl(context, selector):
    element = wait_before_presence_of_element_located(context, selector)
    if platform.system() == 'Darwin':
        element.send_keys(Keys.COMMAND + "a")
        element.send_keys(Keys.DELETE)
    else:
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)


@when('compare text from {selector} with {text}')
def step_impl(context, text, selector):
    text = share.check_context_dict_or_text(context, text)
    wait_before_text_to_be_present_in_element(context, selector, text)


@when('press keyboard numbers {value}')
def press_keyboard_numbers(context, value):
    action = ActionChains(context.browser)
    value = share.check_context_dict_or_text(context, value)
    for num in value:
        numpad = 'NUMPAD' + num
        action.send_keys(Keys.__str__(numpad))
    action.perform()


@when('press keyboard key {value}')
def press_keyboard_numbers(context, value):
    action = ActionChains(context.browser)
    value = share.check_context_dict_or_text(context, value)
    action.send_keys(Keys.__str__(value))
    action.perform()


@when('wait {time_in_sec}')
def step_impl(context, time_in_sec):
    time.sleep(int(time_in_sec))


@when('get {context_text} auth code from Slack')
def get_auth_code_from_slack(context, context_text):
    function_title = 'get_auth_code_from_slack()'

    # выставляем количество попыток
    # выставляем время задержки между попытками
    # высчитываем время, когда код был отправлен на почту
    # просим Slack прислать все сообщения полученные после даты отправки коды
    # проверяем каждое сообщение на совпадение получателя письма с нашим email
    # если почта совпадает, то берем код из письма
    # код авторизации записываем в переменную context

    # log
    logging.info(f"Function {function_title} -> Start")
    slack_code = ''
    for attempt in range(1, 15):  # attempt == попытка
        # get user email from context variable
        user_email = share.check_context_dict_or_text(context, f"{context_text}[email]")
        # log
        logging.info(f"Function {function_title} -> Request #{attempt}")
        # set waiting time
        waiting_time_in_sec = 6
        # wait
        time.sleep(waiting_time_in_sec)
        # calculate the time
        oldest = str(time.time() - waiting_time_in_sec * attempt)
        # get last Slack messages
        client = WebClient(token=share.slack_token)
        results = client.conversations_history(
            channel=share.slack_channel_ych_qa_auth,
            oldest=oldest,
        )
        # log
        logging.info(f"Function {function_title} -> Request #{attempt} -> Got {len(results['messages'])} messages")
        # message counter
        i = 1
        if len(results['messages']) > 0:
            for message in results['messages']:
                # get email_address from Slack message
                slack_email_address = message['files'][0]['to'][0]['address']
                # if user email == email from slack
                if slack_email_address == user_email:
                    # get Slack code from message
                    message_with_code = message['files'][0]['plain_text']
                    code_start = message_with_code.find('Your authentication code is ') + 28
                    code_finish = code_start + 6
                    slack_code = message_with_code[code_start:code_finish]
                    # save code to user variable
                    share.context_update(context, context_text, 'auth_code', slack_code)
                    # log
                    logging.info(f"Function {function_title} -> Request #{attempt} -> Message #{i} -> Code {slack_code}")
                    # message counter +1
                    i = i + 1
                    # stop loop
                    break
                else:
                    # log
                    logging.info(f"Function {function_title} -> Request #{attempt} -> Message #{i}")
        if slack_code != '':
            break
    # log
    logging.info(f"Function {function_title} -> Finish")


@when('generate user {user}')
def generate_user(context, user):

    user = user.replace(' ', '_')  # пробелы заменяем на нижнее подчеркивание
    unique_email = hash(f"{user} {time.time()}")
    user_data = {
        'email': f'stepuschenko+{unique_email}@gmail.com',
        'name': user,
        'age': 29,
        'user_id': '',
        'access_token': '',
        'session_token': '',
        'auth_code': '',
        'visit_log_id': '',
    }
    command = f"context.{user} = {json.dumps(user_data)}"
    exec(command)


@when('generate program {program}')
def generate_user(context, program):
    program = program.replace(' ', '_')  # пробелы заменяем на нижнее подчеркивание
    program_data = {
        'title': f'Title {program}',
        'description': 'Program description',
    }
    command = f"context.{program} = {json.dumps(program_data)}"
    exec(command)


@when('upload {file_name} to {selector}')
def step_impl(context, file_name, selector):
    file_path = f"{share.ROOT_DIR}/static/img/for_tests/{file_name}"
    wait_before_presence_of_element_located(context, selector).send_keys(file_path)


@when('check selector {selector}')
def step_impl(context, selector):
    wait_before_presence_of_element_located(context, selector)


@when('check file {selector}')
def step_impl(context, selector):
    URL = wait_before_presence_of_element_located(context, selector).get_attribute("src")  # get URL
    request_response = requests.head(URL)  # send request to the URL
    status_code = request_response.status_code  # get status code
    assert status_code == 200, f"Status code is not 200, it is {status_code}"


def wait_before_presence_of_element_located(context, selector):
    selector = xpath[selector]  # start_page_sign_in_button -> //*[@data-test-id='auth.button.sign_in']
    wait = WebDriverWait(context.browser, 20)  # 20 seconds wait
    element = wait.until(  # wait until element presence in DOM
        EC.presence_of_element_located((By.XPATH, selector)),  # return element, if it exists in the DOM
        message=f'Can not find {selector}',  # if no element, print a message
    )
    context.browser.execute_script("return arguments[0].scrollIntoView(true);", element)  # focus on the element
    return element


def wait_before_text_to_be_present_in_element(context, selector, text):
    selector = xpath[selector]  # start_page_sign_in_button -> //*[@data-test-id='auth.button.sign_in']
    wait = WebDriverWait(context.browser, 20)  # 20 seconds wait
    true_or_false = wait.until(  # until elements is not visible
        EC.text_to_be_present_in_element((By.XPATH, selector), text),  # return true, if text presents
        message=f'Can not find {text} in {selector}',  # if no text, print a message
    )
