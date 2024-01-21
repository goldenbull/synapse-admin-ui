<template>
  <div class="grid">

    <!-- user list -->
    <div class="col-8">
      <DataTable :value="data"
                 selectionMode="single"
                 v-model:selection="selectedUser"
                 dataKey="name"
                 @rowSelect="onRowSelect"
                 sortField="name"
                 :sortOrder="-1"
                 removableSort
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
      <Button class="m-2" @click="reload(true)">Reload</Button>
    </div>

    <!-- selected user detail -->
    <div class="col-4">
      <Panel :header="selectedUser['name']">
        <DataTable :value="selectedUserData">
          <Column field="field" header="field"></Column>
          <Column field="value" header="value"></Column>
        </DataTable>
      </Panel>
    </div>

  </div>
</template>

<script setup lang="ts">

import {ref} from 'vue';
import {useStore} from "@/data/store";
import axios from "axios";
import Column from "primevue/column";
import DataTable, {type DataTableRowSelectEvent} from "primevue/datatable";
import Button from "primevue/button";
import Panel from "primevue/panel";

const store = useStore();
let data = ref();
let selectedUser = ref<any>({"name": null});
let selectedUserData = ref();

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

function onRowSelect(evt: DataTableRowSelectEvent) {
  let data = [];
  for (const x in selectedUser.value) {
    if (x == "name")
      continue; //skip name field
    data.push({"field": x, "value": selectedUser.value[x]});
  }
  selectedUserData.value = data;
}

</script>

<style scoped>
</style>
