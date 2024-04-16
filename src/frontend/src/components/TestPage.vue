<template>
  <div>{{ store.pgsql_conn_str }}</div>
  <div>{{ store.token }}</div>

  <DataTable :value="items" removable-sort>
    <Column field="name" sortable header="name"/>
    <Column field="value" sortable header="value"/>
  </DataTable>

  <DataTable :value="data"
             resizableColumns
             columnResizeMode="fit"
             showGridlines
             stripedRows
             paginator :rows="20" :rowsPerPageOptions="[5, 10, 20, 50]"
             class="border-3"
  >
    <Column field="code" sortable header="Code"/>
    <Column field="timestamp" sortable header="ts"/>
    <Column field="timestamp_str1" sortable header="ts1"/>
    <Column field="timestamp_str2" header="ts2"/>
    <Column field="ts3" header="ts3"/>
    <Column field="close" header="Price"/>
    <Column field="volume" header="Vol"/>
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
import {DateTime} from "luxon";
import {DateTimeFormatter, LocalDateTime} from "@js-joda/core";

const store = useStore();

let data = ref();
axios.get("/data0")
    .then(rsp => {
      for (let i = 0; i < rsp.data.length; i++) {
        let x = rsp.data[i];
        x["ts3"] = LocalDateTime.parse(x["timestamp"]).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.nnnnnnnnn"));
      }
      data.value = rsp.data;
    });

let items = ref(
    [
      // {name: "@2833", value: "2833"},
      // {name: "@a0", value: "a0"},
      {name: "@09091a", value: "a090"},
      {name: "@a90", value: "a90"},
      {name: "@11-", value: "a11"},
      {name: "@168a", value: "a16"},
    ])

let arr = [];
for (const x of items.value) {
  arr.push(x.value);
}

// console.log(arr);
// arr.sort();
// console.log(arr);

let ss = ["a11", "a16", "a090"];
console.log("numeric=true:" + ss.sort(new Intl.Collator('en', {numeric: true}).compare));
// output: numeric=true:a11,a16,a090
console.log("numeric=false:" + ss.sort(new Intl.Collator('en', {numeric: false}).compare));
// output: numeric=false:a090,a11,a16

</script>

<style scoped>

</style>