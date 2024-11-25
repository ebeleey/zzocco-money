<template>
  <div>
    <nav class="navbar navbar-expand-md">
      <div class="container-fluid">
        <!-- 햄버거 버튼 -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarToggler"
          aria-controls="navbarToggler"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- 로고와 네비게이션 메뉴 -->
        <div class="collapse navbar-collapse" id="navbarToggler">
          <RouterLink :to="{ name: 'home' }">
            <img src="../../assets/logo_sprinkle.png" alt="logo" />
          </RouterLink>
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'savings' }"
                >금융 상품 비교</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'currency-converter' }"
                >환율 계산기</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'bank-locator' }"
                >근처 은행 찾기</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'community' }"
                >커뮤니티</RouterLink
              >
            </li>
            <li v-if="isLogin" class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'profile' }"
                >마이페이지</RouterLink
              >
            </li>
            <li v-if="!isLogin" class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'signup' }"
                >회원가입</RouterLink
              >
            </li>
            <li v-if="!isLogin" class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'login' }"
                >로그인</RouterLink
              >
            </li>
            <li v-if="isLogin" class="nav-item">
              <button @click="logout" class="nav-link">로그아웃</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router';
import { RouterLink, RouterView } from 'vue-router';

const store = useAccountStore()
const router = useRouter()

// const userId = ref(store.user?.id);
// 로그인 상태 즉각 적용
const isLogin = computed(() => store.isLogin)

// 로그아웃 함수
const logout = () => {
  store.logout()  // 로그아웃 처리
  // 로그아웃 후 홈으로 리디렉션
  router.push({ name: 'home' })
}


</script>

<style scoped>


/* Navbar */
.navbar {
  font-family: 'Pretendard-Regular';
  font-size: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #3f2411;
  border-color: #3f2411;
}

.nav-link {
  color: white; /* 링크 텍스트를 흰색으로 설정 */
  text-decoration: none; /* 밑줄 제거 */
}

img {
  height: 4rem;
  width: 8rem;
}
</style>


