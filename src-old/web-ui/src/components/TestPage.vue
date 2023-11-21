<template>
  <h1>Test Page</h1>
  <div class="row">
    <ag-grid-vue
        class="ag-theme-alpine"
        style="height: 600px"
        :columnDefs="columnDefs"
        :rowData="rowData"
        :defaultColDef="defaultColDef"
        rowSelection="single"
        animateRows="true"
        pagination="true"
        paginationAutoPageSize="true"
        @cell-clicked="cellWasClicked"
        @grid-ready="onGridReady"
    />
  </div>
  <button @click="purge()">Purge!</button>
  <div class="row"><p class="text-break">{{ debug_msg }}</p></div>
</template>

<script setup lang="ts">

import {AgGridVue} from "ag-grid-vue3";
import {GridApi, GridReadyEvent} from "ag-grid-community";
import "ag-grid-community/dist/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/dist/styles/ag-theme-alpine.css"; // Optional theme CSS

import {ref, onMounted} from 'vue';
import axios from "axios";

const debug_msg = ref("");
const gridApi = ref(null as GridApi | null); // Optional - for accessing Grid's API

// Obtain API from grid's onGridReady event
function onGridReady(params: GridReadyEvent) {
  gridApi.value = params.api;
}

function cellWasClicked(event: any) { // Example of consuming Grid Event
  console.log("cell was clicked", event);
}

function deselectRows(evt: any) {
  gridApi.value?.deselectAll();
}

const rowData = ref([]); // Set rowData to Array of Objects, one Object per Row
const room_id = "!hhysVhsfJUWruHTJsQ:node16";

// Each Column Definition results in one Column.
const columnDefs = ref([
  {field: "age"},
  {field: "event_id"},
  {field: "sender"},
  {field: "type"},
  {field: "user_id"},
  {field: "ts"},
]);

// DefaultColDef sets props common to all Columns
const defaultColDef = {
  sortable: true,
  filter: true,
};

onMounted(() => {
});

function purge() {
}

</script>

<style scoped>

</style>