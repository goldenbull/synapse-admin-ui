import datetime
import logging
import time
from pprint import pprint
import arrow
import requests
import json

host = "http://localhost:8008"
admin_token = "syt_YWRtaW4_EiCPJozmnOpQAzhxzusB_3PCsxv"
headers = {"Authorization": f"Bearer {admin_token}"}
user_id = "@yiyangqianniu2.0:data.sfuc9tsqc4qwkjm.com"
room_id = "!cZKVGapltTxGoZfbMO:data.sfuc9tsqc4qwkjm.com"


def list_users():
    url = "/_synapse/admin/v2/users?from=0&limit=100&guests=false"
    rsp = requests.get(f"{host}{url}", headers=headers)
    data = rsp.json()
    pprint(data)
    users = data["users"]
    for user in users:
        print(user["displayname"], user["name"])
    return users


def query_all_user_session(users):
    for user in users:
        url = f"/_synapse/admin/v1/whois/{user['name']}"
        rsp = requests.get(f"{host}{url}", headers=headers)
        data = rsp.json()
        connections = data["devices"][""]["sessions"][0]["connections"]
        if len(connections) > 0:
            ts = max(c["last_seen"] for c in connections)
            print(user['displayname'], datetime.datetime.fromtimestamp(ts / 1000).isoformat())


def list_rooms():
    url = "/_synapse/admin/v1/rooms"
    rsp = requests.get(f"{host}{url}", headers=headers)
    data = rsp.json()
    for r in data["rooms"]:
        if r["name"] is not None:
            print(r["name"])


def change_username():
    url = "/_synapse/admin/v2/users/<user_id>".replace("<user_id>", user_id)
    rsp = requests.put(f"{host}{url}",
                       json.dumps({"displayname": "刘博"}),
                       headers=headers
                       )
    print(rsp.json())


def list_activities():
    users = list_users()
    print("=" * 80)
    for user in users:
        try:
            url = f"{host}/_synapse/admin/v2/users/{user['name']}/devices"
            rsp = requests.get(url, headers=headers)
            devices = rsp.json()["devices"]
            max_ts = max(d["last_seen_ts"] for d in devices)
            print(user["displayname"], arrow.get(max_ts, tzinfo="local"))
        except:
            pass


def send_server_notice():
    url = "/_synapse/admin/v1/send_server_notice"
    data = {
        "user_id": user_id,
        "content": {
            "msgtype": "m.text",
            "body": "这是一条测试信息，测试管理员广播消息的功能"
        }
    }
    rsp = requests.post(f"{host}{url}",
                        json.dumps(data),
                        headers=headers)
    print(rsp.json())


def broadcast_server_notice():
    users = list_users()
    url = "/_synapse/admin/v1/send_server_notice"
    for user in users:
        while True:
            user_id = user["name"]
            logging.info(f"sending notice to {user_id}")
            data = {
                "user_id": user_id,
                "content": {
                    "msgtype": "m.text",
                    "body": "Important Notice: This server will be stopped permanently in one month. Please move to other servers. Goodbye."
                }
            }
            rsp = requests.post(f"{host}{url}",
                                json.dumps(data),
                                headers=headers)
            status = rsp.json()
            logging.info(status)
            if "error" not in status:
                break

            # retry
            time.sleep(1)


def delete_room():
    url = f"/_synapse/admin/v1/rooms/{room_id}"
    data = {
        "message": "Room deleted by admin"
    }
    rsp = requests.delete(f"{host}{url}",
                          data=json.dumps(data),
                          headers=headers)
    print(rsp.json())


def show_server_version():
    url = f"/_synapse/admin/v1/server_version"
    print(requests.get(f"{host}{url}", headers=headers).json())


def reset_user_passwd():
    url = f"/_synapse/admin/v1/reset_password/{user_id}"
    data = {
        "new_password": "wwRT49PMH72YUCPDzbaPMsjy",
        "logout_devices": True
    }
    rsp = requests.post(f"{host}{url}",
                        data=json.dumps(data),
                        headers=headers)
    print(rsp.json())


def list_messages():
    url = f"/_synapse/admin/v1/rooms/{room_id}/messages?dir=b"
    pprint(requests.get(f"{host}{url}", headers=headers).json())


def purge_media():
    url = "POST /_synapse/admin/v1/media/delete?before_ts=<before_ts>"


def disable_user():
    to_del = "@pijiu:fight.haohaoxuexi.live"
    url = f"/_synapse/admin/v1/deactivate/{to_del}"
    data = {"erase": True}
    rsp = requests.post(f"{host}{url}",
                        data=json.dumps(data),
                        headers=headers)
    print(rsp.json())


if __name__ == '__main__':
    FORMAT = '%(asctime)s.%(msecs)03d,[%(levelname)s],%(process)5d,%(filename)s:%(lineno)4d,[%(funcName)s], %(message)s'
    DATEFMT = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)
    # users = list_users()
    # query_all_user_session(users)
    # list_activities()
    # reset_user_passwd()
    # list_rooms()
    # change_username()
    # print(arrow.get(1655821187104))
    # send_server_notice()
    # delete_room()
    # show_server_version()
    # list_messages()
    # disable_user()
    broadcast_server_notice()
