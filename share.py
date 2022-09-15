from os.path import dirname, realpath, exists
import json
import requests
import logging
from slack_sdk import WebClient
from statistics import mean
import re
import boto3


#
# CONFIG VARIABLES
#


ROOT_DIR = dirname(realpath(__file__))
slack_token = ''
slack_channel_ych_test_notifications = ''
slack_channel_ych_frontend_delivery = ''
slack_channel_ych_qa_auth = ''
slack_aws_bot_id = ''
aws_access_key_id = ''
aws_secret_access_key = ''
aws_test_server_ip = ''
aws_s3_bucket_reports = ''
aws_s3_bucket_log = ''

envs = [
    {
        "title": "Google",
        "url_frontend": "https://www.google.com",
        "url_backend": ""
    },
]
selenoids = [
    {
        "title": "Chrome104",
        "browserName": "chrome",
        "browserVersion": "104.0",
        "platform": "LINUX",
        "selenoid:options": {
            "enableVNC": bool('false'),
            "enableVideo": bool('false'),
            "videoName": "chrome104.mp4"
        }
    },
    {
        "title": "Chrome105",
        "browserName": "chrome",
        "browserVersion": "105.0",
        "platform": "LINUX",
        "selenoid:options": {
            "enableVNC": bool('false'),
            "enableVideo": bool('false'),
            "videoName": "chrome105.mp4"
        }
    },
{
        "title": "Chrome106",
        "browserName": "chrome",
        "browserVersion": "106.0",
        "platform": "LINUX",
        "selenoid:options": {
            "enableVNC": bool('false'),
            "enableVideo": bool('false'),
            "videoName": "chrome106.mp4"
        }
    },
]


#
# LOGGING
#


logging.basicConfig(
    filename='logs/general.log',
    level=logging.INFO,
    format='%(asctime)s -> %(created)s -> %(message)s'
)


def clear_file_data(path_to_file):
    with open(path_to_file, 'w'):
        pass


#
# UPDATE USER.JSON
#


def user(parameter):
    with open(f"{ROOT_DIR}/user.json") as f:
        config = json.load(f)
    return config[parameter]


def user_update(parameter, value):
    # GET USER
    with open(f"{ROOT_DIR}/user.json") as f:
        config = json.load(f)
    # UPDATE USER
    if parameter in ["selected_url_frontend", "selected_url_backend"]:
        config[parameter] = value
    elif parameter in ["selected_selenoid_id", "selenoid_status"]:
        config[parameter] = int(value)
    # SAVE USER
    with open(f"{ROOT_DIR}/user.json", 'w') as f:
        json.dump(config, f)


def set_up(env=envs[0]['title'], selenoid='0'):
    # python3 -c "from share import set_up; set_up('Stage1', 'Chrome104')"

    function_title = 'set_up()'

    # log
    logging.info(f"Function {function_title} -> Start")

    # ENV
    for env_data in envs:
        if env_data['title'] == env:  # ищем нужный env по title
            # обновляем значение selected_url_frontend в user.json
            user_update('selected_url_frontend', env_data['url_frontend'])
            # обновляем значение selected_url_backend в user.json
            user_update('selected_url_backend', env_data['url_backend'])

    # SELENOID
    if selenoid == '0':
        user_update('selenoid_status', '0')
    else:
        i = 0
        for selenoid_data in selenoids:
            if selenoid_data['title'] == selenoid:  # ищем нужный selenoid по title
                user_update('selenoid_status', '1')
                user_update('selected_selenoid_id', i)  # обновляем значение selected_selenoid_id в user.json
            i += 1

    # log
    logging.info(f"Function {function_title} -> Updated Env: {env}")
    logging.info(f"Function {function_title} -> Updated Selenoid: {selenoid}")
    logging.info(f"Function {function_title} -> Finish")


#
# SLACK
#


def post_message_to_slack(channel, username, message, report_name=None, blocks=None):
    # python3 -c "from share import post_message_to_slack; post_message_to_slack('C041SA6NXG8', 'Test', '', 'full_regression_3')"

    # функция отправляет сообщение в Slack канал
    # если переменная report_name не пустая, то
    # ищем отчет в папке отчетов
    # парсим данные из отчета
    # добавляем ключевые данные в сообщение Slack
    # добавляем ссылку на отчет в S3 в сообщение Slack
    # отправляем сообщение в Slack

    function_title = 'post_message_to_slack()'

    # log
    logging.info(f"Function {function_title} -> Start")

    if report_name is not None:
        # log
        logging.info(f"Function {function_title} -> Report name: {report_name}.html")
        # check report file exists
        if exists(f"{ROOT_DIR}/reports/html/{report_name}.html"):
            # open text file in read mode
            report_data = open(f"{ROOT_DIR}/reports/html/{report_name}.html", "r")
            # read whole file to a string
            report_data = report_data.read()
            # check report_data is not None
            if report_data != '':
                # get values from report file
                features = re.search("""<p id="feature_totals">(.*)</p><p id="scenario_totals">""", report_data)
                scenarios = re.search("""<p id="scenario_totals">(.*)</p><p id="step_totals">""", report_data)
                steps = re.search("""<p id="step_totals">(.*)</p></p><p id="duration">""", report_data)
                duration = re.search("""<p id="duration">(.*)</p>""", report_data)
                # clean values from report file
                features = features.group(1)
                scenarios = scenarios.group(1)
                steps = steps.group(1)
                duration = duration.group(1)
                # get total report
                report_data = f"{features}\n {scenarios}\n {steps}\n {duration}\n"
                # get report status
                if report_data.find('failed') == -1:
                    report_status = ":white_check_mark: Success\n"
                else:
                    report_status = ":x: Failed\n"
                # add data to the message
                message = f"{report_status}{message}\n {report_data} <https://{aws_s3_bucket_reports}.s3.amazonaws.com/{report_name}.html|Report>"
            else:  # if report_data is None
                # log
                logging.info(f"Function {function_title} -> Error: Empty report file")
                message = f":x: Preconditions Failed\n{message}"
        else:  # if file does not exist
            # log
            logging.info(f"Function {function_title} -> Error: Report file does not exist")
            message = f":x: Failed\n{message}"
    # send request
    response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': channel,
        'text': message,
        'username': username,
        'blocks': json.dumps(blocks) if blocks else None
    })
    # check response
    if response.status_code == 200 and response.headers['Content-Type'] == 'application/json; charset=utf-8':
        # get response value
        response_json = response.json()
        # check expected data in response
        if 'ok' in response_json:
            # check response status is Success
            if response_json['ok'] == bool("True"):
                # log
                logging.info(f"Function {function_title} -> Message: {message}")
                logging.info(f"Function {function_title} -> Response Success: {response_json}")
            else:  # response status is not Success
                # log
                logging.info(f"Function {function_title} -> Response Error: {response_json}")
        else:  # unexpected response
            # log
            logging.info(f"Function {function_title} -> Error: Unexpected response")
    else:  # status code is not 200 or unavailable Content-Type
        # log
        logging.info(
            f"Function {function_title} -> Error: Status code {response.status_code} and Content-Type is {response.headers['Content-Type']}")
    # log
    logging.info(f"Function {function_title} -> Finish")


#
#  WEB-APP PERFORMANCE
#


def web_app_performance():
    # python3 -c "from share import web_app_performance; web_app_performance()"

    # получаем из логов последний стейдж, на котором гонялись тесты
    # получаем дату крайнего обновления этого стейджа из Slack канала C03ADCV9ZPE
    # забираем из логов все данные о длительности шагов на этом стейдже
    # для каждого шага считаем среднее время до обновления стейджа и после
    # сравниваем средние значения длительности по каждому шагу до и после обновления стейджа
    # готовим сообщение в Slack со списком изменений в скорости шагов на выбранном стейдже
    # отправляем сообщение в Slack

    function_title = 'web_app_performance()'

    # log
    logging.info(f"Function {function_title} -> Start")

    # get the stage
    stage = ''
    log_data = aws_read_file(aws_s3_bucket_log, 'general.log')
    log_data = log_data.split('\n')
    for line in log_data:
        log_line = line.split(' -> ')
        if len(log_line) == 6:
            if log_line[2] == "Step duration":
                stage = log_line[3]

    # log
    logging.info(f"Function {function_title} -> Selected stage: {stage}")

    # get the date of last stage update from Slack
    stage_update_time = ''
    if stage != '':
        client = WebClient(token=slack_token)
        result = client.conversations_history(
            channel=slack_channel_ych_frontend_delivery,
            limit=300
        )

        aws_stage_search_title = 'webapp-devstaging'
        for message in result["messages"]:
            if 'bot_id' in message and message['bot_id'] == slack_aws_bot_id:
                aws_stage_title = message['attachments'][0]['blocks'][2]['fields'][0]['text']
                aws_stage_title = aws_stage_title.replace("*Application*\n", "")

                if aws_stage_title == aws_stage_search_title:
                    stage_update_time = float(message['ts'])
                    logging.info(f"Function {function_title} -> Stage update time: {stage_update_time}")
                    break

    # get the data from logs about selected stage
    steps_data_before = {}
    steps_data_after = {}

    if stage_update_time != '':
        log_data = aws_read_file(aws_s3_bucket_log, 'general.log')
        log_data = log_data.split('\n')
        for line in log_data:
            log_line = line.split(' -> ')
            if len(log_line) == 6:
                if log_line[2] == "Step duration" and log_line[3] == stage:

                    log_time = float(log_line[1])
                    log_step = log_line[4]
                    log_duration = float(log_line[5].replace('\n', ''))

                    # add step duration to the dictionary
                    if log_time > stage_update_time:
                        if log_step in steps_data_after:
                            steps_data_after[log_step].append(log_duration)
                        else:
                            steps_data_after[log_step] = []
                            steps_data_after[log_step].append(log_duration)
                    else:
                        if log_step in steps_data_before:
                            steps_data_before[log_step].append(log_duration)
                        else:
                            steps_data_before[log_step] = []
                            steps_data_before[log_step].append(log_duration)

    # log
    logging.info(f"Function {function_title} -> All results step duration before update: {steps_data_before}")
    logging.info(f"Function {function_title} -> All results step duration after update: {steps_data_after}")

    # get mean for steps duration
    if len(steps_data_before) > 0:
        for element in steps_data_before:
            steps_data_before[element] = round(mean(steps_data_before[element]), 3)
    if len(steps_data_after) > 0:
        for element in steps_data_after:
            steps_data_after[element] = round(mean(steps_data_after[element]), 3)

    # log
    logging.info(f"Function {function_title} -> Average step duration before update: {steps_data_before}")
    logging.info(f"Function {function_title} -> Average step duration after update: {steps_data_after}")

    # compare average step duration before and after update
    messageSlack = ''
    if len(steps_data_before) > 0 and len(steps_data_after) > 0:
        for element in steps_data_after:
            if element in steps_data_before:
                if (element[0:5] == "click" or element[0:3] == "API") and steps_data_before[element] > 0.1:
                    difference = round((steps_data_after[element] / steps_data_before[element]), 2)
                    if difference > 1.1:
                        messageSlack = f"{messageSlack} :red_circle: `{element}` медленнее на {int(difference * 100 - 100)}%\n"
                    elif difference < 0.9:
                        messageSlack = f"{messageSlack} :large_green_circle: `{element}` быстрее на {int(100 - difference * 100)}%\n"

    # log
    logging.info(f"Function {function_title} -> Prepare message to Slack -> {messageSlack}")

    # send message to Slack
    if messageSlack != '':
        messageSlack = f"*{messageSlack}"
        post_message_to_slack(slack_channel_ych_test_notifications, 'WEB-APP Performance', messageSlack)

    # log
    logging.info(f"Function {function_title} -> Send message to Slack: {messageSlack}")
    logging.info(f"Function {function_title} -> Finish")


#
# GET CONTEXT.VARIABLE VALUE
#


def check_context_dict_or_text(context, value):
    function_title = 'check_context_dict_or_text()'

    if value.find('context.') != -1:  # if 'value' start from 'context.'
        search_context = value.split(".")  # split it context.variable[key] -> ['context', 'variable[key]']
        if search_context[1].find('[') != -1:  # if second part has '['
            attribute = search_context[1].split("[")  # split it variable[key] -> ['variable', '[key]']
            if hasattr(context, attribute[0]):  # is 'variable' an attribute of context ?
                value = value.replace("[", "['")  # context.variable[key] -> context.variable['key]
                value = value.replace("]", "']")  # context.variable['key] -> context.variable['key']
                return eval(
                    value)  # return the value of context.variable or context.variable['key'], in situation of returning non sting will be an error
            else:
                # context.variable is not defined
                assert hasattr(context, attribute[0]), f"Function {function_title} -> {value} is not defined"
        else:
            return eval(value)  # return the value of context.variable
    else:
        return value  # return the value as is


#
# UPDATE CONTEXT.VARIABLE VALUE
#


def context_update(context, context_text, variable_name, variable_value):
    context_dict = eval(f"{context_text}")  # присваиваем значение context.variable в простую переменную
    context_dict[variable_name] = variable_value  # изменяем значение в словаре
    exec(f"{context_text} = {context_dict}")  # заменяет значение context.variable на новое


#
# API
#

def api_send_request_get_response(context, data, method_title):
    # log request
    logging.info(f"API {method_title} -> Request: {data}")
    # send request
    response = requests.post(user('selected_url_backend'), json=data)
    # get response
    if response.status_code == 200 and response.headers['Content-Type'] == 'application/json':
        # get response value
        response_json = response.json()
        # check error message in the response
        if response_json['error'] is None:
            # log
            logging.info(f"API {method_title} -> Response Success: {response.json()}")
            # return
            return response.json()
        else:
            # log
            logging.info(f"API {method_title} -> Response Error: {response_json['error']}")
            # return
            assert response_json['error'] is None, f"API {method_title} -> Response Error: {response_json['error']}"
    else:
        # log
        logging.info(f"API {method_title} -> Status code: {response.status_code}, Headers: {response.headers}")
        # return
        assert response.status_code == 200, f"API {method_title} -> Status code {response.status_code}"
        assert response.headers[
                   'Content-Type'] == 'application/json', f"API {method_title} -> Status code {response.headers['Content-Type']}"


#
# AWS S3 BOTO3
#


def aws_read_file(bucket_title, file_title):
    # creating session with Boto3.
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    # creating S3 resource from the session.
    s3 = session.resource('s3')
    # get object
    s3_object = s3.Bucket(bucket_title).Object(file_title).get()
    data = s3_object['Body'].read().decode()
    # return
    return data


def aws_update_file(bucket_title, s3_file_title, local_file_path):
    # creating session with Boto3
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    # creating S3 resource from the session
    s3 = session.resource('s3')
    s3_object = s3.Object(bucket_title, s3_file_title)
    # get local file data
    local_file_data = ''
    open_file = open(local_file_path, "r")
    for line in open_file.readlines():
        local_file_data = f"{local_file_data}{line}"
    # get S3 file data
    s3_file_data = aws_read_file(bucket_title, s3_file_title)
    # prepare updated data for S3
    s3_file_data = f"{s3_file_data}\n{local_file_data}"
    # send updates
    result = s3_object.put(Body=s3_file_data)
    res = result.get('ResponseMetadata')
    # check response
    if res.get('HTTPStatusCode') != 200:
        assert res.get(
            'HTTPStatusCode') != 200, f"Function aws_update_file() - Error: Status code is {res.get('HTTPStatusCode')}"
    else:
        # log success response
        logging.info(f"Function aws_update_file() -> Response Success")
