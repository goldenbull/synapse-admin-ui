<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand-lg bg-light">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li v-if="!store.isLogin" class="nav-item">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li v-if="store.isLogin" class="nav-item">
          <router-link class="nav-link" to="/users">Users</router-link>
        </li>
        <li v-if="store.isLogin" class="nav-item">
          <router-link class="nav-link" to="/rooms">Rooms</router-link>
        </li>
        <li v-if="store.isLogin" class="nav-item">
          <router-link class="nav-link" to="/purge">Purge</router-link>
        </li>
        <li v-if="store.isLogin" class="nav-item">
          <a class="nav-link" href="#" @click="logout()">Logout</a>
        </li>
      </ul>
      <router-link class="nav-link" to="/test">Test</router-link>
    </nav>

    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import {logout, useStore} from "./data/store";

const store = useStore();
</script>

<style>
</style>
