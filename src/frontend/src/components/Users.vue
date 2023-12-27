<template>
  <h1>Users</h1>
  <div class="row">
  </div>

  <div>current user id is {{ store.current_user_id }}</div>
  <div class="row"><p class="text-break">{{ debug_msg }}</p></div>
</template>

<script setup lang="ts">

import {ref, onMounted, reactive} from 'vue';
import {useStore} from "@/data/store";
import axios from "axios";

const store = useStore();
const cur_user = ref({});
const debug_msg = ref("");

</script>

<style scoped>
</style>
