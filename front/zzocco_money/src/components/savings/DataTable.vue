<template>
  <div class="data-table">
    <div v-if="isLoading" class="loading">
      로딩 중입니다...
    </div>

    <div v-else>

      <!-- 데이터 테이블 -->
      <table>
        <thead>
          <tr>
            <th class="col-rank">순위</th>
            <th class="col-company">금융회사</th>
            <th class="col-product">상품명</th>
            <th 
              class="col-rate"
              :class="{ active: sortKey === 'intr_rate' }"
              @click="toggleSort('intr_rate')"
            >
              기본금리
              <span v-if="sortKey === 'intr_rate'">
                {{ sortOrder === 'desc' ? '▼' : '▲' }}
              </span>
            </th>
            <th 
              class="col-rate2" 
              :class="{ active: sortKey === 'intr_rate2' }"
              @click="toggleSort('intr_rate2')"
            >
              최고 우대금리
              <span v-if="sortKey === 'intr_rate2'">
                {{ sortOrder === 'desc' ? '▼' : '▲' }}
              </span>
            </th>
            <th class="col-eligibility">가입 대상</th>
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
          
          <header>
            <h2>{{ activeTab === 'deposit' ? selectedProduct.deposit_id__fin_prdt_nm : selectedProduct.saving_id__fin_prdt_nm }}</h2>
          </header>
          
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
          <div v-if="isLoggedIn" class="modal-btn">
            <button v-if="!isAdded" @click="manageProduct('add')">가입하기</button>
            <button v-else @click="manageProduct('remove')">가입 취소하기</button>
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
  </div>
</template>


<script setup>
import { computed, ref, watch } from "vue";
import { useAccountStore } from "@/stores/account";
import axios from "axios";

const accountStore = useAccountStore()

// 로그인 여부
const isLoggedIn = computed(() => accountStore.isLogin)

// 상품 가입 여부
const isAdded = computed(() => {
  // console.log(accountStore.user)
  // accountStore.fetchUser()
  const productType = props.activeTab === 'deposit' ? 'deposits' : 'savings'
  const productId = selectedProduct.value.id

  // 사용자의 상품 목록이 있는지 확인
  // console.log(accountStore.user.product_list[productType])
  // if (!accountStore.user?.product_list?[productType]) {
  //   return false
  // }

  // 해당 타입의 상품 목록이 있는지 확인
  const userProducts = accountStore.user?.product_list[productType]
  // if (!userProducts) {
  //   return false
  // }
  console.log(typeof(productId))
  console.log(typeof(userProducts[0]))

  // 선택된 상품의 ID가 사용자의 상품 목록에 있는지 확인
  return userProducts.includes(productId)
})

const manageProduct = async (action) => {
  console.log(selectedProduct)
  const productType = props.activeTab === 'deposit' ? 'deposits' : 'savings';
  const productId = selectedProduct.value.id

  // console.log(productId)
  try {
    const response = await axios.post('http://127.0.0.1:8000/accounts/manage-product/', {
      action: action,
      product_type: productType,
      product_id: productId
    }, {
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    });
    accountStore.fetchUser()
  } catch (error) {
    console.error('Error adding product:', error);
    // 에러 처리 로직 (예: 사용자에게 에러 메시지 표시)
  }
}

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
// 로딩 상태 관리
const isLoading = ref(true); // 로딩 상태 추가
watch(
  () => [props.products, props.activeTab], // products와 activeTab 모두 관찰
  ([newProducts, newActiveTab]) => {
    isLoading.value = true; // 탭 이동 시 로딩 시작
    if (newProducts && newProducts.length > 0) {
      // 데이터가 존재하면 로딩 해제
      setTimeout(() => {
        isLoading.value = false; // 약간의 지연시간 후 로딩 해제 (시각적 효과)
      }, 500); // 0.5초 지연
    }
  },
  { immediate: true } // 초기 로딩 상태 설정
);


const selectedProduct = ref(null);

// 함수를 ref 또는 computed로 정의
const openDetailModal = (product) => {
  console.log(product)
  selectedProduct.value = product;
};

const closeDetailModal = () => {
  selectedProduct.value = null;
};


// 페이지네이션
const itemsPerPage = 20; // 한 페이지당 항목 수
const currentPage = ref(1); // 현재 페이지

// 정렬 기준 (초기값: 최고 우대금리)
// const sortKey = ref("intr_rate2");

const joinDenyMapping = {
  1: "제한없음",
  2: "서민전용",
  3: "일부제한",
};

const filteredProducts = computed(() => {
  currentPage.value = 1
  return props.products.filter((product) => {
    // 검색어 필터링
    const matchesSearch =
      props.filters.searchQuery.trim() === '' || // 검색어가 없으면 무조건 포함
      (props.activeTab === 'deposit'
        ? product.deposit_id__fin_prdt_nm
            .toLowerCase()
            .includes(props.filters.searchQuery.toLowerCase()) // 예금 상품명 검색
        : product.saving_id__fin_prdt_nm
            .toLowerCase()
            .includes(props.filters.searchQuery.toLowerCase())); // 적금 상품명 검색

    console.log(props.filters.searchQuery.trim())
    // 기타 필터링 조건

    
    const matchesBank = props.filters.banks === '' || 
      (props.activeTab === 'deposit' 
        ? product.deposit_id__kor_co_nm 
        : product.saving_id__kor_co_nm
      ).includes(props.filters.banks);


    const matchesPeriod =
      props.filters.savingsPeriod.length === 0 ||
      props.filters.savingsPeriod.includes(product.save_trm);
    const matchesCalculation =
      product.intr_rate_type_nm === props.filters.interestCalculation ||
      props.filters.interestCalculation === '전체';
    const matchesEligibility =
      props.filters.eligibility.length === 0 ||
      props.filters.eligibility.includes(
        props.activeTab === 'deposit'
          ? product.deposit_id__join_deny
          : product.saving_id__join_deny
      );
    const matchesMethod =
      props.filters.applicationMethods.length === 0 ||
      props.filters.applicationMethods.some((method) => {
        const productMethods = (props.activeTab === 'deposit'
          ? product.deposit_id__join_way
          : product.saving_id__join_way
        )
          .split(',') // 쉼표로 구분된 문자열을 배열로 변환
          .map((m) => m.trim()); // 공백 제거

        return productMethods.includes(method);
      });

    return (
      matchesBank &&
      matchesSearch && // 검색 조건 추가
      matchesPeriod &&
      matchesCalculation &&
      matchesEligibility &&
      matchesMethod
    );
  });
});

// 정렬 토글 함수
const sortKey = ref("intr_rate2"); // 초기 정렬 기준: 최고 우대금리
const sortOrder = ref("desc"); // 초기 정렬 방향: 내림차순

const toggleSort = (key) => {
  if (sortKey.value === key) {
    // 현재 정렬 기준이 동일하면 방향 전환
    sortOrder.value = sortOrder.value === "desc" ? "asc" : "desc";
  } else {
    // 새로운 기준으로 변경
    sortKey.value = key;
    sortOrder.value = "desc"; // 새로운 정렬 기준은 기본적으로 내림차순
  }
};


// 정렬된 상품 계산
const sortedProducts = computed(() => {
  return [...filteredProducts.value].sort((a, b) => {
    const multiplier = sortOrder.value === "asc" ? 1 : -1;
    return (a[sortKey.value] - b[sortKey.value]) * multiplier;
  });
});

// const sortedProducts = computed(() => {
//   return [...filteredProducts.value].sort((a, b) => b[sortKey.value] - a[sortKey.value]);
// });

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
/* 검색창 및 버튼 스타일 */
.search-bar {
  display: flex; /* 내부 요소 가로 정렬 */
  justify-content: center; /* 가운데 정렬 */
  align-items: center; /* 세로 가운데 정렬 */
  gap: 10px; /* 검색창과 버튼 사이 간격 */
  margin-bottom: 20px; /* 아래 간격 */
}

.search-bar input {
  width: 300px; /* 검색창 너비 */
  padding: 10px; /* 안쪽 여백 */
  border: 1px solid #ccc; /* 테두리 */
  border-radius: 5px; /* 모서리 둥글게 */
  font-size: 16px; /* 글자 크기 */
  outline: none; /* 선택 시 외곽선 제거 */
  transition: all 0.3s ease; /* 애니메이션 효과 */
}

.search-bar input:focus {
  border-color: #3f2411; /* 포커스 시 테두리 색 변경 */
  box-shadow: 0 0 5px rgba(63, 36, 17, 0.5); /* 그림자 추가 */
}

.search-bar button {
  background-color: #3f2411; /* 버튼 배경색 */
  color: white; /* 버튼 텍스트 색상 */
  border: none; /* 테두리 제거 */
  padding: 10px 20px; /* 안쪽 여백 */
  border-radius: 5px; /* 모서리 둥글게 */
  font-size: 16px; /* 글자 크기 */
  cursor: pointer; /* 포인터로 변경 */
  transition: all 0.3s ease; /* 애니메이션 효과 */
}

.search-bar button:hover {
  background-color: #6d4c41; /* 마우스 올릴 때 배경색 변경 */
}

.loading {
  text-align: center;
  margin: 20px;
  font-size: 18px;
  color: #6d4c41;
}

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

.modal-btn {
  justify-content: center;
  display: flex;
}

.modal-btn button {
  padding: 10px 20px;
  margin-top: 15px;
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

th.active {
  background-color: #6d4c41; /* 활성화된 열 배경색 */
  color: white;
}
th span {
  margin-left: 5px;
  font-size: 12px;
}

th.ascending::after {
  content: "▲"; /* 오름차순 화살표 */
  margin-left: 5px;
  font-size: 12px;
  color: #fff;
}

th.descending::after {
  content: "▼"; /* 내림차순 화살표 */
  margin-left: 5px;
  font-size: 12px;
  color: #fff;
}


.modal-details {
  margin-top: 20px;
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
  margin: 20px 0;
  color: white;

}

.pagination button {
  padding: 8px 12px;
  margin: 0 5px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

.pagination button.active {
  background-color: #3f2411;
  font-weight: bold;
}

.pagination button:hover {
  background-color: #3f2411;
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

.col-rank {
  width: 10%; /* 순위 열 */
}

.col-company {
  width: 20%; /* 금융회사 열 */
}

.col-product {
  width: 30%; /* 상품명 열 */
}

.col-rate,
.col-rate2 {
  width: 15%; /* 금리 열 */
}

.col-eligibility {
  width: 10%; /* 가입 대상 열 */
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
