<script setup lang="ts">
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional
import {ref} from "vue";
import axios from "axios";


let data = ref();

axios.get("/data0")
    .then(rsp => {
      data.value = rsp.data;
    });

</script>

<template>

  <DataTable :value="data"
             resizableColumns
             columnResizeMode="fit"
             showGridlines
             stripedRows
             paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]"
             tableStyle="min-width: 100rem">
    <Column field="code" sortable header="Code"></Column>
    <Column field="timestamp_str1" sortable header="ts1"></Column>
    <Column field="timestamp_str2" header="ts2"></Column>
    <Column field="close" header="Price"></Column>
    <Column field="volume" header="Vol"></Column>
  </DataTable>

</template>
