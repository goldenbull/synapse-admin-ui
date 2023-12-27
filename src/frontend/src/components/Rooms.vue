<template>
  <h1>Rooms</h1>

  <div class="row">current room id is {{ store.current_room_id }}</div>
  <div class="row"><p class="text-break">{{ debug_msg }}</p></div>
</template>

<script setup lang="ts">

import {ref, onMounted, reactive} from 'vue';
import {useStore} from "@/data/store";
import axios from "axios";

const store = useStore();
const cur_room = ref({});
const debug_msg = ref("");

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


</script>

<style scoped>
</style>
