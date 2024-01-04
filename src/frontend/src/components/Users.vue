<template>
  <DataTable :value="data"
             resizableColumns
             columnResizeMode="fit"
             showGridlines
             stripedRows
             paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]"
             class="border-3"
  >
    <Column field="name" sortable header="name"></Column>
    <Column field="admin" header="admin"></Column>
    <Column field="deactivated" header="deactivated"></Column>
    <Column field="displayname" header="displayname"></Column>
    <Column field="creation_ts" header="creation"></Column>
  </DataTable>
  <Button @click="reload(true)">Reload</Button>
</template>

<script setup lang="ts">

import {ref} from 'vue';
import {useStore} from "@/data/store";
import axios from "axios";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import Button from "primevue/button";

const store = useStore();
let data = ref();

function reload(force: boolean) {
  axios.get(
      "/all-users",
      {
        params: {
          deactivated: true,
          force_reload: force
        }
      })
      .then(
          rsp => {
            data.value = rsp.data;
          });
}

reload(false);

</script>

<style scoped>
</style>
