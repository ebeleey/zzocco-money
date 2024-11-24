import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView.vue'
import LoginView from '../views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'
import CurrencyConverterView from '@/views/CurrencyConverterView.vue'
import CommunityView from '@/views/CommunityView.vue'
import RecommendView from '@/views/RecommendView.vue'
import BankLocatorView from '@/views/BankLocatorView.vue'
import SavingsView from '@/views/SavingsView.vue'
import DetailView from '@/views/DetailView.vue'
import PostArticleView from '@/views/PostArticleView.vue'
import fbtiResultView from '@/views/fbtiResultView.vue'
import fbtiTestView from '@/views/fbtiTestView.vue'
import EditView from '@/views/EditView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/savings',
      name: 'savings',
      component: SavingsView
    },
    {
      path: '/currency-converter',
      name: 'currency-converter',
      component: CurrencyConverterView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/articles/:id/edit',
      name: 'EditView',
      component: EditView
    },
    {
      path: '/articles/post/',
      name: 'PostArticleView',
      component: PostArticleView
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: RecommendView
    },
    {
      path: '/fbti',
      name: 'fbti-test',
      component: fbtiTestView,
    },
    {
      path: '/test_result',
      name: 'test-result',
      component: fbtiResultView,
    },
    {
      path: '/bank_locator',
      name: 'bank-locator',
      component: BankLocatorView
    },
  ],
})

export default router
