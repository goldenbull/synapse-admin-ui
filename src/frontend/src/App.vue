<template>

  <!-- 主菜单 -->
  <header class="flex fixed h-5rem left-0 top-0 w-full px-5 py-3 shadow-2 z-5 bg-white">
    <router-link to="/config">
      <Button class="mx-2">Config</Button>
    </router-link>
    <router-link v-if="store.isConfigurated" to="/users">
      <Button class="mx-2">Users</Button>
    </router-link>
    <router-link v-if="store.isConfigurated" to="/rooms">
      <Button class="mx-2">Rooms</Button>
    </router-link>
    <router-link v-if="store.isConfigurated" to="/purge">
      <Button class="mx-2">Purge</Button>
    </router-link>
    <router-link to="/test">
      <Button class="mx-2">Test</Button>
    </router-link>
  </header>

  <!-- 主面板 -->
  <main class="px-1 pt-6 mt-6 pb-1 absolute top-0 left-0">
    <!--    <p>debug</p>-->
    <!--    <div class="border-3 border-blue-100 p-4">-->
    <router-view></router-view>
    <!--    </div>-->
  </main>

</template>

<script setup lang="ts">

import Button from "primevue/button";
import {useStore} from "@/data/store";

const store = useStore();

</script>
