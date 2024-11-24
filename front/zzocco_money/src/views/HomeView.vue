<template>
  <div class="flex">
    <!-- 컨테이너 -->
    <main class="flex items-center justify-center">
      <div class="text-center">
        <h1 class="slogan">
          내 금융 성향은 <br />
          어떤 초콜릿일까?
        </h1>
        <button @click="handleClick" class="mt-4 px-6 py-3 bg-black text-white rounded hover:bg-gray-800">
          내 금융 성향 알아보러 가기
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/account';
import { computed } from 'vue';

const router = useRouter()
const store = useAccountStore()
const isLoggedIn = computed(() => store.isLogin)

const handleClick = () => {
  if (!isLoggedIn.value) {
    if (confirm('로그인 후 이용 가능합니다. \n로그인 하시겠습니까?')) {
      router.push('login/')
    }
  } else {
    router.push('/fbti') // 로그인 상태라면 recommend 페이지로 이동
  }
}
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
}

.slogan {
  font-size: 48px;
}
h1 {
  padding: 10rem;
  
}
#app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}
</style>