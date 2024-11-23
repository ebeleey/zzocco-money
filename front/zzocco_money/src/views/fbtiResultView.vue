<template>
  <div class="result-page">
    <div v-if="loading" class="loading-screen">

      <h2>당신의 금융 유형을 분석 중</h2>
      <br>
      <span class="loading-dots"></span>
      <span class="loading-dots"></span>
      <span class="loading-dots"></span>
    </div>
    <div v-else >
      <p style="font-size: 100px; margin: 0;">🍫</p>
      <h2 class="result-subtitle">{{ resultData[resultType].subtitle }}</h2>
      <h1 class="result-title">{{ resultData[resultType].title }}</h1>
      <div class="result-description">
        <p v-for="(desc, index) in resultData[resultType].description" :key="index">
          {{ desc }}
        </p>
      </div>
      <br>
      <button class="goRecommend">
        나에게 딱 맞는<br>예적금 상품 추천받으러 가기
      </button>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from "vue-router";

const route = useRoute();
const resultType = route.query.result

const loading = ref(true)

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
  }, 2000); // 1초
});
const resultData = {
  spender: {
    subtitle: "달콤하고 부드러운",
    title: "밀크초콜릿 타입",
    description: [
      "현재의 행복을 가장 중요하게 생각하는 당신!",
      "저축보다는 지금의 만족을 위해 소비하는 데 익숙한 편이군요.",
      "맛있는 음식을 먹거나 쇼핑을 하면서 삶의 작은 기쁨을 찾아가는 모습이 돋보입니다.",
      "　",
      "하지만 때로는 이렇게 즉각적인 만족을 추구하는 소비는",
      "장기적인 재정 목표를 방해할 수 있어요.",
      "현명한 소비를 위해 소비 기록을 정리하거나, 소액 자동 저축을 설정해보는 것은 어떨까요?",
      "또한, 캐시백이나 포인트 적립 혜택이 높은 신용카드를 같이 사용하면,",
      "소비 습관을 유지하면서도 조금씩 저축 효과를 낼 수 있습니다.",
      "　",
      "현재의 행복도 중요하지만, 미래를 위한 작은 준비도 시작해보세요.",
      "그러면 더 풍요로운 오늘과 내일을 만들어갈 수 있을 거예요!",
    ],
  },
  saver: {
    subtitle: "풍미 깊은",
    title: "다크초콜릿 타입",
    description: [
      "신중하고 계획적인 재정 관리가 돋보이는 당신!",
      "돈을 쓰기보다 저축을 우선시하며, 최대한의 실용성을 추구하는 편이군요. ",
      "단순하고 소박한 삶을 지향하는 모습이 절약형 타입의 가장 큰 장점입니다.",
      "　",
      "하지만 너무 저축에만 치우치다 보면, 삶의 작은 즐거움을 놓칠 수 있어요.",
      "때로는 자신에게 작은 보상을 선물하거나, 삶의 질을 높이는 투자를 해보는 것도 좋습니다.",
      "예를 들어, 건강을 위한 운동 기구를 구매하거나 취미를 위한 소액 투자를 시작해보세요.",
      "　",
      "지금의 절약 습관은 이미 훌륭하지만,",
      "삶의 균형을 조금 더 맞춘다면 더 큰 행복을 느낄 수 있을 거예요!",
    ],
  },
  investor: {
    subtitle: "새롭고 특별한",
    title: "수제초콜릿 타입",
    description: [
      "새로운 기회를 찾고, 자산을 늘리는 데 적극적인 당신!",
      "돈을 효율적으로 불릴 방법을 탐구하며,",
      "위험을 감수할 수 있는 대담함이 돋보이는 타입이군요.",
      "　",
      "하지만 투자에 집중하다 보면 자칫 위험 관리에 소홀할 수 있습니다.",
      "리스크를 최소화하기 위해 포트폴리오를 다변화하고,",
      "안정적인 장기 투자 상품을 함께 고려해보세요.",
      "　",
      "돈을 불리는 것도 중요하지만, 안정성을 조금 더 신경 쓰며 장기적인 목표를 세워보세요.",
    ],
  },
  planner: {
    subtitle: "균형 잡힌",
    title: "아몬드 초콜릿 타입",
    description: [
      "소비와 저축, 투자 간의 균형을 중요하게 여기는 당신!",
      "신중하게 재정을 계획하고 무리하지 않으면서도 장기적인 목표를 설정하는 모습이 인상적입니다.",
      "　",
      "하지만 안정적인 재정 관리를 유지하면서도,",
      "때로는 더 큰 기회를 잡을 수 있는 도전이 필요할 수 있습니다.",
      "예를 들어, 저금리 시대에는 인플레이션을 고려한 투자 상품을 소액으로 시도해보는 것도 좋습니다.",
      "　",
      "당신은 이미 훌륭한 재정 균형을 이루고 있지만,",
      "조금 더 도전적인 목표를 세워보는 것도 새로운 가능성을 열어줄 거예요!",
    ],
  },
}


</script>

<style scoped>
.loading-screen {
  padding: 200px 0;
}

.loading-dots::after {
  content: "";
  display: inline-block;
  margin-left: 10px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #3f2411;
  animation: loading-dots 1.5s infinite;
}

@keyframes loading-dots {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.result-page {
  text-align: center;
  margin-top: 50px;
  padding: 50px;
  background-color: #c4b4aa;
  width: 720px;
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.goRecommend {
  padding: 10px 15px;
  border-radius: 10px;
  background-color: #3f2411;;
}
.goRecommend:hover {
  /* background-color: rgb(92, 64, 45); */
  color: white;
  transform: scale(1.05);

}

h1, h2 {
  font-family: 'HSJiptokki-Round';
  color: #3f2411;
  margin: 0;
}

h1 {
  font-size: 60px;
  margin-bottom: 20px;
}
</style>