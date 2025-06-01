<template>
  <div class="info-manage">
    <div class="table-title">
      <h2>信息管理</h2>
      <button class="btn-primary" @click="showUpload = true">上传新用户</button>
    </div>

    <!-- 上传表单弹窗 -->
    <div v-if="showUpload" class="upload-overlay" @click.self="showUpload = false">
      <div class="upload-modal">
        <h3>添加新用户</h3>
        <input v-model="form.name" placeholder="姓名" />
        <input v-model="form.student_id" placeholder="学号" />
        <input type="file" @change="handleFileChange" />
        <div class="modal-buttons">
          <button class="btn-primary" @click="submitUpload">提交</button>
          <button class="btn-cancel" @click="showUpload = false">取消</button>
        </div>
      </div>
    </div>

    <div class="table-content">
      <table>
        <thead>
          <tr>
            <th>姓名</th>
            <th>学号</th>
            <th>照片</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in userStore.users" :key="user.id" class="table-row">
            <td>{{ user.name }}</td>
            <td>{{ user.student_id }}</td>
            <td><img :src="`data:${user.mime_type};base64,${user.photo_base64}`" alt="头像" class="avatar" /></td>
            <td><button class="btn-danger" @click="() => userStore.deleteUser(user.id)">删除</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'

const showUpload = ref(false)
const userStore = useUserStore()
const form = ref({
  name: '',
  student_id: '',
  photo: null
})

function handleFileChange(e) {
  form.value.photo = e.target.files[0]
}

async function submitUpload() {
  if (!form.value.name || !form.value.student_id || !form.value.photo) {
    alert('请填写完整信息并上传照片')
    return
  }
  await userStore.uploadUser(form.value)
  showUpload.value = false
  form.value = { name: '', student_id: '', photo: null }
}

onMounted(() => {
  userStore.loadUsers()
  console.log('加载成功')
})
</script>

<style scoped>
.info-manage {
  padding: 24px 32px;
  background-color: #f8fafc;
  min-height: 100%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

/* 标题栏 */
.table-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.table-title h2 {
  font-weight: 700;
  font-size: 24px;
  color: #2c3e50;
}

/* 按钮基础样式 */
button {
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  border: none;
  outline: none;
  transition: all 0.3s ease;
  user-select: none;
  padding: 8px 18px;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgb(0 0 0 / 0.1);
}

/* 主要按钮 - 蓝绿色渐变 */
.btn-primary {
  background-color: rgb(48, 151, 152);
  color: #fff;
  box-shadow: 0 4px 12px rgba(58, 175, 169, 0.4);
}
.btn-primary:hover {
  background-color:  #2b7a78;
  box-shadow: 0 2px 3px rgba(43, 122, 120, 0.6);
}

/* 取消按钮 */
.btn-cancel {
  background-color: #e0e0e0;
  color: #555;
  box-shadow: none;
  margin-left: 12px;
}
.btn-cancel:hover {
  background-color: #c7c7c7;
}

/* 删除按钮 - 红色 */
.btn-danger {
  background-color: #e74c3c;
  color: white;
  padding: 6px 14px;
  font-size: 13px;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
}
.btn-danger:hover {
  background-color: #c0392b;
  box-shadow: 0 4px 12px rgba(192, 57, 43, 0.5);
}

/* 表格 */
.table-content table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
  font-size: 15px;
  color: #34495e;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

thead tr {
  background-color: #3aafa9;
  color: white;
  font-weight: 600;
  font-size: 16px;
  border-radius: 10px;
}

thead th {
  padding: 14px 12px;
  text-align: center;
}

tbody tr {
  background: white;
  transition: background-color 0.2s ease;
  cursor: default;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

tbody tr:hover {
  background-color: #d3f3f1;
}

tbody td {
  padding: 14px 12px;
  text-align: center;
  vertical-align: middle;
  border-radius: 10px;
}

/* 图片头像 */
.avatar {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgb(58 175 169 / 0.4);
}

/* 上传弹窗遮罩 */
.upload-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* 上传弹窗主体 */
.upload-modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  padding: 32px 40px;
  width: 380px;
  max-width: 90vw;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.upload-modal h3 {
  margin: 0 0 12px 0;
  font-weight: 700;
  font-size: 22px;
  color: #2c3e50;
  text-align: center;
}

.upload-modal input{
  padding: 17px 12px;
  font-size: 15px;
  border: 1.8px solid #bbb;
  border-radius: 8px;
  outline-color: #3aafa9;
}
.upload-modal input[type='file'] {
  padding: 17px 12px;
  font-size: 15px;
  border: 1.8px solid #bbb;
  border-radius: 8px;
  outline-color: #3aafa9;
  transition: border-color 0.3s ease;
}

.upload-modal input[type='text']:focus,
.upload-modal input[type='file']:focus {
  border-color: #2b7a78;
}

/* 弹窗按钮排布 */
.modal-buttons {
  display: flex;
  justify-content: center;
  margin-top: 8px;
}
</style>

