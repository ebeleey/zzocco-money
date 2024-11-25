<template>
  <div class="profile-page">
    <h1 class="page-title">마이페이지</h1>
    <nav>
      <ul class="nav justify-content-center">
        <li class="nav-item">
          <RouterLink 
            :to="{ name: 'userInfo' }" 
            class="nav-link"
          >
            회원 정보
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink 
            :to="{ name: 'userProduct' }" 
            class="nav-link"
          >
            내가 가입한 금융상품
          </RouterLink>
        </li>
      </ul>
    </nav>

    <hr>

    <RouterView />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/account';
import { RouterLink, RouterView } from 'vue-router';

const store = useAccountStore();
const userId = ref(store.user.id);
</script>

<style scoped>
.profile-page {
  width: 60%;
  justify-content: center;
}

.nav-link {
  color: black;
  font-size: 18px;
  cursor: pointer;
}

/* Vue Router가 활성화된 링크에 자동으로 추가하는 클래스 */
.router-link-active {
  font-weight: bold;
	text-decoration: underline;

}
hr {
  margin: 0 auto;
  height: 3px;
  background-color: #3f2411;
  margin-bottom: 30px;
}
</style>
