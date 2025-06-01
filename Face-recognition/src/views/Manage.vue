<template>
  <div class="manage-container">
    <!-- 顶部标题 -->
    <div class="title">
      <h1 style="font-size: 35px;">管理后台 · 人脸识别签到系统</h1>
    </div>

    <!-- 主体区域 -->
    <div class="manage-component">
      <!-- 左侧导航 -->
      <div class="navigate">
        <div
          class="nav-item"
          :class="{ active: currentView === 'info' }"
          @click="switchView('info')"
        >
          信息管理
        </div>
        <div
          class="nav-item"
          :class="{ active: currentView === 'sign' }"
          @click="switchView('sign')"
        >
          签到信息
        </div>
        <div
          class="nav-item"
          :class="{ active: currentView === 'stats' }"
          @click="switchView('stats')"
        >
          签到统计
        </div>
        <div class="nav-item logout" @click="confirmLogout">
          <el-icon class="arrow-icon" style="vertical-align: -2px; "><ArrowLeftBold /></el-icon>退出登录
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="content">
        <ManageInfo v-if="currentView === 'info'" />
        <SignInfo v-if="currentView === 'sign'" />
        <Analyse v-if="currentView === 'stats'" />
        <div v-else-if="currentView === 'exit'" class="exit-view">
          <h2>你已退出登录</h2>
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <div class="tail">
      <p>© 2025 人脸识别签到系统管理界面</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import ManageInfo from '@/components/ManageInfo.vue'
import SignInfo from '@/components/SignInfo.vue'
import Analyse from '@/components/Analyse.vue'
import { ArrowLeftBold } from '@element-plus/icons-vue';

const currentView = ref('info')
const router = useRouter()

function switchView(view) {
  currentView.value = view
}

function confirmLogout() {
  ElMessageBox.confirm(
    '确定要退出登录吗？',
    '提示',
    {
      confirmButtonText: '退出',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      localStorage.removeItem('token')
      ElMessage.success('已退出登录')
      router.push('/signup')
    })
    .catch(() => {
      ElMessage.info('已取消退出')
    })
}
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  font-family: 'Segoe UI', sans-serif;
}

.manage-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.title {
  height: 120px;
  background: linear-gradient(135deg, #2195c6, #3ed1bd);
  display: flex;
  align-items: center;
  padding-left: 40px;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.title h1 {
  font-size: 20px;
  font-weight: bold;
  line-height: 60px;
}

.manage-component {
  flex: 1;
  display: flex;
  min-height: 0; /* 💡 关键 */
}

.navigate {
  width: 200px;
  background-color: #ffffff;
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.nav-item {
  padding: 18px 24px;
  font-size: 18px;
  color: #333;
  cursor: pointer;
  border-bottom: 1px solid #f1f1f1;
  transition: background 0.3s;
}

.nav-item:hover {
  background-color: #f5f7fa;
}

.nav-item.active {
  background-color: #e6fffd;
  color: #13a078;
  font-weight: bold;
}

.logout {
  color: #12b499;
  margin-top: auto;
  font-weight: 700;
}

.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f8f9fa;
  min-height: 0; /* 💡 关键 */
}

.exit-view h2 {
  text-align: center;
  margin-top: 100px;
  color: #999;
}

.tail {
  height: 40px;
  background-color: #fafafa;
  text-align: center;
  font-size: 14px;
  line-height: 40px;
  color: #aaa;
  border-top: 1px solid #eee;
  flex-shrink: 0;
}
</style>
