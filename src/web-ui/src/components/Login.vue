<template>
  <p>username</p>
  <input type="text" v-model="username"/>

  <p>password</p>
  <input type="password" v-model="password"/>

  <button @click="try_login()">login</button>

  <div>{{ message }}</div>
</template>

<script setup lang="ts">
import {useStore, login, load_storage_and_check} from "../data/store";
import {onMounted, ref} from "vue";
import {router} from "../main";

const store = useStore();
const username = ref("admin");
const password = ref("");
const message = ref("");

function try_login() {
  login(username.value, password.value)
      .then(ret => {
        message.value = "OK";
      })
      .catch(err => {
        message.value = JSON.stringify(err);
      });
}

console.log(`Login.vue setup, islogin=${store.isLogin}`);
onMounted(() => {
  console.log(`Login.vue onMounted, islogin=${store.isLogin}`);

  // 从localStorage加载token，验证权限，判断之前是否已经成功登陆了
  load_storage_and_check()
      .then(ret => {
        if (store.isLogin) {
          router.push("/users");
        }
      })
      .catch(err => {
        message.value = JSON.stringify(err);
      });
});

</script>

<style scoped>

</style>