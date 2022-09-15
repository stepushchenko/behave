import share
from behave import given, when, then
import logging


@when('API {context_text} user.auth.send_code')
def api_user_auth_send_code(context, context_text):
    method_title = "user.auth.send_code"
    context_dict = share.check_context_dict_or_text(context, context_text)

    # check variables availability
    assert context_dict['email'] != '', f"API {method_title} -> Error: no value in variable email"
    # data preparation
    data = {
        "id": 1,
        "method": method_title,
        "meta": {
            "token": "valid",
            "version": [9, 0]
        },
        "params":
            {
                "to_website": bool("true"),
                "email": context_dict['email'],
                "platform": "web",
            }
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title} (to_website)")

    # check variables availability
    assert context_dict['email'] != '', f"API {method_title} -> Error: no value in variable email"
    # data preparation
    data = {
        "id": 1,
        "method": method_title,
        "meta": {
            "token": "valid",
            "version": [9, 0]
        },
        "params":
            {
                "email": context_dict['email'],
                "platform": "web",
            }
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")


@when('API {context_text} user.auth.signup')
def api_user_auth_signup(context, context_text):
    method_title = "user.auth.signup"
    context_dict = share.check_context_dict_or_text(context, context_text)
    # check variables availability
    assert context_dict['auth_code'] != '', f"API {method_title} -> Error: no value in variable auth_code"
    assert context_dict['email'] != '', f"API {method_title} -> Error: no value in variable email"
    assert context_dict['name'] != '', f"API {method_title} -> Error: no value in variable name"
    # data preparation
    data = {
        "id": 1,
        "method": method_title,
        "meta": {
            "token": "valid",
            "version": [9, 0]
        },
        "params":
            {
                "code": context_dict['auth_code'],
                "device": "Google Chrome",
                "email": context_dict['email'],
                "name": context_dict['name'],
                "platform": "web",
                "push_token": None
            }
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")
    # update context.variable
    share.context_update(context, context_text, 'access_token', response["result"]["access"]["token"])
    share.context_update(context, context_text, 'session_token', response["result"]["session"]["token"])
    share.context_update(context, context_text, 'user_id', response["result"]["user"]["_id"])


@when('API {context_text} user.auth.login')
def api_user_auth_login(context, context_text):
    method_title = "user.auth.login"
    context_dict = share.check_context_dict_or_text(context, context_text)
    # check variables availability
    assert context_dict['auth_code'] != '', f"API {method_title} -> Error: no value in variable auth_code"
    assert context_dict['email'] != '', f"API {method_title} -> Error: no value in variable email"
    # data preparation
    data = {
        "id": 1,
        "method": method_title,
        "meta": {
            "token": "valid",
            "version": [9, 0]
        },
        "params":
            {
                "code": context_dict['auth_code'],
                "device": "Google Chrome",
                "email": context_dict['email'],
                "platform": "web",
                "push_token": None
            }
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")
    # update context.variable
    share.context_update(context, context_text, 'access_token', response["result"]["access"]["token"])
    share.context_update(context, context_text, 'session_token', response["result"]["session"]["token"])
    share.context_update(context, context_text, 'user_id', response["result"]["user"]["_id"])


@when('API {context_text} user.profile.become_coach')
def api_user_profile_become_coach(context, context_text):
    method_title = "user.profile.become_coach"
    context_dict = share.check_context_dict_or_text(context, context_text)
    # check variables availability
    assert context_dict['access_token'] != '', f"API {method_title} -> Error: no value in variable access_token"
    # data preparation
    data = {
        "id": 1,
        "meta":
            {
                "access_token": context_dict['access_token'],
                "version": [9, 0]
            },
        "method": method_title,
        "params": {}
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")


@when('API {context_text} admin.visit_logs.list')
def api_admin_visit_logs_list(context, context_text):
    method_title = "admin.visit_logs.list"
    context_dict = share.check_context_dict_or_text(context, context_text)
    # check variables availability
    assert context_dict['access_token'] != '', f"API {method_title} -> Error: no value in variable access_token"
    assert context_dict['ip'] != '', f"API {method_title} -> Error: no value in variable ip"
    # data preparation
    data = {
        "id": 50,
        "meta":
            {
                "access_token": context_dict['access_token'],
                "version": [9, 0]
            },
        "method": method_title,
        "params": {
            "limit": 51,
            "query": [["ip", "==", context_dict['ip']]]
        },
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")
    # did we get a visit_log_id for the selected IP?
    if len(response["result"]["_items"]) > 0:
        # update variable value
        share.context_update(context, context_text, 'visit_log_id', response["result"]["_items"][0]["_id"])
    else:  # no visit_log_id in response
        # log
        logging.info(f"API {method_title} -> Error: no visit_log_id in the response")
        # return
        assert len(response["result"]["_items"]) > 0, f"API {method_title} -> Error: no visit_log_id in the response"


@when('API {context_text} admin.visit_logs.update')
def api_admin_visit_logs_update(context, context_text):
    method_title = "admin.visit_logs.update"
    context_dict = share.check_context_dict_or_text(context, context_text)
    # check variables availability
    assert context_dict['access_token'] != '', f"API {method_title} -> Error: no value in variable access_token"
    assert context_dict['visit_log_id'] != '', f"API {method_title} -> Error: no value in variable visit_log_id"
    # data preparation
    data = {
        "id": 50,
        "meta":
            {
                "access_token": context_dict['access_token'],
                "version": [9, 0]
            },
        "method": method_title,
        "params": {
            "_id": context_dict['visit_log_id'],
            "suspends": []
        },
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")


@when('API {context_text} admin.visit_logs.delete')
def api_admin_visit_logs_delete(context, context_text):
    method_title = "admin.visit_logs.delete"
    context_dict = share.check_context_dict_or_text(context, context_text)
    # check variables availability
    assert context_dict['access_token'] != '', f"API {method_title} -> Error: no value in variable access_token"
    assert context_dict['visit_log_id'] != '', f"API {method_title} -> Error: no value in variable visit_log_id"
    # data preparation
    data = {
        "id": 50,
        "meta":
            {
                "access_token": context_dict['access_token'],
                "version": [9, 0]
            },
        "method": method_title,
        "params": {
            "_id": context_dict['visit_log_id']
        },
    }
    # send request and get response
    response = share.api_send_request_get_response(context, data, f"{method_title}")
