<template>
  <h1>Users</h1>
  <div class="row">
    <ag-grid-vue
        class="ag-theme-alpine"
        style="height: 600px"
        :columnDefs="columnDefs"
        :rowData="rowData.value"
        :defaultColDef="defaultColDef"
        rowSelection="single"
        animateRows="true"
        pagination="true"
        paginationAutoPageSize="true"
        @cell-clicked="cellWasClicked"
        @grid-ready="onGridReady"
        @rowDataChanged="onDataChanged"
    />
  </div>

  <div>current user id is {{ store.current_user_id }}</div>
  <div class="row"><p class="text-break">{{ debug_msg }}</p></div>
</template>

<script setup lang="ts">

import {AgGridVue} from "ag-grid-vue3";
import {GridApi, CellClickedEvent, GridReadyEvent, RowDataChangedEvent} from "ag-grid-community";
import "ag-grid-community/dist/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/dist/styles/ag-theme-alpine.css"; // Optional theme CSS

import {ref, onMounted, reactive} from 'vue';
import {useStore} from "../data/store";
import axios from "axios";

const store = useStore();
const cur_user = ref({});
const debug_msg = ref("");
const gridApi = ref(null as GridApi | null); // Optional - for accessing Grid's API
const rowData = reactive({value: []}); // Set rowData to Array of Objects, one Object per Row

// Each Column Definition results in one Column.
const columnDefs = ref([
      {field: "name"},
      {field: "displayname"},
      {field: "admin"},
      {field: "deactivated"},
      {field: "created_at"},
    ]
);

// DefaultColDef sets props common to all Columns
const defaultColDef = {
  sortable: true,
  filter: true,
};

// Obtain API from grid's onGridReady event
function onGridReady(params: GridReadyEvent) {
  console.log("Users.vue onGridReady");
  gridApi.value = params.api;

  // 准备用户列表数据
  let data_promise = store.users.length != 0
      ? Promise.resolve(store.users)
      : axios.get("/proxy/_synapse/admin/v2/users?from=0&limit=10000&guests=false",
          {headers: {"Authorization": "Bearer " + store.token}})
          .then(rsp => {
            // 时间字段格式切换
            const users = rsp.data["users"];
            for (let user of users) {
              user["created_at"] = new Date(user["creation_ts"]).toLocaleString();
            }
            store.users = users;
            return users;
          });

  // 显示数据
  data_promise.then(users => {
    // 绑定
    rowData.value = users;
  });
}

function onDataChanged(evt: RowDataChangedEvent) {
  // 恢复选择
  // if (store.current_user_id != "" && gridApi.value != null) {
  //   console.log(`onDataChanged: idx=${store.current_user_row_index}, pagesize=${gridApi.value?.paginationGetPageSize()}, curpage=${store.current_user_page}`);
  //   // search the node
  //   const model = gridApi.value.getModel();
  //   const node = model.getRow(store.current_user_row_index);
  //   node?.setSelected(true);
  //   gridApi.value.paginationGoToPage(store.current_user_page);
  // }
}

function cellWasClicked(evt: CellClickedEvent) { // Example of consuming Grid Event
  console.log("cell was clicked", evt);
  store.current_user_id = evt.data["name"];
  store.current_user_row_index = evt.rowIndex ?? 0;
  store.current_user_page = gridApi.value?.paginationGetCurrentPage() ?? 0;
  cur_user.value = evt.data;
  debug_msg.value = JSON.stringify(cur_user.value);

  console.log(`cellWasClicked: idx=${evt.rowIndex}, pagesize=${gridApi.value?.paginationGetPageSize()}, curpage=${gridApi.value?.paginationGetCurrentPage()}`);
}

function deselectRows(evt: any) {
  gridApi.value?.deselectAll();
}

</script>

<style scoped>
</style>
