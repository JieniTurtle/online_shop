<!-- ImageUploader.vue -->
<template>
  <div
    class="image-uploader"
    :class="{ 'is-loading': loading }"
    @click="triggerFileSelect"
  >
    <img v-if="currentImageUrl" :src="currentImageUrl" alt="preview" />
    <div v-else class="placeholder">点击上传图片</div>
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      style="display: none"
      @change="handleFileChange"
    />
    <div v-if="loading" class="loading-mask">上传中...</div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  // 初始图片 URL
  imageUrl: {
    type: String,
    default: ''
  },
  // 自定义上传函数，接收 File 对象，返回 Promise<string>（新图片 URL）
  uploadHandler: {
    type: Function,
    required: true
  },
  // 允许的文件类型
  accept: {
    type: String,
    default: 'image/*'
  }
})

const emit = defineEmits(['update:imageUrl', 'upload-success', 'upload-error'])

// 当前展示的图片 URL
const currentImageUrl = ref(props.imageUrl)
// 上传状态
const loading = ref(false)
const fileInput = ref(null)

// 监听外部传入的 imageUrl 变化并同步
watch(() => props.imageUrl, (newVal) => {
  currentImageUrl.value = newVal
})

// 触发文件选择
function triggerFileSelect() {
  if (loading.value) return
  fileInput.value.click()
}

// 文件选择处理
async function handleFileChange(e) {
  const file = e.target.files[0]
  if (!file) return

  loading.value = true
  try {
    const newUrl = await props.uploadHandler(file)
    currentImageUrl.value = newUrl
    // 同步更新父组件绑定的 imageUrl（配合 .sync 或 v-model）
    emit('update:imageUrl', newUrl)
    emit('upload-success', newUrl)
  } catch (error) {
    emit('upload-error', error)
    console.error('上传失败', error)
  } finally {
    loading.value = false
    // 清空 input，允许重新上传相同文件
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
.image-uploader {
  position: relative;
  width: 200px;
  height: 200px;
  border: 1px dashed #ccc;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.image-uploader img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.placeholder {
  color: #999;
}
.loading-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.is-loading {
  cursor: not-allowed;
}
</style>