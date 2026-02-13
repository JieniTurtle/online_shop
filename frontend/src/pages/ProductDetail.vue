<template>
  <div class="product-detail">
    <div v-if="loading" class="loading">
      Loading product details...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="product" class="product-info">
      <h1>{{ $t('productDetail.title') }}</h1>
      <div class="detail-item">
        <strong>{{ $t('productDetail.itemCode') }}:</strong> {{ product.item_code }}
      </div>
      <!-- <div class="detail-item" v-if="product.category">
        <strong>{{ $t('productDetail.category') }}:</strong> {{ product.category }}
      </div> -->
      <div class="detail-item" v-if="product.blade_material">
        <strong>{{ $t('productDetail.bladeMaterial') }}:</strong> {{ product.blade_material }}
      </div>
      <div class="detail-item" v-if="product.fittings_material">
        <strong>{{ $t('productDetail.fittingsMaterial') }}:</strong> {{ product.fittings_material }}
      </div>
      <div class="detail-item" v-if="product.total_length">
        <strong>{{ $t('productDetail.totalLength') }}:</strong> {{ product.total_length }} cm
      </div>
      <div class="detail-item" v-if="product.blade_length">
        <strong>{{ $t('productDetail.bladeLength') }}:</strong> {{ product.blade_length }} cm
      </div>
      <div class="detail-item" v-if="product.tsuka_length">
        <strong>{{ $t('productDetail.tsukaLength') }}:</strong> {{ product.tsuka_length }} cm
      </div>
    </div>
    <button @click="goBack">{{ $t('productDetail.goBack') }}</button>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'ProductDetail',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const { locale } = useI18n(); // Get current locale from i18n
    const product = ref(null);
    const loading = ref(true);
    const error = ref(null);

    const goBack = () => {
      router.go(-1); // Go back to previous page
    };

    const fetchProductDetails = async (language) => {
      const { productId } = route.params;
      console.log("Fetching with language: ", language);
      
      try {
        const response = await axios.get(`/api/product/get_product_by_id/${productId}/${language}`);
        product.value = response.data;
      } catch (err) {
        console.error('Error fetching product details:', err);
        error.value = `Failed to load product details: ${err.message}`;
      } finally {
        loading.value = false;
      }
    };

    // Watch for language changes and reload product details
    watch(locale, (newLocale) => {
      console.log("Language changed to: ", newLocale);
      loading.value = true;
      error.value = null;
      fetchProductDetails(newLocale);
    });

    onMounted(() => {
      // Use the current application language instead of URL parameter
      const currentLanguage = locale.value;
      fetchProductDetails(currentLanguage);
    });

    return {
      product,
      loading,
      error,
      goBack
    };
  }
};
</script>

<style scoped>
.product-detail {
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

.product-info {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.detail-item {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}

button:hover {
  background-color: #5a6268;
}
</style>