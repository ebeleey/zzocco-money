<template>
  <div class="data-table">
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
        <!-- 필터링 및 정렬된 상품 출력 -->
        <tr v-for="(product, index) in sortedProducts" :key="product.id">
          <td>{{ index + 1 }}</td>
          <td>{{ product.bank }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.basicRate }}%</td>
          <td>{{ product.maxRate }}%</td>
          <td>{{ product.eligibility }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from "vue";

// Props 정의
const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
});

// 더미 데이터 (실제 데이터는 API로 받아올 예정)
const products = [
  { id: 1, bank: "은행A", name: "상품1", basicRate: 1.5, maxRate: 2.5, period: "1개월", calculation: "단리", region: "서울", eligibility: "전체", method: "온라인", condition: "특정 조건" },
  { id: 2, bank: "은행B", name: "상품2", basicRate: 1.2, maxRate: 2.8, period: "3개월", calculation: "복리", region: "경기", eligibility: "청년", method: "영업점", condition: "가입조건 없음" },
  // 더 많은 데이터 추가 가능
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

// 정렬된 데이터 계산 (우대 금리 순으로 정렬)
const sortedProducts = computed(() => {
  return [...filteredProducts.value].sort((a, b) => b.maxRate - a.maxRate);
});
</script>

<style scoped>
.data-table {
  width: 100%;
}

table {
  border-collapse: collapse; /* 셀 테두리 겹치기 */
  border-radius: 10px; /* 테이블 외곽 반경 */
  overflow: hidden; /* 반경 내부의 내용 잘리도록 처리 */
  width: 100%; /* 테이블 너비 */
}

th {
  background-color: #3f2411;
  font-weight: bold;
  padding: 10px;
  text-align: center;
  color: white;
  
}

td {
  padding: 10px;
  text-align: center;

}

thead th:first-child {
  border-top-left-radius: 10px; /* 좌측 상단 반경 */
}

thead th:last-child {
  border-top-right-radius: 10px; /* 우측 상단 반경 */
}

tr:hover:not(:has(th)) {
  background-color: rgba(228, 217, 211, 0.829);
}
</style>
