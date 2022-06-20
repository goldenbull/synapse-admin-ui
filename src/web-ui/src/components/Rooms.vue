<template>
  <h1>Rooms</h1>
  <div class="row">
    <div class="col-9">
      <ag-grid-vue
          class="ag-theme-alpine"
          style="height: 600px"
          :columnDefs="roomListColDefs"
          :rowData="roomList"
          :defaultColDef="defaultColDef"
          rowSelection="single"
          animateRows="true"
          pagination="true"
          paginationAutoPageSize="true"
          @cell-clicked="roomListCellWasClicked"
          @grid-ready="onRoomListGridReady"
          @rowDataChanged="onDataChanged"
      />
    </div>
    <div class="col-3">
      <ag-grid-vue
          class="ag-theme-alpine"
          style="height: 600px"
          :columnDefs="roomDetailColDefs"
          :rowData="roomDetail"
          :defaultColDef="defaultColDef"
          animateRows="true"
      />
    </div>

  </div>

  <div class="row">current room id is {{ store.current_room_id }}</div>
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
const cur_room = ref({});
const debug_msg = ref("");
const gridApi = ref(null as GridApi | null); // Optional - for accessing Grid's API
const roomList = ref([]); // Set rowData to Array of Objects, one Object per Row
const roomDetail = ref([{field: "", value: null}]);

// Each Column Definition results in one Column.
const roomListColDefs = ref([
  {field: "room_id"},
  {field: "name"},
  {field: "canonical_alias"},
  {field: "joined_members"},
  {field: "joined_local_members"},
  {field: "version"},
  {field: "creator"},
  {field: "encryption"},
  {field: "federatable"},
  {field: "public"},
  {field: "join_rules"},
  {field: "guest_access"},
  {field: "history_visibility"},
  {field: "state_events"},
]);

const roomDetailColDefs = ref([{field: "field"}, {field: "value"}]);

// DefaultColDef sets props common to all Columns
const defaultColDef = {
  sortable: true,
  filter: true,
};

// Obtain API from grid's onGridReady event
function onRoomListGridReady(params: GridReadyEvent) {
  console.log("Rooms.vue onGridReady");
  gridApi.value = params.api;

  // 准备用户列表数据
  let data_promise = store.rooms.length != 0
      ? Promise.resolve(store.rooms)
      : axios.get("/proxy/_synapse/admin/v1/rooms?limit=10000",
          {headers: {"Authorization": "Bearer " + store.token}})
          .then(rsp => {
            store.rooms = rsp.data["rooms"];
            return store.rooms;
          });

  // 显示数据
  data_promise.then(rooms => {
    // 绑定
    roomList.value = rooms;
  });
}

function onDataChanged(evt: RowDataChangedEvent) {
  // 恢复选择
  // TODO
}

function roomListCellWasClicked(evt: CellClickedEvent) { // Example of consuming Grid Event
  console.log("cell was clicked", evt);
  store.current_room_id = evt.data["room_id"];
  cur_room.value = evt.data;
  debug_msg.value = JSON.stringify(cur_room.value);

  console.log(`cellWasClicked: idx=${evt.rowIndex}, pagesize=${gridApi.value?.paginationGetPageSize()}, curpage=${gridApi.value?.paginationGetCurrentPage()}`);

  // 获取room detail
  axios.get(`/proxy/_synapse/admin/v1/rooms/${store.current_room_id}`,
      {headers: {"Authorization": "Bearer " + store.token}})
      .then(rsp => {
        // dict转换为list
        const detail = rsp.data;
        roomDetail.value = Object.keys(detail).map((k) => {
          return {field: k, value: detail[k]};
        });
      });
}

function deselectRows(evt: any) {
  gridApi.value?.deselectAll();
}

</script>

<style scoped>
</style>
