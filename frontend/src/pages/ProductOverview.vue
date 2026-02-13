<template>
  <div class="product-list">
    <h1>Product Item Codes</h1>
    
    <!-- 使用表格上传组件 -->
    <TableUploader
      title="Upload Product Table"
      :refresh-callback="fetchItemCodes"
      @upload-success="onUploadSuccess"
      @upload-error="onUploadError"
    />
    
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else class="products-container">
      <ul class="item-codes-list">
        <li 
          v-for="(item, index) in products" 
          :key="item.product_id" 
          class="item-code-item"
        >
          <div class="product-info">
            <span class="item-code-display">{{ item.item_code }}</span>
            
            <!-- Image Display and Upload Area -->
            <div 
              class="image-area"
              @click="triggerFileSelect(item.product_id)"
              :class="{ uploading: uploading[item.product_id] }"
            >
              <img 
                v-if="getImageUrl(item.product_id)" 
                :src="getImageUrl(item.product_id)" 
                alt="Product Image" 
                class="product-image"
              />
              <div 
                v-else 
                class="placeholder"
              >
                <div class="placeholder-text">Click to add image</div>
              </div>
              
              <div 
                v-if="uploading[item.product_id]" 
                class="upload-overlay"
              >
                <div class="spinner"></div>
                <p>Uploading...</p>
              </div>
            </div>
            
            <input 
              type="file" 
              :ref="`fileInput_${item.product_id}`"
              @change="handleFileUpload($event, item.product_id)"
              accept="image/*"
              style="display: none;"
            />
            
            <button 
              class="detail-button"
              @click="goToProductDetail(item.product_id)"
            >
              View Details
            </button>
          </div>
        </li>
      </ul>
    </div>
    <button @click="fetchItemCodes" :disabled="loading">Refresh Data</button>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
import TableUploader from '../components/TableUploader.vue'; // 引入组件

export default {
  name: 'ProductList',
  components: {
    TableUploader // 注册组件
  },
  setup() {
    const router = useRouter();
    
    const goToProductDetail = (productId) => {
      // Get the current language from the route or global state
      const currentLanguage = localStorage.getItem('language') || 'en';
      router.push(`/product-detail/${productId}/${currentLanguage}`);
    };

    return {
      goToProductDetail
    };
  },
  data() {
    return {
      products: [],
      loading: false,
      error: null,
      imageUrls: {}, // Store image URLs by product ID
      uploading: {} // Track upload status for each product
    }
  },
  mounted() {
    this.fetchItemCodes();
  },
  methods: {
    async fetchItemCodes() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('/api/product/get_all_item_codes');
        
        if (response.data && Array.isArray(response.data)) {
          this.products = response.data.filter(item => item.item_code && item.product_id);
          
          // Fetch image URLs for all products
          await this.fetchAllImageUrls();
        } else {
          this.error = 'Unexpected response format';
        }
      } catch (err) {
        console.error('Error fetching item codes:', err);
        this.error = `Failed to load item codes: ${err.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchAllImageUrls() {
      // Fetch image URL for each product
      for (const product of this.products) {
        try {
          const response = await axios.get(`/api/product/get_main_image_url/${product.product_id}`);
          console.log("response: ", response);
          
          // 处理可能的响应格式 - 字符串或对象
          let imageUrl = null;
          
          // 检查是否是对象格式 { image_url: "url" }
          if (response.data && typeof response.data === 'object' && response.data.image_url) {
            imageUrl = response.data.image_url;
          } 
          // 检查是否是纯字符串格式
          else if (typeof response.data === 'string' && response.data.startsWith('/')) {
            imageUrl = response.data;
          }
          
          if (imageUrl) {
            this.imageUrls[product.product_id] = imageUrl;
            console.log(`Set image URL for ${product.product_id}: ${imageUrl}`);
          } else {
            console.log(`No valid image URL found for product ${product.product_id}`);
            // 设置默认图片
            this.imageUrls[product.product_id] = '/static/images/default.png';
          }
        } catch (err) {
          console.error(`Error fetching image for product ${product.product_id}:`, err);
          // 设置默认图片
          this.imageUrls[product.product_id] = '/static/images/default.png';
        }
      }
    },
    
    getImageUrl(productId) {
      console.log("url", this.imageUrls);
      return this.imageUrls[productId];
    },
    
    triggerFileSelect(productId) {
      // 使用 $refs 来访问文件输入元素
      const fileInputRef = this.$refs[`fileInput_${productId}`];
      if (fileInputRef && fileInputRef.length > 0) {
        fileInputRef[0].click();
      }
    },
    
    async handleFileUpload(event, productId) {
      const file = event.target.files[0];
      if (!file) return;
      
      // 设置上传状态 - Vue 3 中直接赋值
      this.uploading[productId] = true;
      
      const formData = new FormData();
      formData.append('image', file);
      
      try {
        const response = await axios.post(`/api/product/upload_product_image/${productId}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        if (response.data.success) {
          // 上传成功后更新图片URL - Vue 3 中直接赋值
          this.imageUrls[productId] = response.data.imageUrl;
          console.log(`Image uploaded successfully for product ${productId}`);
        } else {
          console.error(`Upload failed for product ${productId}:`, response.data.error);
          alert(`Failed to upload image: ${response.data.error}`);
        }
      } catch (err) {
        console.error(`Error uploading image for product ${productId}:`, err);
        alert(`Error uploading image: ${err.message}`);
      } finally {
        // 重置上传状态
        this.uploading[productId] = false;
        
        // 重置文件输入
        event.target.value = '';
      }
    },
    
    // 表格上传成功的回调
    onUploadSuccess(data) {
      console.log('Table upload successful:', data);
      // 可以在这里添加额外的成功处理逻辑
    },
    
    // 表格上传失败的回调
    onUploadError(error) {
      console.error('Table upload failed:', error);
      // 可以在这里添加额外的错误处理逻辑
    }
  }
}
</script>

<style scoped>
.product-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.error {
  color: #e74c3c;
  text-align: center;
  padding: 10px;
  background-color: #fadbd8;
  border-radius: 4px;
}

.products-container {
  margin: 20px 0;
}

.item-codes-list {
  list-style-type: none;
  padding: 0;
}

.item-code-item {
  padding: 15px;
  margin: 5px 0;
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  border-radius: 4px;
  transition: background-color 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-code-item:hover {
  background-color: #e9ecef;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-grow: 1;
}

.item-code-display {
  font-weight: bold;
  color: #2c3e50;
  flex-grow: 1;
}

.image-area {
  width: 100px;
  height: 100px;
  border: 2px dashed #ccc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.image-area:hover {
  border-color: #007bff;
}

.image-area.uploading {
  opacity: 0.7;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.placeholder-text {
  color: #999;
  font-size: 0.8rem;
}

.upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 10;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
  margin-bottom: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.detail-button {
  background-color: #17a2b8;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  margin-left: 10px;
}

.detail-button:hover {
  background-color: #138496;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>