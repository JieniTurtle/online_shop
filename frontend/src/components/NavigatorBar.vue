<template>
  <nav class="navbar">
    <div class="nav-container">
      <RouterLink to="/" class="nav-logo">{{ $t('appName') }}</RouterLink>
      <div class="nav-menu">
        <RouterLink to="/product-overview" class="nav-item">{{ $t('navigation.products') }}</RouterLink>
        <button @click="switchLanguage" class="lang-switcher">
          {{ currentLang === 'en' ? '中文' : 'English' }}
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'NavigatorBar',
  setup() {
    const { locale, t } = useI18n()
    const currentLang = ref(locale.value)

    const switchLanguage = () => {
      const newLang = currentLang.value === 'en' ? 'zh' : 'en'
      locale.value = newLang
      currentLang.value = newLang
      
      // Save the selected language preference
      localStorage.setItem('language', newLang)
    }

    // Initialize language based on saved preference or browser language
    onMounted(() => {
      const savedLang = localStorage.getItem('language')
      const browserLang = navigator.language.startsWith('zh') ? 'zh' : 'en'
      
      if (savedLang && ['en', 'zh'].includes(savedLang)) {
        locale.value = savedLang
        currentLang.value = savedLang
      } else {
        locale.value = browserLang
        currentLang.value = browserLang
      }
    })

    return {
      currentLang,
      switchLanguage,
      t
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.nav-logo {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-item {
  color: #ecf0f1;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.router-link-active {
  background-color: #3498db;
  color: white;
}

.lang-switcher {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.lang-switcher:hover {
  background-color: #2980b9;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-menu {
    width: 100%;
    justify-content: center;
  }
}
</style>