<template>
  <div class="container">
    <n-space vertical size="large">

      <div v-show="selected()">
        <n-form ref="formRef" inline :label-width="80" :model="formValue" :size="'large'">
          <n-form-item label="姓名" path="user.name">
            <n-input v-model:value="formValue.name" placeholder="输入姓名" />
          </n-form-item>
          <n-form-item label="学号" path="user.code">
            <n-input v-model:value="formValue.code" placeholder="输入学号" />
          </n-form-item>
          <n-form-item>
            <n-button attr-type="button" @click="checkIn()">
              签到
            </n-button>
          </n-form-item>
        </n-form>
      </div>

      <n-layout>
        <n-layout-header>
          <h1 style="margin: 0; padding: 0;">{{ classRoomName }} 讲台</h1>
        </n-layout-header>
        <n-layout-content content-style="padding: 24px;">
          <n-table :bordered="true" :single-line="false" :size="'large'">
            <thead>
              <tr>
                <th v-for="idx in columns" style="text-align: center; align-content: center;">
                  {{ idx }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="seat_col in seats">
                <td v-for="seat in seat_col">
                  <span v-if="seat.text.length > 0">
                    {{ seat.text }}
                  </span>
                  <span v-else>
                    <span v-if="selected() && seat.x == selectedPosition.x && seat.y == selectedPosition.y">
                      签到中
                    </span>
                    <span v-else-if="selected()">
                      点击签到
                    </span>
                    <span v-else>
                      <a href="javascript:void(0);" @click="showCheckInForm(seat.x, seat.y)">点击签到</a>
                    </span>
                  </span>
                </td>
              </tr>
            </tbody>
          </n-table>
        </n-layout-content>
        <n-layout-footer>Copyright by WH0ever®</n-layout-footer>
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

import { defineComponent, onMounted, ref } from 'vue';
import {
  NTable,
  NLayout,
  NLayoutHeader,
  NLayoutFooter,
  NLayoutContent,
  NSpace,
  NForm,
  NFormItem,
  NButton,
  NInput,
} from 'naive-ui'

class Seat {
  public text: string = ''
  public x: number = -1
  public y: number = -1
}

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
    NFormItem,
    NButton,
    NInput,
  },
  setup() {
    const classRoomName = ref('')
    const columns = ref(8)
    const rows = ref(6)
    const checked = ref(Array<any>())
    const formValue = ref({ name: '', code: '' })
    const selectedPosition = ref({ x: -1, y: -1 })
    const seats = ref(Array<Array<Seat>>())

    function showCheckInForm(x: number, y: number): void {
      selectedPosition.value.x = x
      selectedPosition.value.y = y
    }

    async function checkIn() {
      try {
        const url = `/v1/api/checkin/${selectedPosition.value.x},${selectedPosition.value.y}`
        const res = await axios.post(url, formValue.value)
        if (res.status !== 200) {
          alert('请求API失败！')
          return
        }
        if (res.data.code !== 0) {
          alert(res.data.message)
          return
        }
        alert('签到成功')
      } catch (err) {
        alert(`发生错误：${err}`)
        return
      }
    }

    function selected(): boolean {
      return selectedPosition.value.x >= 0
        && selectedPosition.value.x < columns.value
        && selectedPosition.value.y >= 0
        && selectedPosition.value.y < rows.value
    }

    function allLabels(): void {
      for (let i = 0; i < rows.value; i++) {
        seats.value.push(Array<Seat>())
        for (let j = 0; j < columns.value; j++) {
          const seat = new Seat()
          seat.y = i
          seat.x = j
          seats.value[i].push(seat)
        }
      }
      console.log(checked.value)
      for (let _ in checked.value) {
        const c: any = checked.value[_]
        console.log(c)

        seats.value[c.y][c.x].text = c.name
      }
    }

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
        classRoomName.value = res.data.data.classroom.name
        columns.value = res.data.data.classroom.columns
        rows.value = res.data.data.classroom.rows
        checked.value = res.data.data.checkin
        allLabels()
      } catch (err) {
        alert(`发生错误：${err}`)
        return
      }
    })
    return {
      classRoomName, columns, rows, checked, formValue,
      selected, selectedPosition, seats, showCheckInForm,
      checkIn,
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
