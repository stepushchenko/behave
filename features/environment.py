from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import share
import logging


@fixture
def open_browser(context):
    # OPEN BROWSER
    if share.user('selenoid_status') == 0:  # selenoid is turned off
        options = Options()
        options.add_argument('--headless')  # do not open browser during tests
        context.browser = webdriver.Chrome(
            executable_path='/usr/local/bin/chromedriver',
            options=options,
        )
    else:
        selenoids = share.selenoids
        selected_selenoid_id = share.user('selected_selenoid_id')
        context.browser = webdriver.Remote(
            command_executor=f'http://{share.aws_test_server_ip}:4444/wd/hub',
            desired_capabilities=selenoids[selected_selenoid_id]
        )
    # UPDATE BROWSER SETTINGS
    context.browser.set_window_size(1240, 1000)


@fixture
def quite_browser(context):
    context.browser.quit()


@fixture
def step_duration(context, step):
    logging.info(f"Step duration -> {share.user('selected_url_frontend')} -> {step.name} -> {round(step.duration, 3)}")


@fixture
def add_log_about_new_run(context):
    logging.info(f"")
    logging.info(f"NEW RUN")
    logging.info(f"")


def before_all(context):
    use_fixture(add_log_about_new_run, context)


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    use_fixture(open_browser, context)


def before_step(context, step):
    pass


def after_step(context, step):
    use_fixture(step_duration, context, step)


def after_scenario(context, scenario):
    use_fixture(quite_browser, context)


def after_feature(context, feature):
    pass


def after_all(context):
    pass
