<template>
  <div class="page-warpper">
  <div class = "login-container">
    <div class="back-icon" @click="goBack">
      <el-icon class="arrow-icon"><ArrowLeftBold /></el-icon>
    </div>
    <h2>管理员登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" type="password" placeholder="密码" />
      <button type="submit">登录</button>
    </form>
    <p v-if="error" class="error-msg">{{"[ "+ error +" ]"}}</p>
  </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';
import { ArrowLeftBold } from '@element-plus/icons-vue';
import { LoginUser } from '../stores/user';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

// 模拟前端处理逻辑，比如校验长度等
const validateForm = (): boolean => {
  if (!username.value || !password.value) {
    error.value = '用户名和密码不能为空';
    return false;
  }
  if (username.value.length < 3 || password.value.length < 6) {
    error.value = '用户名或密码格式不正确';
    return false;
  }
  return true;
};
const goBack = () => {
  router.push('/signup')
};
const handleLogin = async () => {
  error.value = '';

  // 前端先校验
  if (!validateForm()) return;

  try {
    const token = await LoginUser(username.value,password.value);
    console.log('token',token);
    // 登录成功后
    localStorage.setItem('token', token)
    router.push('/manage')
  } catch (e: any) {
    error.value = e.response?.data?.message || '登录失败';
  }
};
</script>

<style scoped>
.login-container{
  position: relative;
  width: 420px;
  height: 310px;
  margin: 0px auto;
  padding: 50px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  text-align: center;
  font-family: 'Helvetica Neue', sans-serif;
}

.fa {
  font-family: 'Font Awesome 5 Free' !important;
  font-style: normal !important;
  transform: none !important;
}

.return-link {
  position: absolute;
  top: 0;
  right: 0;
}

.back-icon {
  position: absolute;
  top: 17px;
  left: 15px;
}
.back-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

body {
  background: linear-gradient(135deg, #c3ecf7, #a0c4ff);
  margin: 0;
  font-family: 'Helvetica Neue', sans-serif;
}

input {
  display: block;
  width: 100%;
  margin: 12px 0;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  transition: border 0.2s;
}

input:focus {
  box-shadow: 0 0 0 1.2px #9393fa;
  outline: none;
}

.arrow-icon {
  font-size: 22px;
  color: #b9bdc4;
}

.arrow-icon:hover {
  font-size: 22px;
  color: #a5aebe;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #409eff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3d7ec3;
}

.error-msg {
  color: rgb(223, 9, 9);
  margin-top: 10px;
}

.login-container {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}



</style>