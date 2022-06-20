import pprint
import requests

host = "http://localhost:8008"
admin_token = "syt_YWRtaW4_OcNnpGDumDEkiYeyPXas_0yuOxS"
headers = {"Authorization": f"Bearer {admin_token}"}


def list_users():
    url = "/_synapse/admin/v2/users?from=0&limit=100&guests=false"
    rsp = requests.get(f"{host}{url}", headers=headers)
    pprint.pprint(rsp.json())


if __name__ == '__main__':
    list_users()
