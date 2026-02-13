<template>
  <div class="table-uploader">
    <div class="upload-section">
      <h3>{{ title }}</h3>
      <div class="upload-controls">
        <input 
          type="file" 
          ref="fileInput"
          @change="handleFileChange" 
          :accept="acceptedFileTypes"
        />
        <!-- <label class="upload-label">{{ selectLabel }}</label> -->
        <button 
          @click="triggerFileSelect"
          class="upload-button"
          :disabled="isUploading"
        >
          {{ isUploading ? uploadingText : buttonText }}
        </button>
      </div>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TableUploader',
  props: {
    title: {
      type: String,
      default: 'Upload Product Table'
    },
    selectLabel: {
      type: String,
      default: 'Select Excel File'
    },
    buttonText: {
      type: String,
      default: 'Upload Table'
    },
    uploadingText: {
      type: String,
      default: 'Uploading...'
    },
    acceptedFileTypes: {
      type: String,
      default: '.xls,.xlsx'
    },
    uploadEndpoint: {
      type: String,
      default: '/api/product/upload_product_table'
    },
    refreshCallback: {
      type: Function,
      default: null
    }
  },
  emits: ['upload-start', 'upload-success', 'upload-error'],
  data() {
    return {
      fileInput: null,
      isUploading: false,
      errorMessage: null,
      successMessage: null
    }
  },
  methods: {
    // 触发文件选择
    triggerFileSelect() {
      this.$refs.fileInput.click();
    },

    // 处理文件选择变化
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      await this.uploadFile(file);
      
      // 重置文件输入
      event.target.value = '';
    },

    // 上传文件
    async uploadFile(file) {
      this.isUploading = true;
      this.errorMessage = null;
      this.successMessage = null;

      // 发射开始上传事件
      this.$emit('upload-start', file);

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post(this.uploadEndpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.data.success) {
          this.successMessage = response.data.message || 'Successfully uploaded!';
          
          // 发射上传成功事件
          this.$emit('upload-success', response.data);
          
          // 如果提供了回调函数，则执行
          if (this.refreshCallback && typeof this.refreshCallback === 'function') {
            this.refreshCallback();
          }
        } else {
          this.errorMessage = response.data.error || 'Upload failed.';
          this.$emit('upload-error', response.data.error);
        }
      } catch (err) {
        console.error('Error uploading file:', err);
        this.errorMessage = `Error uploading: ${err.message}`;
        this.$emit('upload-error', err.message);
      } finally {
        this.isUploading = false;
      }
    },

    // 允许父组件手动触发上传（如果需要）
    async uploadWithFile(file) {
      await this.uploadFile(file);
    }
  }
}
</script>

<style scoped>
.table-uploader {
  width: 100%;
}

.upload-section {
  padding: 20px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background-color: #f8f9fa;
  margin-bottom: 20px;
}

.upload-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.upload-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.upload-label {
  cursor: pointer;
  padding: 8px 12px;
  background-color: #6c757d;
  color: white;
  border-radius: 4px;
}

.upload-button {
  padding: 8px 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.upload-button:hover:not(:disabled) {
  background-color: #218838;
}

.upload-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

input[type="file"] {
  display: none;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
  padding: 8px;
  background-color: #fadbd8;
  border-radius: 4px;
  font-size: 0.9em;
}

.success-message {
  color: #27ae60;
  margin-top: 10px;
  padding: 8px;
  background-color: #d5f4e6;
  border-radius: 4px;
  font-size: 0.9em;
}
</style>