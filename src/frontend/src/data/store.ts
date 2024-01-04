import {defineStore} from 'pinia';
import axios, {AxiosError} from "axios";
import {router} from "@/main";

////////////////////////////////////////////////////////////////////////////////
// 全局状态的处理

export const useStore = defineStore(
    'global',
    {
        // init data here
        state: () => {
            console.log("init store");
            return {
                pgsql_conn_str: "",
                token: "",

                // 登录信息
                user_id: "",

                // users
                users: [],
                current_user_id: "",
                current_user_row_index: 0,
                current_user_page: 0,

                // rooms
                rooms: [],
                current_room_id: "",
            };
        },

        getters: {
            isConfigurated: (self) => {
                return self.pgsql_conn_str != "" && self.token != "";
            },

            isLogin: (state) => {
                return state.user_id != "" && state.token != "";
            },

            server_name: (state) => {
                // 从登陆user_id中拆出server_name
                const ss = state.user_id.split(":");
                if (ss.length == 2) {
                    return ss[1];
                } else {
                    return "";
                }
            },
        },
    }
);

/*

function check_token(user_id: string, token: string) {
    // 确保token有效，而且是admin权限
    console.log("validate token");
    return axios.get("/proxy/_synapse/admin/v2/users/" + user_id,
        {headers: {"Authorization": "Bearer " + token}})
        .then(rsp => {
            // admin登陆成功
            console.log(rsp.data);
            const store = useStore();
            store.user_id = user_id;
            store.token = token;
            localStorage.setItem("user_id", user_id);
            localStorage.setItem("token", token);
            return true;
        })
        .catch(err => {
            // admin权限检查失败
            console.log(err);
            localStorage.removeItem("user_id");
            localStorage.removeItem("token");
            if (err instanceof AxiosError)
                throw err.response;
            else
                throw err;
        });
}

export function load_storage_and_check() {
    console.log("load data from local storage");
    let user_id = localStorage.getItem("user_id") ?? "";
    let token = localStorage.getItem("token") ?? "";
    if (token != "")
        return check_token(user_id, token);
    else
        return Promise.reject("no data in localStorage");
}

export function login(username: string, password: string) {
    return axios.post("/proxy/_matrix/client/r0/login",
        {"type": "m.login.password", "user": username, "password": password}
    ).then(async rsp => {
        const data = rsp.data;
        console.log(data);
        return check_token(data["user_id"], data["access_token"]);
    }).catch(err => {
        console.log("login failed");
        if (err instanceof AxiosError)
            throw err.response;
        else
            throw err;
    }).then(ret => {
        return router.push("/users");
    });
}

export async function logout() {
    const store = useStore();
    store.user_id = "";
    store.token = "";
    localStorage.removeItem("user_id");
    localStorage.removeItem("token");
    await router.push("/login");
}
*/