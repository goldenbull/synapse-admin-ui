<template>
  <h1>Purge history</h1>
  <div class="row m-2">
    <Datepicker
        v-model="purge_timepoint"
        inline
        inlineWithInput
        auto-apply
    />
  </div>
  <div class="row m-2">
    <p class="text-break">
      server端删除指定日期之前的全部消息、文件、图片，需要在postgres中运行vacuum full以回收空间
    </p>
  </div>
  <div class="m-2">
    <button class="btn-primary" @click="purge()">Purge!</button>
  </div>
  <div class="row m-2">
    <div class="overflow-scroll" style="height: 500px">
      <p class="text-break m-0" v-for="msg in debug_msg.reverse()">{{ msg }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">

import {ref, onMounted} from 'vue';
import {DateTime} from "luxon";
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import axios, {AxiosError} from "axios";
import {useStore} from "../data/store";

const store = useStore();
const purge_timepoint = ref(new Date());
const debug_msg = ref([""]);

onMounted(() => {
  // 初始化，默认为一周以前
  purge_timepoint.value = DateTime.local().minus({week: 1}).toJSDate();
});

function dumpError(err: unknown) {
  const rsp = (err as AxiosError)?.response;
  if (rsp) {
    debug_msg.value.push(`status=[${rsp.status}]${rsp.statusText}, ${JSON.stringify(rsp.data)}`);
  } else {
    debug_msg.value.push(JSON.stringify(err));
  }
}

async function purge() {
  // 清除全部数据
  debug_msg.value = [`删除 ${store.server_name} 上位于 ${DateTime.fromJSDate(purge_timepoint.value).toISO()} 之前的数据`];
  const ts = purge_timepoint.value.getTime();

  // 先删除media
  debug_msg.value.push(`删除${store.server_name}上的media...`);
  try {
    const rsp = await axios.post(`proxy/_synapse/admin/v1/media/${store.server_name}/delete?before_ts=${ts}`,
        {},
        {headers: {"Authorization": "Bearer " + store.token}});
    debug_msg.value.push(`status=[${rsp.status}]${rsp.statusText}, 已删除${rsp.data["total"]}个media`);
  } catch (err) {
    dumpError(err);
  }

  // 获得room列表
  let rooms = [] as Array<any>;
  try {
    const rsp = await axios.get("/proxy/_synapse/admin/v1/rooms?limit=10000",
        {headers: {"Authorization": "Bearer " + store.token}});
    rooms = rsp.data["rooms"];
    debug_msg.value.push(`一共有${rooms.length}个room`);
  } catch (err) {
    dumpError(err);
  }

  // 然后逐个room删除历史记录
  for (let room of rooms) {
    try {
      const rsp = await axios.post(`/proxy/_synapse/admin/v1/purge_history/${room["room_id"]}`,
          {
            delete_local_events: true,
            purge_up_to_ts: ts,
          },
          {headers: {"Authorization": "Bearer " + store.token}});
      debug_msg.value.push(`room name=${room["name"]}, room_id=${room["room_id"]}, [${rsp.status}]${rsp.statusText}`);
    } catch (err) {
      dumpError(err);
    }
  }

  debug_msg.value.push(`============ 清理完毕 =================`);

  // delete local media of one user
  // axios.delete(`proxy/_synapse/admin/v1/users/@admin:node16/media`,
  //     {headers: {"Authorization": "Bearer " + store.token}}).then(rsp => {
  //   console.log(rsp);
  // }).catch(err => {
  //   console.log(err);
  // })

}

</script>

<style scoped>

</style>