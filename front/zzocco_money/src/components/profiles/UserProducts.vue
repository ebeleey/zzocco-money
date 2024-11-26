<template>
  <div class="products-page">
    <!-- <div class="charts-container">
				<div>
					<h4>예금</h4>
					<canvas id="depositChart" ref="depositChart"></canvas>
				</div>
				<div>
					<h4>적금</h4>
					<canvas id="savingChart" ref="savingChart"></canvas>
				</div>
			</div> -->
		<div class="products-list">
			<div class="products-list-title">
				<h3>내가 가입한 상품</h3>
        
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
					데이터가 없습니다.
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
							<!-- 각 detail-row에 대한 내용은 동일하게 유지 -->
						</div>

						<div v-if="isLoggedIn" class="modal-btn">
							<button v-if="!isAdded" @click="manageProduct('add')">가입하기</button>
							<button v-else @click="manageProduct('remove')">가입 취소하기</button>
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
const isLoggedIn = computed(() => accountStore.isLogin)

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
		if (productType === 'deposits') {
      depositsData.value = depositsData.value.filter(item => item.id !== productId);
    } else {
      savingsData.value = savingsData.value.filter(item => item.id !== productId);
    }
    closeDetailModal();
    accountStore.fetchUser();
  } catch (error) {
    console.error('Error managing product:', error);
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

.products-list-content {
	flex: 1;
}


.products-chart-content {
	flex: 1;
}

h3 {
	font-size: 22px;
	font-weight: bolder;
}

h4 {
	font-size: 17px;
	font-weight: bolder;
}

.products-list-deposits,
.products-list-savings {
	margin-bottom: 20px;
}

.products-list li {
	list-style: none;
	margin: 10px;
}

.chart-container {
  display: flex;
  justify-content: center;

}
canvas {
  max-width: 400px;
  max-height: 300px;
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


</style>