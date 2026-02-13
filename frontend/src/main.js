import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'

// Load locale messages
import enLocale from './locales/en.json'
import zhLocale from './locales/zh.json'

const i18n = createI18n({
  locale: 'en', // default locale
  fallbackLocale: 'en', // fallback locale
  messages: {
    en: enLocale,
    zh: zhLocale
  }
})

createApp(App).use(i18n).use(router).mount('#app')