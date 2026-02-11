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
        <li v-for="(item, index) in itemCodes" :key="index" class="item-code-item">
          {{ item }}
        </li>
      </ul>
    </div>
    <button @click="fetchItemCodes" :disabled="loading">Refresh Data</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductList',
  data() {
    return {
      itemCodes: [],
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
        this.itemCodes = response.data;
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
  padding: 10px;
  margin: 5px 0;
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  border-radius: 4px;
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