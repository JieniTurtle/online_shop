<template>
  <div class="product-detailed-images">
    <h3>Product Detailed Images</h3>

    <!-- Error display -->
    <div v-if="error" class="error-message">Error: {{ error }}</div>

    <!-- Main image display -->
    <div class="main-image-container">
      <img
        v-if="selectedImage"
        :src="selectedImage.url"
        :alt="`Detailed ${selectedImage.order_number}`"
        class="main-image"
      />
      <div v-else class="no-image">No image selected</div>
    </div>

    <!-- Thumbnail list -->
    <div v-if="images.length || true" class="thumbnail-list">
      <!-- Existing images - only for viewing/selecting -->
      <div
        v-for="image in images"
        :key="image.image_id"
        :class="['thumbnail-item', { active: selectedImage?.image_id === image.image_id }]"
        @click="selectedImage = image"
      >
        <img :src="image.url" :alt="`Thumb ${image.order_number}`" />
        <button
          class="delete-btn"
          @click.stop="handleDelete(image.image_id)"
          :disabled="deleteLoading"
        >
          ×
        </button>
        <span class="order-badge">{{ image.order_number }}</span>
      </div>
      
      <!-- Add new image placeholder - only this supports upload -->
      <div
        class="thumbnail-item add-new"
        @click="handleAddNewClick"
      >
        <div class="add-icon">+</div>
        <span class="order-badge">Add</span>
      </div>
    </div>

    <!-- Hidden file input for adding new images -->
    <input
      type="file"
      ref="hiddenFileInput"
      accept="image/*"
      @change="handleFileChange"
      style="display: none;"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// Props
const props = defineProps({
  productId: {
    type: [String, Number],
    required: true
  }
})

// State
const images = ref([])
const selectedImage = ref(null)
const loading = ref(false)
const error = ref(null)
const uploadLoading = ref(false)
const deleteLoading = ref(false)
const orderNumber = ref('')
const hiddenFileInput = ref(null) // For click-to-upload functionality

// Fetch images
const fetchImages = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/product/get_detailed_images/${props.productId}`)
    if (!response.ok) {
      throw new Error('Failed to fetch images')
    }
    const data = await response.json()
    images.value = data
    // Select first image by default
    selectedImage.value = data.length ? data[0] : null
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Handle click on add new placeholder
const handleAddNewClick = () => {
  const nextOrderNumber = images.value.length + 1 // Next available order number
  // Use the next available order number or let the backend handle it
  hiddenFileInput.value.click()
}

// Handle file selection from hidden input
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Calculate the order number for the new image
  const nextOrderNumber = images.value.length + 1
  
  // Use the same upload logic but with the file from hidden input
  await handleUploadWithFile(file, nextOrderNumber)

  // Clear the file input
  event.target.value = ''
}

// Upload handler with specific file
const handleUploadWithFile = async (file, orderNum) => {
  if (!file) {
    alert('Please select an image file.')
    return
  }
  if (!orderNum) {
    alert('Order number is required.')
    return
  }

  const formData = new FormData()
  formData.append('image', file)

  uploadLoading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/product/upload_detailed_image/${props.productId}/${orderNum}`, {
      method: 'POST',
      body: formData,
    })
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Upload failed')
    }
    // Refresh images
    await fetchImages()
  } catch (err) {
    error.value = err.message
  } finally {
    uploadLoading.value = false
  }
}

// Delete handler
const handleDelete = async (imageId) => {
  if (!confirm('Are you sure you want to delete this image?')) return

  deleteLoading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/product/delete_detailed_image/${imageId}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || 'Delete failed')
    }
    // Refresh images
    await fetchImages()
  } catch (err) {
    error.value = err.message
  } finally {
    deleteLoading.value = false
  }
}

// Initial fetch
onMounted(() => {
  if (props.productId) fetchImages()
})

// Refetch when productId changes
watch(() => props.productId, (newId) => {
  if (newId) fetchImages()
})
</script>

<style scoped>
.product-detailed-images {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: sans-serif;
}
.error-message {
  color: red;
  margin: 10px 0;
}
.main-image-container {
  width: 100%;
  height: 400px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  background: #f9f9f9;
}
.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.no-image {
  color: #999;
}
.thumbnail-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.thumbnail-item {
  position: relative;
  width: 80px;
  height: 80px;
  border: 2px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
}
.thumbnail-item.active {
  border-color: #007bff;
}
.thumbnail-item.add-new {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border: 2px dashed #ccc;
}
.thumbnail-item.add-new:hover {
  background-color: #e0e0e0;
  border-color: #aaa;
}
.thumbnail-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.add-icon {
  font-size: 32px;
  color: #666;
  font-weight: bold;
}
.delete-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  background: rgba(255, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.delete-btn:hover {
  background: red;
}
.order-badge {
  position: absolute;
  bottom: 2px;
  left: 2px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 10px;
  padding: 2px 4px;
  border-radius: 2px;
}
</style>