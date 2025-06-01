<template>
  <el-calendar class="custom-calendar">
    <template #date-cell="{ data }">
      <div class="calendar-cell">
        <div>{{ dayjs(data.date).format('D') }}日</div>
        <div v-if="hasStats(dayjs(data.date).format('YYYY-MM-DD'))">
          <div>应到: {{ statsMap[dayjs(data.date).format('YYYY-MM-DD')].expected }}</div>
          <div>实到: {{ statsMap[dayjs(data.date).format('YYYY-MM-DD')].actual }}</div>
          <div>最早: {{ statsMap[dayjs(data.date).format('YYYY-MM-DD')].earliest_time }}</div>
        </div>
      </div>
    </template>
  </el-calendar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import dayjs from 'dayjs'
import { getStats } from '../stores/sign'

const statsMap = ref({})

const hasStats = (date) => {
  return statsMap.value[date]?.expected !== undefined
}

onMounted(async () => {
  try {
    const defaultStats = {}
    for (let i = 1; i <= 31; i++) {
      const date = `2025-05-${i.toString().padStart(2, '0')}`
      defaultStats[date] = {}
    }

    const data = await getStats()
    console.log('getStats 返回的数据:', data)

    if (Array.isArray(data)) {
      const dbStats = Object.fromEntries(
        data.map(item => [item.date, item])
      )
      statsMap.value = { ...defaultStats, ...dbStats }
      console.log('生成的 statsMap:', statsMap.value)
    } else {
      console.warn('获取的签到统计数据不是数组:', data)
      statsMap.value = defaultStats
    }
  } catch (error) {
    console.error('获取签到统计数据失败:', error)
    statsMap.value = defaultStats
  }
})
</script>

<style>
/* 放大日历格子高度 */
.el-calendar-day {
  height: 100%;
  padding: 12px;
  box-sizing: border-box;
}

/* 美化格子内容 */
.calendar-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  font-size: 14px;
}

.calendar-cell > div:first-child {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 6px;
}



/* 调整顶部 header 区域 */
.el-calendar__header {
  padding: 20px;
  font-size: 18px;
  font-weight: bold;
}

/* 月份标题放大 */
.el-calendar__title {
  font-size: 24px;
  font-weight: bold;
}

/* 左右切换按钮 */
.el-calendar__button-group button {
  font-size: 16px;
}

.el-calendar-table__row{
    height: 120px;
}
</style>
