<template>
  <div class="savings-page">

    <h1 class="page-title">금융 상품 목록 비교</h1>

    <div class="savings-view">
      <Sidebar @update-filters="applyFilters" />
      <DataTable :filters="filters" />
    </div>

  </div>
</template>
  
<script setup>
import { ref } from "vue";
import Sidebar from "../components/savings/Sidebar.vue";
import DataTable from "../components/savings/DataTable.vue";

// 필터 상태 관리
const filters = ref({
  savingsPeriod: "1개월", // 기본값
  financialSector: "전체", // 기본값
  interestCalculation: "전체", // 기본값
  regions: [],
  eligibility: [],
  applicationMethods: [],
  benefitConditions: [],
});

// Sidebar에서 전달된 필터를 업데이트
const applyFilters = (updatedFilters) => {
  filters.value = updatedFilters;
};
</script>
  
<style scoped>

.page-title {
  text-align: center;
  margin-top: 70px; 
  margin-bottom: 50px; 
  font-weight: bold;
}

.savings-view {
  display: flex; /* Sidebar와 DataTable을 가로로 배치 */
}


/* DataTable 스타일 */
.data-table {
  flex: 1; /* 남은 공간 차지 */
  padding: 20px;
  overflow-y: auto; /* 내용이 많을 경우 스크롤 */
}
</style>