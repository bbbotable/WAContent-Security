<template>
  <div class="reco-container">
    <div class="title">
      <h1>人脸识别签到管理系统</h1>
      <div class="right-text">
        <router-link to="/login" class="mylink"><el-icon style="vertical-align: -3px;"><Avatar/></el-icon>管理员页面</router-link>
      </div>
    </div>

    <div class="camera-container">
      <div class="camera-view">
        <video ref="videoRef" autoplay playsinline class="mirror"></video>
        <button @click="takePhoto">📸 拍照签到</button>
        <canvas ref="canvasRef" style="display: none;"></canvas>
      </div>

      <div class="reco-choice">
        <div class="reco-item">
          <el-icon class="icon"><Clock /></el-icon>
          <div>
            <h2>当前时间</h2>
            <p class="info-text">{{ currentTime }}</p>
          </div>
        </div>

        <div class="reco-item">
          <el-icon class="icon"><Setting /></el-icon>
          <div>
            <h2>活体检测方案</h2>
            <select id="verifyMethod" v-model="selectedMethod">
              <option value="baidu">百度API</option>
              <option value="local">本地模型</option>
            </select>
          </div>
        </div>

        <div class="reco-item">
          <el-icon class="icon"><Connection /></el-icon>
          <div>
            <h2>签到状态</h2>
            <p class="info-text">检测结果：{{ state }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { UserSignUp } from '../stores/recognition'
import { Avatar, Clock, Setting, Connection } from '@element-plus/icons-vue'

const videoRef = ref(null)
const canvasRef = ref(null)
const photoDataUrl = ref('')
const selectedMethod = ref('baidu')
const state = ref('')
const currentTime = ref('')
let stream = null

function updateTime() {
  const now = new Date()
  const year = now.getFullYear()
  const month = (now.getMonth() + 1).toString().padStart(2, '0')
  const day = now.getDate().toString().padStart(2, '0')
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  const seconds = now.getSeconds().toString().padStart(2, '0')

  currentTime.value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

onMounted(async () => {
  updateTime()
  setInterval(updateTime, 1000)

  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
  } catch (err) {
    console.error('无法访问摄像头:', err)
  }
})

onBeforeUnmount(() => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
})

async function takePhoto() {
  const video = videoRef.value
  const canvas = canvasRef.value
  if (!video || !canvas) return

  const width = video.videoWidth
  const height = video.videoHeight

  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video, 0, 0, width, height)
  const base64Data = canvas.toDataURL('image/png')
  photoDataUrl.value = base64Data

  const blob = await fetch(base64Data).then(res => res.blob())
  const timeStr = currentTime.value
  let result = "";
  state.value = '识别中...'
  try{
    result = await UserSignUp(blob, selectedMethod.value, timeStr)
    state.value = result
  }catch(err){
    console.log(err)
    state.value = "识别失败请检查网络"
  }

}
</script>


<style scoped>
.mirror {
  transform: scaleX(-1);
}

.camera-container {
  display: flex;
}

.reco-container {
  margin: 0 auto;
  width: 820px;
  height: 500px;
  border: 1px solid #ccc;
  border-radius: 25px;
  background-color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.camera-view {
  margin: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reco-choice {
  margin: 30px 18px;
  display: flex;
  flex-direction: column;
  gap: 27px;
  font-family: 'Noto Sans SC', 'Microsoft Yahei', 微软雅黑, Arial, sans-serif;
  font-weight: 700;
}

.reco-item {
  display: flex;
  align-items: center;
  background: #f9f9f9;
  padding: 13.2px;
  width: 350px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.3s ease;
}

.reco-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.icon {
  font-size: 30px;
  margin-right: 14px;
  color: #3ed1bd;
  min-width: 32px;
  text-align: start;
}

.info-text {
  font-size: 17px;
  font-weight: 500;
  margin-top: 4px;
  color: #555;
}

.right-text {
  width: 30%;
  text-align: right;
}

.title {
  font-family: 'Noto Sans SC', 'Microsoft Yahei', 微软雅黑, Arial, sans-serif;
  font-weight: 900;
  width: 100%;
  padding: 20px 30px 10px;
  font-size: 22px;
  background: linear-gradient(135deg, #2195c6, #3ed1bd);
  border-top-left-radius: 25px;
  border-top-right-radius: 25px;
  display: flex;
}

h1 {
  font-family: 'Noto Sans SC', 'Microsoft Yahei', 微软雅黑, Arial, sans-serif;
  font-weight: 700;
  font-size: 42px;
  width: 70%;
  color: #fff;
}

h2 {
  font-family: 'Noto Sans SC', 'Microsoft Yahei', 微软雅黑, Arial, sans-serif;
  font-weight: 500;
  font-size: 18px;
}

.mylink {
  color: aliceblue;
}

.mylink:hover {
  color: #dae8db;
}

video {
  width: 100%;
  max-width: 350px;
  border: 2px solid #ccc;
  border-radius: 8px;
}

button {
  font-family: 'Noto Sans SC', 'Microsoft Yahei', 微软雅黑, Arial, sans-serif;
  font-weight: 700;
  width: 100%;
  margin-top: 10px;
  padding: 12px 12px;
  font-size: 22px;
  border: none;
  background: linear-gradient(135deg, #2195c6, #3ed1bd);
  color: white;
  border-radius: 9px;
  cursor: pointer;
  transition: background 0.3s ease;
}
.title,
h1,
h2,
.reco-choice,
button,
select,
.info-text,
.mylink {
  font-family: 'Noto Sans SC', 'Microsoft Yahei', 微软雅黑, Arial, sans-serif;
    font-weight: 700;
}
button:hover {
  background: linear-gradient(135deg, #2195c6, #3ed1bd, #2195c6, #3ed1bd);
  background-size: 200% 100%;
  animation: gradientFlow 3s linear infinite;
}

@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 200% 50%;
  }
}

select {
  margin-top: 8px;
  padding: 8px 12px;
  font-size: 16px;
  width: 230px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #fff;
  transition: border-color 0.2s;
}

select:focus {
  border-color: #3ed1bd;
  outline: none;
}
</style>
