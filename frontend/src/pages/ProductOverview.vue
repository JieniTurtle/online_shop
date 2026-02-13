<template>
  <div class="product-list">
    <h1>Product Item Codes</h1>
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

export default {
  name: 'ProductList',
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
      products: [], // Changed from itemCodes to products to store both id and code
      loading: false,
      error: null
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
        
        // Handle different response formats
        if (response.data && Array.isArray(response.data)) {
          this.products = response.data.filter(item => item.item_code && item.product_id);
        } else {
          this.error = 'Unexpected response format';
        }
      } catch (err) {
        console.error('Error fetching item codes:', err);
        this.error = `Failed to load item codes: ${err.message}`;
      } finally {
        this.loading = false;
      }
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

.detail-button {
  background-color: #17a2b8;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  margin-right: 10px;
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
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>