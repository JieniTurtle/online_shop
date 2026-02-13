import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import ProductOverview from '../pages/ProductOverview.vue'
import ProductDetail from '../pages/ProductDetail.vue' // Import the new component

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/product-overview',
    name: 'ProductOverview',
    component: ProductOverview
  },
  {
    path: '/product-detail/:productId/:language',
    name: 'ProductDetail',
    component: ProductDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router