<template>

  <InputGroup>
    <InputGroupAddon class="_label"> postgres conn str</InputGroupAddon>
    <InputText class="_textbox" v-model="connstr"/>
  </InputGroup>

  <InputGroup>
    <InputGroupAddon class="_label">token</InputGroupAddon>
    <InputText class="_textbox" v-model="token"/>
  </InputGroup>

  <div class="flex justify-content-center">
    <Button class="m-2" @click="save_cfg">Save</Button>
  </div>

</template>

<script setup lang="ts">

import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import {useStore} from "@/data/store";
import {ref} from "vue";

const store = useStore();
let connstr = ref(store.pgsql_conn_str);
let token = ref(store.token);

function save_cfg() {
  store.pgsql_conn_str = connstr;
  store.token = token;
}

</script>

<style scoped>
._label {
  justify-content: flex-end;
  width: 240px;
  font-size: 1.5rem;
}

._textbox {
  width: 800px;
}
</style>