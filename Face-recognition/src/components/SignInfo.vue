<template>
  <div class="info-manage">
    <div class="table-title">
      <h2>签到信息管理</h2>
    </div>

    <div class="table-content">
      <table>
        <thead>
          <tr>
            <th>时间</th>
            <th>姓名</th>
            <th>学号</th>
            <th>照片</th>
            <th>人脸检测</th>
            <th>活体检测</th>
            <th>检测结果</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sign in [...userStore.signs].reverse()" :key="sign.id">
            <td>{{ sign.time }}</td>
            <td>{{ sign.name }}</td>
            <td>{{ sign.student_id }}</td>
            <td>
              <img
                :src="`data:${sign.mime_type};base64,${sign.photo_base64}`"
                alt="头像"
                class="avatar"
              />
            </td>
            <td>{{ sign.recognition_success ? '成功' : '失败' }}</td>
            <td>{{ sign.liveness_success ? '成功' : '失败' }}</td>
            <td>{{ sign.result }}</td>
            <td>
              <button class="delete-btn" @click="() => userStore.deleteSign(sign.id)">
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSignStore } from '../stores/sign'

const userStore = useSignStore()

onMounted(() => {
  userStore.loadSigns()
  console.log('加载成功')
})
</script>

<style scoped>
.info-manage {
  padding: 24px 32px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #fafafa;
  min-height: 100%;
}

.table-title {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.table-title h2 {
  font-weight: 700;
  font-size: 24px;
  color: #333;
}

.table-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgb(0 0 0 / 0.1);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 12px;
  min-width: 900px;
}

thead tr {
  background-color: #3aafa9;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

th,
td {
  padding: 14px 12px;
  text-align: center;
  border-bottom: 1px solid #e8e8e8;
  vertical-align: middle;
}

tbody tr:hover {
  background-color: #e6f7ff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.avatar {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.15);
}

.delete-btn {
  background-color: #e76467;
  border: none;
  padding: 6px 14px;
  color: white;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.delete-btn:hover {
  background-color: #d85154;
}

@media (max-width: 768px) {
  .table-content {
    overflow-x: scroll;
  }
}
</style>
