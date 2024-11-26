<template>
  <div class="products-page">

		<div class="products-list">
			<div class="products-list-title">
				<h3>내가 가입한 상품</h3>
        <p class="description">각 상품을 선택하면<br>상세 정보를 확인할 수 있습니다.</p>
        <RouterLink :to="{name: 'savings'}"><button class="goButton">가입하러 가기</button></RouterLink>
        
			</div>
			<div class="products-list-content">
				<div v-if="productList.deposits.length || productList.savings.length">
					<ul>
						<div class="products-list-deposits">
							<h4>예금</h4>
							<hr style="margin: 0 0 12px; width: 80%;">
							<li 
								v-for="(product, index) in productList.deposits" 
								:key="`deposit-${index}`" 
								@click="openDetailModal(product, 'deposit')"
							>
								<span>{{ product.deposit_id__fin_prdt_nm }}</span>
							</li>
              <div class="chart-container">
                <canvas id="depositChart" ref="depositChart"></canvas>
              </div>
						</div>
						<br>
						<div class="products-list-savings">
							<h4>적금</h4>
							<hr style="margin: 0 0 12px; width: 80%;">
							<li 
								v-for="(product, index) in productList.savings" 
								:key="`saving-${index}`" 
								@click="openDetailModal(product, 'saving')"
							>
								<span>{{ product.saving_id__fin_prdt_nm }}</span>	
							
							</li>
              <div class="chart-container">
                <canvas id="savingChart" ref="savingChart"></canvas>
              </div>
						</div>

					</ul>
				</div>
				<div v-else>
          <p style="margin:10px;">아직 가입한 상품이 없습니다.</p>
				</div>

				<!-- 상세 정보 모달 -->
				<div v-if="selectedProduct" class="modal-overlay" @click.self="closeDetailModal">
					<div class="modal-content">
						<button class="close-btn" @click="closeDetailModal" aria-label="Close modal">×</button>
						
						<header>
							<h2>
								{{ selectedProduct.type === 'deposit' 
									? selectedProduct.deposit_id__fin_prdt_nm 
									: selectedProduct.saving_id__fin_prdt_nm 
								}}
							</h2>
						</header>
						
						<div class="modal-details">
              <header>
               <h2>{{ selectedProduct.fin_prdt_nm }}</h2>
              </header>

              <div class="modal-details">
                <div class="detail-row">
                  <span class="detail-label">금융회사</span>
                  <span class="detail-value">
                    {{ selectedProduct.type === 'deposit' 
                    ? selectedProduct.deposit_id__kor_co_nm
                    : selectedProduct.saving_id__kor_co_nm
                    }}
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
                    {{ selectedProduct.type === 'deposit' 
                    ? joinDenyMapping[selectedProduct.deposit_id__join_deny]
                    : joinDenyMapping[selectedProduct.saving_id__join_deny] }}
                  </span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">저축 기간</span>
                  <span class="detail-value">{{ selectedProduct.save_trm }}개월</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">가입 방법</span>
                  <span class="detail-value">
                    {{ selectedProduct.type === 'deposit' 
                    ? selectedProduct.deposit_id__join_way
                    : selectedProduct.saving_id__join_way }}
                  </span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">우대 조건</span>
                  <span class="detail-value">
                    {{ selectedProduct.type === 'deposit' 
                    ? selectedProduct.deposit_id__spcl_cnd
                    : selectedProduct.saving_id__spcl_cnd }}%
                  </span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">금리 유형</span>
                  <span class="detail-value">{{ selectedProduct.intr_rate_type_nm }}</span>
                </div>
              </div>
            </div>

            <div class="modal-btn">
              <button v-if="!isAdded" @click="manageProduct('add')">가입하기</button>
              <button v-else @click="confirmRemove">가입 취소하기</button>
            </div>

					</div>
				</div>
			</div>
		</div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account"
import { useSavingsStore } from "@/stores/savings"
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios  from 'axios'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip);

const accountStore = useAccountStore()
const savingsStore = useSavingsStore()

const savingsData = ref([])
const depositsData = ref([])

const depositChart = ref(null);
const savingChart = ref(null);

const user = ref(null)
const router = useRouter()

const joinDenyMapping = {
  1: "제한없음",
  2: "서민전용",
  3: "일부제한",
};

const productList = computed(() => ({
  deposits: depositsData.value,
  savings: savingsData.value,
}));

onMounted(async () => {
  try {
    user.value = accountStore.user;
    const depositPromises = user.value?.product_list.deposits.map(item =>
      savingsStore.getDeposit(item).catch(err => console.error(`Failed to load deposit: ${err}`))
    );
    const savingsPromises = user.value?.product_list.savings.map(item =>
      savingsStore.getSaving(item).catch(err => console.error(`Failed to load saving: ${err}`))
    );
    depositsData.value = (await Promise.all(depositPromises)).filter(Boolean);
    savingsData.value = (await Promise.all(savingsPromises)).filter(Boolean);

    nextTick(() => {
      createDepositChart();
      createSavingChart();
    });
  } catch (error) {
    console.error('Error loading user data:', error);
  }
});

const selectedProduct = ref(null);

const openDetailModal = (product, type) => {
  selectedProduct.value = { ...product, type };
};

const closeDetailModal = () => {
  selectedProduct.value = null;
};

// 상품 가입 여부
const isAdded = computed(() => {

  const productType = selectedProduct.value.type === 'deposit' ? 'deposits' : 'savings'
  const productId = selectedProduct.value.id

  const userProducts = accountStore.user?.product_list[productType]

  return userProducts.includes(productId)
})


const manageProduct = async (action) => {
  if (!selectedProduct.value) return;

  const productType = selectedProduct.value.type === 'deposit' ? 'deposits' : 'savings';
  const productId = selectedProduct.value.id; // Ensure this is the correct property

  try {
    await axios.post('http://127.0.0.1:8000/accounts/manage-product/', {
      action,
      product_type: productType,
      product_id: productId,
    }, {
      headers: {
        'Authorization': `Token ${accountStore.token}`,
      },
    });
    accountStore.fetchUser();
  } catch (error) {
    console.error('Error managing product:', error);
  }
};

const confirmRemove = () => {
  if (confirm("정말 가입을 취소하시겠습니까?")) {
    manageProduct('remove');
    closeDetailModal()
    router.go(0)
  }
};


const createDepositChart = () => {
  if (!depositChart.value) return;
  const ctx = depositChart.value.getContext("2d");
  const labels = depositsData.value.map((item) => item.deposit_id__fin_prdt_nm);
  const data1 = depositsData.value.map((item) => item.intr_rate);
  const data2 = depositsData.value.map((item) => item.intr_rate2);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "기본 금리 (%)",
          data: data1,
          backgroundColor: "#6F4E37",
          borderWidth: 1,
        },
        {
          label: "최대 금리 (%)",
          data: data2,
          backgroundColor: "#F5DEB3",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
};

const createSavingChart = () => {
  if (!savingChart.value) return;
  const ctx = savingChart.value.getContext("2d");
  const labels = savingsData.value.map((item) => item.saving_id__fin_prdt_nm);
  const data1 = savingsData.value.map((item) => item.intr_rate);
  const data2 = savingsData.value.map((item) => item.intr_rate2);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "기본 금리 (%)",
          data: data1,
          backgroundColor: "#6F4E37",
          borderWidth: 1,
        },
        {
          label: "최대 금리 (%)",
          data: data2,
          backgroundColor: "#F5DEB3", 
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
};

</script>

<style scoped>
.products-page {
	display: flex;
	flex-direction: column;
}

.products-list,
.products-chart {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	gap: 20px;
	margin-bottom: 20px;
}

.products-list-title,
.products-chart-title {
	width: 30%;
	text-align: right;
}

.description {
  font-size: 12px;
  color: gray;
}

.products-list-content {
	flex: 1;
}


.products-chart-content {
	flex: 1;
}

h3 {
	font-size: 22px;
	font-weight: bolder;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}

h4 {
	font-size: 17px;
	font-weight: bolder;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}

.products-list-deposits,
.products-list-savings {
	margin-bottom: 20px;
}

.products-list li {
	list-style: none;
	margin: 10px;
}

.goButton {
  margin-top: 10px;
  padding: 8px 10px;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}


/* 차트 */

.chart-container {
  display: flex;
  justify-content: center;

}
canvas {
  max-width: 400px;
  max-height: 300px;
}

/* 모달 */

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



</style>