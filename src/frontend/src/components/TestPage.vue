<template>
  <h1>Test Page</h1>
  <div class="row">

  </div>
  <button @click="purge()">Purge!</button>
  <div class="row"><p class="text-break">{{ debug_msg }}</p></div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import axios from "axios";

const debug_msg = ref("");

function purge() {
}

</script>

<style scoped>

</style>