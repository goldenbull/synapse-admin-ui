import datetime
import pprint
import arrow
import requests
import json

host = "http://localhost:8008"
admin_token = "syt_YWRtaW4_OcNnpGDumDEkiYeyPXas_0yuOxS"
headers = {"Authorization": f"Bearer {admin_token}"}
user_id = "@winnie_emperor:data.sfuc9tsqc4qwkjm.com"


def list_users():
    url = "/_synapse/admin/v2/users?from=0&limit=100&guests=false"
    rsp = requests.get(f"{host}{url}", headers=headers)
    data = rsp.json()
    pprint.pprint(data)
    users = data["users"]
    for user in users:
        print(user["displayname"], user["name"])
    return users


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


if __name__ == '__main__':
    # list_users()
    # list_activities()
    # list_rooms()
    # change_username()
    # print(arrow.get(1655821187104))
    send_server_notice()
