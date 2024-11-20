<template>
  <div class="sidebar">
    <!-- 단일 선택: 저축 예정 기간 -->
    <div class="filter-group">
      <h3>저축 예정 기간</h3>
      <select v-model="selectedSavingsPeriod" @change="updateFilters">
        <option v-for="period in savingsPeriod" :key="period" :value="period">
          {{ period }}
        </option>
      </select>
    </div>

    <!-- 단일 선택: 금융 권역 -->
    <div class="filter-group">
      <h3>금융 권역</h3>
      <select v-model="selectedFinancialSector" @change="updateFilters">
        <option v-for="sector in financialSector" :key="sector" :value="sector">
          {{ sector }}
        </option>
      </select>
    </div>

    <!-- 단일 선택: 이자 계산 방식 -->
    <div class="filter-group">
      <h3>이자 계산 방식</h3>
      <select v-model="selectedInterestCalculation" @change="updateFilters">
        <option v-for="calculation in interestCalculation" :key="calculation" :value="calculation">
          {{ calculation }}
        </option>
      </select>
    </div>

    <!-- 다중 선택: 지역 -->
    <!-- <div class="filter-group">
      <h3>지역</h3>
      <div v-for="area in region" :key="area">
        <input type="checkbox" :value="area" v-model="selectedRegions" @change="updateFilters" />
        <label>{{ area }}</label>
      </div>
    </div> -->
    <div class="filter-group">
      <h3>지역</h3>
      <div class="checkbox-container">
        <div v-for="area in region" :key="area" class="checkbox-item">
          <label>
            <input 
            type="checkbox"
            :value="area"
            v-model="selectedRegions"
            @change="updateFilters"
          />
            {{ area }}
          </label>
        </div>
      </div>
    </div>

    <!-- 다중 선택: 가입 대상 -->
    <div class="filter-group">
      <h3>가입 대상</h3>
      <div v-for="target in eligibility" :key="target">
        <label>
          <input type="checkbox" :value="target" v-model="selectedEligibility" @change="updateFilters" />
          {{ target }}
        </label>
      </div>
    </div>

    <!-- 다중 선택: 가입 방법 -->
    <div class="filter-group">
      <h3>가입 방법</h3>
      <div v-for="method in applicationMethod" :key="method">
        <label>
          <input type="checkbox" :value="method" v-model="selectedApplicationMethods" @change="updateFilters" />
          {{ method }}
        </label>
      </div>
    </div>

    <!-- 다중 선택: 우대 조건 -->
    <div class="filter-group">
      <h3>우대 조건</h3>
      <div v-for="condition in benefitConditions" :key="condition">
        <label>
          <input type="checkbox" :value="condition" v-model="selectedBenefitConditions" @change="updateFilters" />
          {{ condition }}
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// 단일 선택 옵션
const savingsPeriod = ["1개월", "3개월", "6개월", "12개월", "24개월", "36개월"];
const financialSector = ["전체", "은행", "저축은행", "신협조합"];
const interestCalculation = ["전체", "단리", "복리"];

// 다중 선택 옵션
const region = [
  "전체", "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
  "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"
];
const eligibility = ["제한없음", "서민전용", "일부제한"];
const applicationMethod = [
  "전체", "영업점", "인터넷", "스마트폰", "모집인", "전화(텔레뱅킹)", "기타"
];
const benefitConditions = [
  "비대면 가입", "재예치", "주거래(급여, 연금 이체 등)", "첫거래", "연령", "타상품가입·실적"
];

// 선택 상태
const selectedSavingsPeriod = ref(savingsPeriod[0]); // 기본값: 첫 번째 항목
const selectedFinancialSector = ref(financialSector[0]);
const selectedInterestCalculation = ref(interestCalculation[0]);

const selectedRegions = ref([]); // 다중 선택
const selectedEligibility = ref([]);
const selectedApplicationMethods = ref([]);
const selectedBenefitConditions = ref([]);

// 부모 컴포넌트로 이벤트 전달
const emit = defineEmits(["update-filters"]); // 이벤트 정의

// 부모 컴포넌트로 필터 업데이트 전달
const updateFilters = () => {
  const filters = {
    savingsPeriod: selectedSavingsPeriod.value,
    financialSector: selectedFinancialSector.value,
    interestCalculation: selectedInterestCalculation.value,
    regions: selectedRegions.value,
    eligibility: selectedEligibility.value,
    applicationMethods: selectedApplicationMethods.value,
    benefitConditions: selectedBenefitConditions.value,
  };
  // 이벤트로 부모 컴포넌트에 전달
  emit("update-filters", filters);
};
</script>

<style scoped>

.checkbox-container {
  display: grid; /* Grid 레이아웃 사용 */
  grid-template-columns: repeat(3, 1fr); /* 한 줄에 3개의 열로 배치 */

}

.sidebar {
  width: 230px;
  padding: 20px;
  background-color: rgba(228, 217, 211, 0.829);
  border-radius: 1cap;
}

.filter-group {
  margin-bottom: 20px;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

h3 {
  font-weight: bolder;
  font-size: 1rem;
  margin-bottom: 10px;
}

input[type="checkbox"] {
  margin-right: 10px;
}
</style>
