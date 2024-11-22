<template>
  <div class="min-h-screen flex flex-col">
    <!-- 컨테이너 -->
    <main class="flex-1 flex items-center justify-center bg-gray-50">
      <div class="text-center">
        <h1 class="text-3xl font-bold mb-4">
          나도 몰랐던 내 금융 성향, <br />
          지금 확인해보세요!
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
    router.push('/recommend') // 로그인 상태라면 recommend 페이지로 이동
  }
}
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
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