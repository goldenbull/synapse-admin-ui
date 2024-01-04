<template>
  <div>{{store.pgsql_conn_str}}</div>
  <div>{{ store.token}}</div>
  <DataTable :value="data"
             resizableColumns
             columnResizeMode="fit"
             showGridlines
             stripedRows
             paginator :rows="20" :rowsPerPageOptions="[5, 10, 20, 50]"
             class="border-3"
  >
    <Column field="code" sortable header="Code"></Column>
    <Column field="timestamp_str1" sortable header="ts1"></Column>
    <Column field="timestamp_str2" header="ts2"></Column>
    <Column field="close" header="Price"></Column>
    <Column field="volume" header="Vol"></Column>
  </DataTable>
</template>

<script setup lang="ts">

import {useStore} from "@/data/store";
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

</style>