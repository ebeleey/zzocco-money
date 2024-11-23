<template>
  <div>
    <h1 class="page-title">FBTI</h1>
    <h2>금융 성향 테스트</h2>
    <h3>Finance-Type Test</h3>
    <div class="question-page">
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
        <div class="progress-status">
          <p>{{ currentIndex + 1 }} / {{ questions.length }}</p>
        </div>
      </div>

      <div v-if="currentIndex < questions.length" class="question-content">
        <div class="questions">
          <p class="question-number">Q{{ currentIndex + 1 }}</p>
          <p class="question-text">{{ questions[currentIndex].question }}</p>
        </div>
        <div class="answers">
          <button
            v-for="(answer, index) in questions[currentIndex].answers"
            :key="index"
            @click="selectAnswer(answer)"
          >
            {{ answer.text }}
          </button>
        </div>
      </div>

      <div v-else class="completion-message">
        <h3>테스트가 완료되었습니다!</h3>
        <p>결과를 확인하려면 다음 단계를 진행하세요.</p>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, computed  } from "vue";
import { useRouter } from "vue-router";

const router = useRouter()

const questions = [
  {
    question: "갑자기 받은 성과급이나 보너스, 또는 용돈으로 통장이 꽉 찼을 때, 가장 먼저 떠오르는 생각은?",
    answers: [
      { type: "소비형", text: "아싸! 일단 맛있는 것부터 먹자.", point: 1 },
      { type: "투자형", text: "소중한 기회! 새로운 투자처를 찾아보자.", point: 1 },
      { type: "안정형", text: "차를 바꿔야겠다, 예전에 마음에 드는 모델이 있었는데.", point: 1 },
      { type: "절약형", text: "이 돈은 일단 저축해야겠다.", point: 1 },
    ],
  },
  {
    question: "급하게 돈이 필요해져서 통장을 확인했을 때, 잔고가 부족하다면?",
    answers: [
      { type: "투자형", text: "은행에서 대출을 받아 투자금을 유지한다.", point: 1 },
      { type: "안정형", text: "큰 결정을 내리기 전에 더 많은 고민을 해본다.", point: 1 },
      { type: "소비형", text: "부모님이나 친구에게 빌릴 수 있을지 알아본다.", point: 1 },
      { type: "절약형", text: "조금 아끼면서 생활비를 조절해본다.", point: 1 },
    ],
  },
  {
    question: "친한 친구가 “이 투자, 괜찮을 거야”라고 추천하는 큰 투자가 있을 때, 당신이라면?",
    answers: [
      { type: "투자형", text: "친구의 말을 믿고 무조건 투자해본다.", point: 1 },
      { type: "안정형", text: "투자에 대해 더 알아보고, 전문가의 의견을 듣는다.", point: 1 },
      { type: "소비형", text: "재미 삼아 소액만 투자해본다.", point: 1 },
      { type: "절약형", text: "위험하다고 생각해서 아예 투자하지 않는다.", point: 1 },
    ],
  },
  {
    question: "온라인 쇼핑몰에서 마음에 쏙 드는 상품을 발견했을 때, 당신이라면?",
    answers: [
      { type: "소비형", text: "“이건 꼭 필요해!”라며 즉시 구매한다.", point: 1 },
      { type: "투자형", text: "조금 더 알아보고 더 좋은 상품이 있는지 찾아보고 구매한다.", point: 1 },
      { type: "안정형", text: "신중히 고민한 후, 그래도 괜찮다고 생각하면 구매한다.", point: 1 },
      { type: "절약형", text: "나에게 필요 없다고 생각하고 바로 페이지를 닫는다.", point: 1 },
    ],
  },
  {
    question: "매달 일정 금액을 저축하거나 투자하는 것에 대해 어떻게 생각하시나요?",
    answers: [
      { type: "절약형", text: "절대로 해야 한다, 꾸준히 저축하는 것이 가장 중요하다.", point: 3 },
      { type: "투자형", text: "내가 잘 할 수 있을지 모르겠지만, 투자도 한번 해볼까?", point: 3 },
      { type: "안정형", text: "적당히 저축하면서 여유가 되면 소액 투자도 해본다.", point: 3 },
      { type: "소비형", text: "나는 저축보다는 소비를 더 선호한다.", point: 3 },
    ],
  },
  {
    question: "현재 사용하는 휴대폰의 배터리가 자주 방전됩니다. 어떤 선택을 하시겠습니까?",
    answers: [
      { type: "소비형", text: "최신 스마트폰으로 바꿔서 배터리 문제를 한 번에 해결한다.", point: 1 },
      { type: "투자형", text: "성능과 가성비를 모두 고려해 새 휴대폰을 구매한다.", point: 1 },
      { type: "안정형", text: "배터리만 교체하거나 보조 배터리를 활용해 비용을 아낀다.", point: 1 },
      { type: "절약형", text: "당분간 불편하더라도 지금 상황을 참고 견딘다.", point: 1 },
    ],
  },
  {
    question: "후배가 점심 약속을 먼저 잡고 식사 비용을 계산하려고 합니다. 당신이라면 어떻게 할까요?",
    answers: [
      { type: "소비형", text: '"내가 살게"라며 선배로서 계산한다.', point: 1 },
      { type: "안정형", text: '"다음에는 내가 살게"라며 후배가 계산하도록 둔다.', point: 1 },
      { type: "안정형", text: "식사 후 커피를 내가 사며 균형을 맞춘다.", point: 1 },
      { type: "절약형", text: "서로 더치페이하자고 제안한다.", point: 1 },
    ],
  },
  {
    question: "동료들이 단체로 복권을 사자고 제안했습니다. 당신이라면?",
    answers: [
      { type: "소비형", text: "재미 삼아 참여한다.", point: 1 },
      { type: "투자형", text: "소액이라면 괜찮지만, 큰 돈은 거절한다.", point: 1 },
      { type: "안정형", text: "관심은 없지만 분위기를 위해 동의한다.", point: 1 },
      { type: "절약형", text: "돈을 아끼기 위해 아예 참여하지 않는다.", point: 1 },
    ],
  },
];

const currentIndex = ref(0)

const saverCount = ref(0)
const investorCount = ref(0)
const spenderCount = ref(0)
const plannerCount = ref(0)

// 답변 선택 시 동작
const selectAnswer = (answer) => {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value++;
    console.log(answer)
    if (answer.type === "절약형") {
      saverCount.value += answer.point
    } else if (answer.type === "투자형") {
      investorCount.value += answer.point
    } else if (answer.type === "소비형") {
      spenderCount.value += answer.point
    } else if (answer.type === "안정형") {
      plannerCount.value += answer.point
    }

  } else {
    const resultType = calculateResult();
    console.log(resultType)
    router.push({ name: "test-result", query: { result: resultType } });

  }
};

const priorityOrder = ["saver", "investor", "spender", "planner"];

const calculateResult = () => {
  const results = [
    { type: "saver", points: saverCount.value },
    { type: "investor", points: investorCount.value },
    { type: "spender", points: spenderCount.value },
    { type: "planner", points: plannerCount.value },
  ];

  // 포인트 내림차순으로 정렬
  // 동점 시 우선순위 적용
  results.sort((a, b) => {
    if (b.points === a.points) {
      // 동점일 때 우선순위에 따라 비교
      return priorityOrder.indexOf(a.type) - priorityOrder.indexOf(b.type);
    }
    return b.points - a.points; 
  });

  return results[0].type; 
};


const progressPercentage = computed(() => {
  return ((currentIndex.value + 1) / questions.length) * 100;
});



</script>

<style scoped>

.progress-bar-container {
  width: 50%;
  height: 15px;
  background-color: #e0e0e0;
  border-radius: 10px;
  margin: 20px auto 40px;
}

.progress-bar {
  height: 100%;
  background-color: #3f2411;
  width: 0%;
  transition: width 0.3s ease;
  border-radius: 10px;
}

.progress-status {
  text-align: right;
  color: gray;
  margin-right: 5px;
}

.question-number {
  font-size: 40px;
  font-family: 'HSJiptokki-Round';
  width: 80px;
  color: #3f2411;
}

.questions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.question-text {
  width: 500px;
  text-align: left;
}

.answers {
  display: flex; /* Flexbox로 설정 */
  flex-direction: column; /* 세로로 배열 */
  align-items: center; /* 중앙 정렬 */
  gap: 10px; /* 버튼 간 간격 */
}

.question-page {
  text-align: center;
}

.answers button {
  margin: 10px;
  padding: 10px 20px;
  width: 45%;
  height: 60px;
  background-color: #c4b4aa;
  color: #1f1816;
  font-weight: bold;
  cursor: pointer;
}

.answers button:hover {
  background-color: #3f2411;
  color: white;
}


.page-title {
  font-size: 70px;
  text-align: center;
  margin: 70px 0 0 0; 
  font-weight: bold;
}

h2, h3 {
  margin:0px;
  font-family: 'HSJiptokki-Black';
  color: #3f2411;
  text-align: center;
}

h3 {
  font-family: 'Pretendard-Regular';
  font-weight: bold;
  font-size: 14px;
}

</style>