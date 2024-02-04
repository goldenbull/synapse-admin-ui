# -*- coding: utf-8 -*-

import logging
import pickle
from dataclasses import dataclass
import uvicorn
from pprint import pprint
import arrow
import requests
import json
from arrow import Arrow
from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
import pandas as pd
import numpy as np
import os


# region global vars

@dataclass
class GlobalVars:
    pgsql_dsn: str = "postgresql://synapse_user:4dCPPJKLnCNoJTANShTQWErasdwO@localhost:5432/synapse"
    admin_token: str = "syt_YWRtaW4_EiCPJozmnOpQAzhxzusB_3PCsxv"
    host: str = "http://localhost:8008"
    conn: connection = None
    prev_load_user: Arrow = arrow.get(0)
    all_users = []

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.admin_token}"}

    def merge_url(self, url: str):
        return f"{self.host}{url}"

    def get_conn(self):
        if self.conn is None:
            self.conn = psycopg2.connect(dsn=self.pgsql_dsn)
        return self.conn


_g = GlobalVars()

# endregion

# region setup webapp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("../frontend/dist", exist_ok=True)
app.mount("/ui", StaticFiles(directory="../frontend/dist", html=True), name="ui")


# endregion


# homepage
@app.get("/")
def index():
    return RedirectResponse("/ui")


# region http api getters

@app.get("/api/echo")
def echo():
    return str(arrow.get())


def to_str(b: bool):
    return "true" if b else "false"


@app.post("/api/savecfg")
async def savecfg(data=Body(None)):
    pprint(data)
    _g.pgsql_dsn = data["connstr"]
    _g.admin_token = data["token"]
    logging.info("config saved")
    return True


@app.get("/api/all-users")
def read_item(deactivated: bool = False, force_reload: bool = False):
    # 提供cache机制
    os.makedirs("./cache", exist_ok=True)
    cache_fname = "./cache/all-users.pkl"
    if not force_reload:
        _g.all_users = None
        try:
            _g.all_users = pickle.load(open(cache_fname, "rb"))
        except Exception:
            logging.exception("can not read users from cache")

    if force_reload or _g.all_users is None:
        print("=== reload all users ===")
        next_token = 0
        users = []
        while True:
            url = f"/_synapse/admin/v2/users?from={next_token}&limit=100&guests=false&deactivated={to_str(deactivated)}"
            print(_g.headers)
            rsp = requests.get(_g.merge_url(url), headers=_g.headers)
            data = rsp.json()
            print(type(data))
            print(data)
            cur_users = data["users"]
            next_token = data["next_token"] if "next_token" in data else -1
            logging.info(f"get {len(cur_users)} from server, next token: {next_token}")
            users.extend(cur_users)
            if next_token == -1:
                break

        # update cache
        _g.prev_load_user = arrow.get()
        _g.all_users = users
        pickle.dump(_g.all_users, open(cache_fname, "wb"))

    return _g.all_users


@app.get("/api/list-inactive")
def list_inactive():
    cur = _g.get_conn().cursor(cursor_factory=RealDictCursor)
    sql = """SELECT user_id, device_id, user_agent, TO_TIMESTAMP(last_seen / 1000) AS "last_seen"
             FROM devices
             WHERE last_seen < DATE_PART('epoch', NOW() - INTERVAL '1 month') * 1000
             order by last_seen; """
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return data


@app.get("/api/rooms")
def list_rooms():
    url = "/_synapse/admin/v1/rooms"
    rsp = requests.get(_g.merge_url(url), headers=_g.headers)
    data = rsp.json()
    return data["rooms"]


@app.get("/api/data0")
def test_table_data0():
    data: pd.DataFrame = pd.DataFrame(index=list(range(100)))
    data["code"] = data.index.map('code{:06d}'.format)
    ts = list(arrow.Arrow.range("minute", arrow.get().ceil("second"), limit=len(data)))
    data["timestamp"] = pd.to_datetime([t.naive for t in ts])
    data["timestamp"] += pd.to_timedelta(np.random.randint(0, 10000000, len(data)), "ns")
    data["timestamp_str1"] = data["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S.%f") + \
                             data["timestamp"].dt.nanosecond.map("{:03d}".format)
    data["timestamp_str2"] = data["timestamp"].apply(lambda t: t.isoformat())
    data["close"] = np.random.rand(len(data))
    data["volume"] = np.random.rand(len(data)) * 10000
    # return json.loads(data.to_json(orient="records", date_format="iso", date_unit="us"))
    return data.to_dict(orient="records")


# endregion

def send_server_notice():
    url = "/_synapse/admin/v1/send_server_notice"
    data = {
        "user_id": user_id,
        "content": {
            "msgtype": "m.text",
            "body": "这是一条测试信息，测试管理员广播消息的功能"
        }
    }
    rsp = requests.post(_g.merge_url(url),
                        json.dumps(data),
                        headers=_g.headers)
    print(rsp.json())


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True, log_level=logging.INFO)
