<template>
  <div class="container">
    <n-space vertical size="large">

      <div v-show="selected()">
        <n-form
            ref="formRef"
            inline
            :label-width="80"
            :model="formValue"
            :size="'large'"
        >
          <n-form-item label="姓名" path="user.name">
            <n-input v-model="formValue.name" placeholder="输入姓名"/>
          </n-form-item>
          <n-form-item label="学号" path="user.code">
            <n-input v-model="formValue.code" placeholder="输入学号"/>
          </n-form-item>
          <n-form-item>
            <n-button attr-type="button" @click="">
              签到
            </n-button>
          </n-form-item>
        </n-form>
      </div>

      <n-layout>
        <n-layout-header><h1 style="margin: 0; padding: 0;">{{ classRoomName }} 讲台</h1></n-layout-header>
        <n-layout-content content-style="padding: 24px;">
          <n-table :bordered="true" :single-line="false" :size="'large'">
            <thead>
            <tr>
              <th v-for="idx in columns" style="text-align: center; align-content: center;">
                {{ 9 - idx }}
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="i in rows">
              <td v-for="j in columns">{{ i }},{{ j }}</td>
            </tr>
            </tbody>
          </n-table>
        </n-layout-content>
        <n-layout-footer>Copyright by whoever</n-layout-footer>
      </n-layout>
      <n-layout>
      </n-layout>
    </n-space>
  </div>
</template>

<script lang="ts">
import 'naive-ui'
import 'vfonts/Lato.css' // 通用字体
import 'vfonts/FiraCode.css' // 等宽字体

import axios from 'axios'

import {defineComponent, onMounted, ref} from 'vue';
import {
  NTable,
  NLayout,
  NLayoutHeader,
  NLayoutFooter,
  NLayoutContent,
  NSpace,
  NForm,
  NButton,
  NInput,
} from 'naive-ui'


export default defineComponent({
  name: 'App',
  components: {
    NTable,
    NLayout,
    NLayoutHeader,
    NLayoutFooter,
    NLayoutContent,
    NSpace,
    NForm,
    NButton,
    NInput,
  },
  setup() {
    const classRoomName = ref('')
    const columns = ref(8)
    const rows = ref(6)
    const checked = ref([])
    const formValue = ref({name: '', code: ''})
    const selectedPosition = ref({x: -1, y: -1})

    function selected(): boolean {
      return selectedPosition.value.x >= 0
          && selectedPosition.value.x < columns.value
          && selectedPosition.value.y >= 0
          && selectedPosition.value.y < rows.value
    }

    function allLabels(): Array<Array<string>> | undefined {
      return undefined
    }

    // function label(x: number, y: number): string {
    //   const rowX = Math.floor(x)
    //   const colY = Math.floor(y)
    //   if (rowX < 0 || rowX >= rows.value || colY < 0 || colY >= columns.value) {
    //     return ""
    //   }
    //   for (let c in checked) {
    //     let a = c as any
    //     const name =
    //   }
    //   return ""
    // }

    onMounted(async () => {
      try {
        const res = await axios.get('/v1/api/checkin')
        if (res.status !== 200) {
          alert('请求API失败！')
          return
        }
        if (res.data.code !== 0) {
          alert(res.data.message)
          return
        }
        // console.log(res.data.data.classroom)
        classRoomName.value = res.data.data.classroom.name
        columns.value = res.data.data.classroom.columns
        rows.value = res.data.data.classroom.rows
        checked.value = res.data.data.checkin
      } catch (err) {
        alert(`发生错误：${err}`)
        return
      }
    })
    return {
      classRoomName, columns, rows, checked, formValue,
      selected, selectedPosition,
    }
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

td {
  vertical-align: middle;
  text-align: center;
  padding: 0;
  margin: 0;
}

th {
  vertical-align: middle;
  text-align: center;
  padding: 0;
  margin: 0;
}
</style>
