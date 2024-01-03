<template>
  <div class="flex fixed h-5rem left-0 top-0 w-full px-5 py-0 bg-white shadow-2 z-5">
<!--  <div class="layout-topbar">-->
    <p>hello</p>
  </div>

  <div class="layout-main-container">
    <h1>hello</h1>
    <h2 v-for="x in data">this is {{ x }}</h2>
  </div>
  <!--  <div class="container-fluid">-->
  <!--    <nav class="navbar navbar-expand-lg bg-light">-->
  <!--      <ul class="navbar-nav me-auto mb-2 mb-lg-0">-->
  <!--        <li v-if="!store.isLogin" class="nav-item">-->
  <!--          <router-link class="nav-link" to="/login">Login</router-link>-->
  <!--        </li>-->
  <!--        <li v-if="store.isLogin" class="nav-item">-->
  <!--          <router-link class="nav-link" to="/users">Users</router-link>-->
  <!--        </li>-->
  <!--        <li v-if="store.isLogin" class="nav-item">-->
  <!--          <router-link class="nav-link" to="/rooms">Rooms</router-link>-->
  <!--        </li>-->
  <!--        <li v-if="store.isLogin" class="nav-item">-->
  <!--          <router-link class="nav-link" to="/purge">Purge</router-link>-->
  <!--        </li>-->
  <!--        <li v-if="store.isLogin" class="nav-item">-->
  <!--          <a class="nav-link" href="#" @click="logout()">Logout</a>-->
  <!--        </li>-->
  <!--      </ul>-->
  <!--      <router-link class="nav-link" to="/test">Test</router-link>-->
  <!--    </nav>-->

  <!--    <router-view></router-view>-->
  <!--    <DataTable :value="data"-->
  <!--               resizableColumns-->
  <!--               columnResizeMode="fit"-->
  <!--               showGridlines-->
  <!--               stripedRows-->
  <!--               paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]"-->
  <!--               tableStyle="min-width: 100rem">-->
  <!--      <Column field="code" sortable header="Code"></Column>-->
  <!--      <Column field="timestamp_str1" sortable header="ts1"></Column>-->
  <!--      <Column field="timestamp_str2" header="ts2"></Column>-->
  <!--      <Column field="close" header="Price"></Column>-->
  <!--      <Column field="volume" header="Vol"></Column>-->
  <!--    </DataTable>-->
  <!--  </div>-->


</template>

<script setup lang="ts">
import {useStore} from "./data/store";
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional
import {ref} from "vue";
import axios from "axios";

const store = useStore();
let data = ref();

axios.get("/data0")
    .then(rsp => {
      data.value = rsp.data;
    });

</script>

<style scoped>
.layout-topbar {
  position: fixed;
  height: 5rem;
  z-index: 997;
  left: 0;
  top: 0;
  width: 100%;
  padding: 0 2rem;
  background-color: var(--surface-card);
  display: flex;
  box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.02), 0px 0px 2px rgba(0, 0, 0, 0.05), 0px 1px 4px rgba(0, 0, 0, 0.08);
}

.layout-main-container {
  display: flex;
  flex-direction: column;
  padding: 6rem 1rem 1rem 1rem;
}

</style>