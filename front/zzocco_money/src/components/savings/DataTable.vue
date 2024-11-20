<template>
    <div class="data-table">
      <h2>금융 상품 목록</h2>
      <table>
        <thead>
          <tr>
            <th>순위</th>
            <th>금융회사</th>
            <th>상품명</th>
            <th>기본금리</th>
            <th>최고 우대금리</th>
            <th>가입 대상</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>{{ product.name }}</td>
            <td>{{ product.interestRate }}%</td>
            <td>{{ product.bank }}</td>
            <td>{{ product.region }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { computed } from "vue";
  
  const props = defineProps({
    filters: {
      type: Object,
      required: true,
    },
  });
  
  // 예시 데이터
  const products = [
    { id: 1, name: "상품 A", interestRate: 2.5, bank: "은행", region: "서울" },
    { id: 2, name: "상품 B", interestRate: 3.0, bank: "저축은행", region: "부산" },
    // ...더 많은 데이터
  ];
  
  // 필터링된 데이터 계산
  const filteredProducts = computed(() => {
    return products.filter((product) => {
      const matchesPeriod = product.period === props.filters.savingsPeriod;
      const matchesSector = product.bank === props.filters.financialSector || props.filters.financialSector === "전체";
      const matchesCalculation = product.calculation === props.filters.interestCalculation || props.filters.interestCalculation === "전체";
      const matchesRegion = props.filters.regions.length === 0 || props.filters.regions.includes(product.region);
      const matchesEligibility = props.filters.eligibility.length === 0 || props.filters.eligibility.includes(product.eligibility);
      const matchesMethod = props.filters.applicationMethods.length === 0 || props.filters.applicationMethods.includes(product.method);
      const matchesCondition = props.filters.benefitConditions.length === 0 || props.filters.benefitConditions.includes(product.condition);
  
      return matchesPeriod && matchesSector && matchesCalculation && matchesRegion && matchesEligibility && matchesMethod && matchesCondition;
    });
  });
  </script>
  
  <style scoped>
  .data-table {
    width: 100%;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  </style>
  