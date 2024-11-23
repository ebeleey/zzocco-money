<template>
  <div class="savings-page">

      <h1 class="page-title">금융 상품 목록 비교</h1>
      <!-- 탭 버튼 -->
      <div class="tabs">
        <button
          class="tab-button"
          :class="{ active: activeTab === 'deposit' }"
          @click="switchTab('deposit')"
        >
          예금
        </button>
        <button
          class="tab-button"
          :class="{ active: activeTab === 'saving' }"
          @click="switchTab('saving')"
        >
          적금
        </button>
      </div>


    <div class="savings-view">
      
      <Sidebar @update-filters="applyFilters" :banks="bankList" />
      <DataTable :filters="filters" :products="currentProducts" :active-tab="activeTab"/>
    </div>

  </div>
</template>
  
<script setup>

import { ref, computed, onMounted } from "vue";
import Sidebar from "../components/savings/Sidebar.vue";
import DataTable from "../components/savings/DataTable.vue";
import axios from 'axios'

const activeTab = ref("deposit"); // 기본값: 정기예금

// 탭 전환 함수
const switchTab = async (tab) => {
  activeTab.value = tab;
  await fetchData(); // 탭 전환 시 데이터 로드

};

const deposits = ref([])
const savings = ref([])
const bankList = ref([])

const initialFilters = {
  banks: [],
  savingsPeriod: [], // 모든 기간 허용
  interestCalculation: '전체',
  eligibility: [],
  applicationMethods: [],
}

// 필터 상태 관리
const filters = ref(initialFilters);

const currentProducts = computed(() => {
  return activeTab.value == "deposit" ? deposits.value : savings.value
})



// API 데이터 로드
const fetchData = async () => {
  try {
    if (activeTab.value === "deposit") {
      console.log("예금")
      // 정기예금 데이터 가져오기
      if (deposits.value.length === 0) { 
        const response = await axios.get("http://127.0.0.1:8000/savings/get-deposits/");
        deposits.value = response.data
        console.log("정기예금 데이터:", deposits.value);
      }

      bankList.value = [...new Set(deposits.value.map(item => item.deposit_id__kor_co_nm))]
      bankList.value.sort()
      // [...new Set(data.map(item => item.saving_id__kor_co_nm))]
      console.log(bankList.value)
    } else if (activeTab.value === "saving") {
      console.log("적금")
      // 적금 데이터 가져오기
      if (savings.value.length === 0) {
        const response = await axios.get("http://127.0.0.1:8000/savings/get-savings/");
        savings.value = response.data
        console.log("적금 데이터:", savings.value);
      }
      bankList.value = [...new Set(savings.value.map(item => item.saving_id__kor_co_nm))]
      bankList.value.sort()
      console.log(bankList.value)
    }
  } catch (error) {
    console.error("API 호출 중 오류 발생:", error);
  }
};


// Sidebar에서 필터 업데이트
const applyFilters = (updatedFilters) => {
  filters.value = updatedFilters;
};

onMounted(() => {
  fetchData()
})
</script>
  
<style scoped>
.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  background-color:#3f2411;
  border-radius: 1cap;
}

.tab-button {
  background-color: #3f2411;
  padding: 20px;
  width: 650px;
  cursor: pointer;
  font-size: 20px;
  /* color: rgba(255, 255, 255, 0.651); */
}

.tab-button.active {
  /* background-color: #3f2411;
  color: white; */
  background-color: #ffffff28;
  font-weight: bold;
  
}

.page-title {
  text-align: center;
  margin-top: 70px; 
  margin-bottom: 50px; 
  font-weight: bold;
}

.savings-view {
  display: flex; /* Sidebar와 DataTable을 가로로 배치 */
}



.tab-button.active {
  /* background-color: #3f2411;
  color: white; */
  background-color: #ffffff28;
  font-weight: bold;
  
}


.savings-view {
  display: flex; /* Sidebar와 DataTable을 가로로 배치 */
}

/* DataTable 스타일 */
.data-table {
  flex: 1; /* 남은 공간 차지 */
  padding-left: 20px;
  overflow-y: auto; /* 내용이 많을 경우 스크롤 */
}


</style>