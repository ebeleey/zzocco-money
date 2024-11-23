<template>
  <div class="sidebar">
    <!-- 정렬 버튼 -->
    <div class="sort-buttons">
      <form class="search-bar" @submit.prevent="updateFilters" role="search">
        <div class="input-group">
          <input 
            v-model="searchQuery" 
            class="form-control me-2" 
            type="search" 
            placeholder="검색어를 입력하세요" 
            aria-label="Search"
          />
          <button class="btn btn-outline-success search-button" type="submit">검색</button>
        </div>
      </form>
    </div>
    <!-- 단일 선택: 저축 예정 기간 -->
    <div class="filter-group">
      <h3>저축 예정 기간</h3>
      <div class="button-group">
        <button
          v-for="period in savingsPeriod"
          :key="period"
          :class="{ active: selectedSavingsPeriod.includes(period) }"
          @click="togglePeriod(period)"
        >
          {{ period }}개월
        </button>
      </div>
    </div>
    <hr>
    <!-- 단일 선택: 금융 권역 -->
    <!-- <div class="filter-group">
      <h3>금융 권역</h3>
      <select v-model="selectedFinancialSector" @change="updateFilters">
        <option v-for="sector in financialSector" :key="sector" :value="sector">
          {{ sector }}
        </option>
      </select>
    </div>
    <hr> -->

    <div class="filter-group">
      <h3>은행 선택</h3>
      <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle full-width" type="button" data-bs-toggle="dropdown" aria-expanded="false">
          {{ selectedBank || '은행을 선택하세요' }}
        </button>
        <ul class="dropdown-menu">
          <li class="dropdown-item" v-for="bank in banks" :key="bank" @click="selectBank(bank)">
            {{ bank }}
          </li>
        </ul>
      </div>
    </div>
    <!-- <div class="filter-group">
      <h3>은행</h3>
      <div v-for="bank in banks" :key="bank" class="checkbox-item">
        <label>
          <input 
          type="checkbox"
          :value="bank"
          v-model="selectedBanks"
          @change="updateFilters"
        />
          {{ bank }}
        </label>
      </div>
    </div> -->
    <hr>
    

    <!-- 단일 선택: 이자 계산 방식 -->
    <div class="filter-group">
      <h3>이자 계산 방식</h3>
      <div class="button-group">
        <button
          v-for="calculation in interestCalculation"
          :key="calculation"
          :class="{ active: selectedInterestCalculation === calculation }"
          @click="selectInterestCalculation(calculation)"
        >
          {{ calculation }}
        </button>
      </div>
    </div>

    <hr>

    <!-- 다중 선택: 가입 대상 -->
    <div class="filter-group">
      <h3>가입 대상</h3>
      <div v-for="target in eligibility" :key="target">
        <label>
          <input type="checkbox" :value="eligibilityMapping[target]" v-model="selectedEligibility" @change="updateFilters" />
          {{ target }}
        </label>
      </div>
    </div>
    
    <hr>
    
    <!-- 다중 선택: 가입 방법 -->
    <!-- <div class="filter-group">
      <h3>가입 방법</h3>
      <div v-for="method in applicationMethod" :key="method">
        <label>
          <input type="checkbox" :value="method" v-model="selectedApplicationMethods" @change="updateFilters" />
          {{ method }}
        </label>
      </div>
    </div> -->

    <div class="filter-group">
      <h3>가입 방법</h3>
      <!-- "전체" 체크박스 -->
      <label>
        <input 
          type="checkbox" 
          value="전체" 
          :checked="isAllSelected" 
          @change="toggleAllMethods" 
        />
        전체
      </label>
      <!-- 개별 체크박스 -->
      <div v-for="method in applicationMethod" :key="method">
        <label>
          <input 
            type="checkbox" 
            :value="method" 
            v-model="selectedApplicationMethods" 
            @change="updateSelectedMethods" 
          />
          {{ method }}
        </label>
      </div>
    </div>

    <!-- 다중 선택: 우대 조건 -->
    <!-- <div class="filter-group">
      <h3>우대 조건</h3>
      <div v-for="condition in benefitConditions" :key="condition">
        <label>
          <input type="checkbox" :value="condition" v-model="selectedBenefitConditions" @change="updateFilters" />
          {{ condition }}
        </label>
      </div>
    </div> -->

  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";

// 단일 선택 옵션
const props = defineProps({
  banks: Array
})
// 검색어 관련 변수 분리
const searchQuery = ref(''); // 실제 검색에 사용될 검색어

const savingsPeriod = [1, 3, 6, 12, 24, 36]
// const financialSector = ["전체", "은행", "저축은행", "신협조합"];
const interestCalculation = ["전체", "단리", "복리"];
const eligibility = ["제한없음", "서민전용", "일부제한"];
const applicationMethod = [
  "영업점", "인터넷", "스마트폰", "모집인", "전화(텔레뱅킹)", "기타"
];
// const benefitConditions = [
//   "비대면 가입", "재예치", "주거래(급여, 연금 이체 등)", "첫거래", "연령", "타상품가입·실적"
// ];

const selectedSavingsPeriod = ref([]);
const selectedInterestCalculation = ref(interestCalculation[0]);
const selectedEligibility = ref([]);
const selectedApplicationMethods = ref([...applicationMethod]);

// 선택된 province, city, bank 상태
const selectedProvince = ref(null)
const selectedCity = ref(null)
const selectedBank = ref(null)

const showProvinceDropdown = ref(false);
const showCityDropdown = ref(false);
const showBankDropdown = ref(false);

watch(selectedBank, (newBank) => {
	updateFilters()
	// selectedBank.value = null;
});

const selectBank = (bank) => {
	selectedBank.value = bank;
	showBankDropdown.value = false;
};

const banks = computed(() => props.banks)

// 부모 컴포넌트로 이벤트 전달
const emit = defineEmits(["update-filters"]); // 이벤트 정의

const eligibilityMapping = {
  "제한없음": 1,
  "서민전용": 2,
  "일부제한": 3,
};

// 기간 선택/해제 함수
const togglePeriod = (period) => {
  if (selectedSavingsPeriod.value.includes(period)) {
    // 이미 선택된 경우 -> 해제
    selectedSavingsPeriod.value = selectedSavingsPeriod.value.filter((p) => p !== period);
  } else {
    // 선택되지 않은 경우 -> 추가
    selectedSavingsPeriod.value.push(period);
  }
  updateFilters(); // 필터 업데이트
};

const selectInterestCalculation = function (calculation) {
  selectedInterestCalculation.value = calculation
  updateFilters()
}

// 선택된 가입 방법 (초기 상태: 전체 선택)


// "전체" 체크 여부를 계산하는 computed 속성
const isAllSelected = computed(() => {
  return selectedApplicationMethods.value.length === applicationMethod.length;
});

// "전체" 체크박스 상태 변경
const toggleAllMethods = () => {
  if (isAllSelected.value) {
    // 모든 체크박스 해제
    selectedApplicationMethods.value = [];
  } else {
    // 모든 체크박스 선택
    selectedApplicationMethods.value = [...applicationMethod];
  }
  updateFilters();
};

const updateSelectedMethods = () => {
  // 모든 개별 체크박스가 선택되었으면 "전체"를 선택
  if (selectedApplicationMethods.value.length === applicationMethod.length) {
    selectedApplicationMethods.value = [...applicationMethod];
  }
  updateFilters();
};

// 부모 컴포넌트로 필터 업데이트 전달
const updateFilters = () => {
  const filters = {
    searchQuery: searchQuery.value,
    banks: selectedBank.value,
    savingsPeriod: selectedSavingsPeriod.value, 
    // financialSector: selectedFinancialSector.value,
    interestCalculation: selectedInterestCalculation.value,
    eligibility: selectedEligibility.value,
    applicationMethods: selectedApplicationMethods.value,
    // benefitConditions: selectedBenefitConditions.value,
  };
  // 이벤트로 부모 컴포넌트에 전달
  emit("update-filters", filters);
};

</script>

<style scoped>
.sort-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: flex-end;
}

.search-bar .input-group {
  display: flex;
  width: 100%;
}

.search-bar .form-control {
  flex-grow: 1; /* 검색창을 버튼보다 넓게 만들기 */
}

.search-button {
  background-color: #3f2411;
  border: 1px solid white; /* 초록색 테두리에서 흰색으로 변경 */
  color: white; /* 글씨도 흰색으로 변경 */
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  background-color: #6d4c41;
}

.button-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

button {
  margin: 2px;
  background-color: #3f2411;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button.active {
  background-color: #6d4c41;
  color: white;
  font-weight: bold;
}

button:hover {
  background-color: #6d4c41;
  color: white;
}

button:focus {
  background-color: #6d4c41;
  color: white;
}

.sidebar {
  accent-color: #3f2411;
}

.filter-group {
  padding: 20px;
  background-color: rgba(228, 217, 211, 0.829);
  border-radius: 1cap;
}

h3 {
  font-weight: bolder;
  font-size: 1rem;
  margin-bottom: 10px;
}

input[type="checkbox"] {
  margin-right: 5px;
}

.dropdown {
  width: 100%; /* 부모 컨테이너의 전체 너비를 채우도록 설정 */
}

.full-width {
  width: 100%;
}

.dropdown-menu {
  width: 100%; /* 드롭다운 메뉴를 부모 요소와 같은 너비로 설정 */
  max-height: 300px; /* 너무 길 경우 스크롤 표시 */
  overflow-y: auto;
}

.dropdown-item {
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}
</style>
