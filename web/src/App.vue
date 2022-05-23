<template>
  <div class="container">
    <!-- container设置了position:relative -->
    <n-layout position="absolute">
      <h1>讲台</h1>
      <n-table :bordered="false" :single-line="false">
        <thead>
          <tr>

            <th>01</th>
            <th>Abormal</th>
            <th>Abolish</th>
            <th>...</th>
            <th>万事开头难</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>放弃</td>
            <td>反常的</td>
            <td>彻底废除</td>
            <td>...</td>
            <td>干！我刚才背的是啥</td>
          </tr>
          <tr>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
          </tr>
        </tbody>
      </n-table>
    </n-layout>
  </div>
</template>

<script lang="ts">
import 'naive-ui'
import 'vfonts/Lato.css' // 通用字体
import 'vfonts/FiraCode.css' // 等宽字体

import axios from 'axios'

import { defineComponent, onMounted } from 'vue';
import { NTable } from 'naive-ui'


export default defineComponent({
  name: 'App',
  components: {
    NTable,
  },
  setup() {
    onMounted(async () => {
      // const classroomInfo = await axios.get('/v1/api/checkin')
      
    })
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
