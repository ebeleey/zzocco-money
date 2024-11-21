<template>
  <div class="data-table">
    <!-- 정렬 버튼 -->
    <div class="sort-buttons">
      <button
        :class="{ active: sortKey === 'intr_rate2' }"
        @click="sortKey = 'intr_rate2'"
      >
        최고 우대금리로 정렬
      </button>
      <button
        :class="{ active: sortKey === 'intr_rate' }"
        @click="sortKey = 'intr_rate'"
      >
        기본금리로 정렬
      </button>
    </div>

    <!-- 데이터 테이블 -->
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
        <tr 
          v-for="(product, index) in paginatedProducts" 
          :key="product.id"
          @click="openDetailModal(product)"
          class="cursor-pointer"
        >
          <td>{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>
          <td>
            {{ activeTab === 'deposit' ? product.deposit_id__kor_co_nm : product.saving_id__kor_co_nm }}
          </td>
          <td>
            {{ activeTab === 'deposit' ? product.deposit_id__fin_prdt_nm : product.saving_id__fin_prdt_nm }}
          </td>
          <td>{{ product.intr_rate }}%</td>
          <td>{{ product.intr_rate2 }}%</td>
          <td>
            {{
              activeTab === 'deposit'
                ? joinDenyMapping[product.deposit_id__join_deny]
                : joinDenyMapping[product.saving_id__join_deny]
            }}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 상세 정보 모달 -->
    <div 
      v-if="selectedProduct" 
      class="modal-overlay"
      @click.self="closeDetailModal"
    >
      <div class="modal-content">
        <button class="close-btn" @click="closeDetailModal">×</button>
        <h2>{{ activeTab === 'deposit' ? selectedProduct.deposit_id__fin_prdt_nm : selectedProduct.saving_id__fin_prdt_nm }}</h2>
        
        <div class="modal-details">
          <div class="detail-row">
            <span class="detail-label">금융회사</span>
            <span class="detail-value">
              {{ activeTab === 'deposit' ? selectedProduct.deposit_id__kor_co_nm : selectedProduct.saving_id__kor_co_nm }}
            </span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">기본금리</span>
            <span class="detail-value">{{ selectedProduct.intr_rate }}%</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">최고 우대금리</span>
            <span class="detail-value">{{ selectedProduct.intr_rate2 }}%</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">가입 대상</span>
            <span class="detail-value">
              {{ activeTab === 'deposit' 
                ? joinDenyMapping[selectedProduct.deposit_id__join_deny] 
                : joinDenyMapping[selectedProduct.saving_id__join_deny] 
              }}
            </span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">저축 기간</span>
            <span class="detail-value">{{ selectedProduct.save_trm }}개월</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">가입 방법</span>
            <span class="detail-value">
              {{ activeTab === 'deposit' 
                ? selectedProduct.deposit_id__join_way 
                : selectedProduct.saving_id__join_way 
              }}
            </span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">우대 조건</span>
            <span class="detail-value">
              {{ activeTab === 'deposit' 
                ? selectedProduct.deposit_id__spcl_cnd 
                : selectedProduct.saving_id__spcl_cnd 
              }}
            </span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">금리 유형</span>
            <span class="detail-value">{{ selectedProduct.intr_rate_type_nm }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button
        v-for="page in totalPages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="currentPage = page"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>


<script setup>
import { computed, ref } from "vue";

// Props 정의
const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
  products: {
    type: Array,
    required: true,
  },
  activeTab: {
    type: String,
    required: true,
  }
});


const selectedProduct = ref(null);

// 함수를 ref 또는 computed로 정의
const openDetailModal = (product) => {
  selectedProduct.value = product;
};

const closeDetailModal = () => {
  selectedProduct.value = null;
};


// 페이지네이션
const itemsPerPage = 20; // 한 페이지당 항목 수
const currentPage = ref(1); // 현재 페이지

// 정렬 기준 (초기값: 최고 우대금리)
const sortKey = ref("intr_rate2");

const joinDenyMapping = {
  1: "제한없음",
  2: "서민전용",
  3: "일부제한",
};

const filteredProducts = computed(() => {
  return props.products.filter((product) => {
    const matchesPeriod =
      props.filters.savingsPeriod.length === 0 ||
      props.filters.savingsPeriod.includes(product.save_trm);
    const matchesCalculation =
      product.intr_rate_type_nm === props.filters.interestCalculation ||
      props.filters.interestCalculation === "전체";
    const matchesEligibility =
      props.filters.eligibility.length === 0 ||
      props.filters.eligibility.includes(
        props.activeTab.value === "deposit"
          ? product.deposit_id__join_deny
          : product.saving_id__join_deny
      );
    const matchesMethod =
      props.filters.applicationMethods.length === 0 ||
      props.filters.applicationMethods.includes(
        props.activeTab.value === "deposit"
          ? product.deposit_id__join_way
          : product.saving_id__join_way
      );
    // const matchesCondition =
    //   props.filters.benefitConditions.length === 0 ||
    //   props.filters.benefitConditions.includes(
    //     activeTab.value === "deposit"
    //       ? product.deposit_id__spcl_cnd
    //       : product.saving_id__spcl_cnd
    //   );
    
    return (
      matchesPeriod &&
      matchesCalculation &&
      matchesEligibility &&
      matchesMethod
    );
  });
});



const sortedProducts = computed(() => {
  return [...filteredProducts.value].sort((a, b) => b[sortKey.value] - a[sortKey.value]);
});

const totalPages = computed(() => {
  return Math.ceil(sortedProducts.value.length / itemsPerPage);
});

// 현재 페이지 데이터 계산
const paginatedProducts = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return sortedProducts.value.slice(startIndex, endIndex);
});


defineExpose({
  openDetailModal,
  closeDetailModal
});

</script>

<style scoped>
/* 새로 추가된 모달 스타일 */
.cursor-pointer {
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}

.modal-details {
  margin-top: 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}
.detail-label {
  font-weight: bold;
  color: #3f2411;
  width: 130px; /* 원하는 너비로 조정 */
  flex-shrink: 0; /* 레이블 크기 유지 */
}

.detail-row {
  display: flex;
  align-items: center; /* 세로 정렬 */
  justify-content: space-between;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.detail-value {
  color: #6d4c41;
  flex-grow: 1; /* 남은 공간 차지 */
  text-align: right; /* 값을 오른쪽 정렬 */
}
.sort-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: flex-end;
}


.sort-buttons button {
  background-color: #3f2411;

  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-buttons button.active {
  background-color: #6d4c41;
  color: white;
  font-weight: bold;
}

.sort-buttons button:hover {
  background-color: #6d4c41;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 12px;
  margin: 0 5px;
  /* border: 1px solid #ccc; */
  background-color: white;
  color: black;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button.active {
  background-color: #3f2411;
  color: white;
  font-weight: bold;
  border: 1px solid #3f2411;
}

.pagination button:hover {
  background-color: #6d4c41;
  color: white;
}

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
