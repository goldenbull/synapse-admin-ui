# -*- coding: utf-8 -*-

import uvicorn
import datetime
from pprint import pprint
import arrow
import requests
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/ui", StaticFiles(directory="../frontend/dist", html=True), name="ui")

host = "http://localhost:8008"
admin_token = "syt_YWRtaW4_EiCPJozmnOpQAzhxzusB_3PCsxv"
headers = {"Authorization": f"Bearer {admin_token}"}

db_conn = psycopg2.connect(database="synapse",
                           host="localhost",
                           user="synapse_user",
                           password="4dCPPJKLnCNoJTANShTQWErasdwO",
                           port="5432")


@app.get("/")
def index():
    return RedirectResponse("/ui")


@app.get("/api/users")
def read_item():
    url = "/_synapse/admin/v2/users?from=0&limit=100&guests=false"
    rsp = requests.get(f"{host}{url}", headers=headers)
    data = rsp.json()
    pprint(data)
    users = data["users"]
    return users


@app.get("/api/list-inactive")
def list_inactive():
    cur = db_conn.cursor(cursor_factory=RealDictCursor)
    sql = """SELECT user_id, device_id, user_agent, TO_TIMESTAMP(last_seen / 1000) AS "last_seen" FROM devices
           WHERE last_seen < DATE_PART('epoch', NOW() - INTERVAL '1 month') * 1000; """
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return data


@app.get("/api/rooms")
def list_rooms():
    url = "/_synapse/admin/v1/rooms"
    rsp = requests.get(f"{host}{url}", headers=headers)
    data = rsp.json()
    return data["rooms"]

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
