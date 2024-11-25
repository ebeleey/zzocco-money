<template>
	<div>
		<!-- {{ user.product_list }} -->
		<ul>
      <!-- <li v-for="(product, index) in user.product_list['savings']" :key="index">
        {{ product }}
      </li> -->
    </ul>

		<!-- <canvas id="myChart" ref="chartCanvas"></canvas> -->
	</div>
</template>
  
<script setup>
// import {
// 	Chart,
// 	BarController,
// 	BarElement,
// 	CategoryScale,
// 	LinearScale,
// 	Title,
// 	Tooltip,
// 	Legend,
// } from "chart.js";

// Chart.register(
// 	BarController,
// 	BarElement,
// 	CategoryScale,
// 	LinearScale,
// 	Title,
// 	Tooltip,
// 	Legend
// );

import { useAccountStore } from "@/stores/account"
import { useSavingsStore } from "@/stores/savings"
import { ref, onMounted } from 'vue'

const accountStore = useAccountStore()
const savingsStore = useSavingsStore()


const savingsData = ref([])

onMounted(async () => {
	try {
		const accountStore = useAccountStore()
		const savingsStore = useSavingsStore()
		const user = accountStore.user
		const savingsData = ref([])
		console.log(user)
		console.log(user.product_list)
		for ( const item of user.product_list['deposits']) {
			console.log("여긴 for문 안")
			console.log(item)
			console.log(savingsStore.getDeposit(item))
			savingsData.value.push(savingsStore.getDeposit(item))	
		}
		console.log("savings", savingsData)

	} catch (error) {
		console.error(error)
	}
})




// export default {
// 	name: "UserProductChart"
// 	// data() {
// 	// 	return {
// 	// 		user: {
// 	// 			product_list: [
// 	// 				{ name: "적금1", amount: 100 },
// 	// 				{ name: "적금2", amount: 200 },
// 	// 				{ name: "적금3", amount: 150 },
// 	// 				{ name: "적금4", amount: 50 },
// 	// 				{ name: "적금5", amount: 120 },
// 	// 			],
// 	// 		},
// 	// 		chart: null, // Chart.js 인스턴스
// 	// 	};
// 	// },
// 	computed: {
// 		user() {
// 			const accountStore = useAccountStore()
// 			return accountStore.user
// 		}

	// 	// Chart.js에 사용될 데이터 가공
	// 	chartData() {
	// 		const labels = this.user.product_list.map((product) => product.name); // 상품 이름
	// 		const data = this.user.product_list.map((product) => product.amount); // 상품 금액
	// 		return {
	// 			labels,
	// 			datasets: [
	// 				{
	// 					label: "금융상품 금액",
	// 					data,
	// 					backgroundColor: [
	// 						"rgba(255, 99, 132, 0.2)",
	// 						"rgba(54, 162, 235, 0.2)",
	// 						"rgba(255, 206, 86, 0.2)",
	// 						"rgba(75, 192, 192, 0.2)",
	// 						"rgba(153, 102, 255, 0.2)",
	// 					],
	// 					borderColor: [
	// 						"rgba(255, 99, 132, 1)",
	// 						"rgba(54, 162, 235, 1)",
	// 						"rgba(255, 206, 86, 1)",
	// 						"rgba(75, 192, 192, 1)",
	// 						"rgba(153, 102, 255, 1)",
	// 					],
	// 					borderWidth: 1,
	// 				},
	// 			],
	// 		};
	// 	},
	// },
	// mounted() {
	// 	this.renderChart();
	// },
	// methods: {
	// 	renderChart() {
	// 		const ctx = this.$refs.chartCanvas.getContext("2d");
	// 		this.chart = new Chart(ctx, {
	// 			type: "bar", // 차트 유형: bar, line, pie 등
	// 			data: this.chartData,
	// 			options: {
	// 				responsive: true,
	// 				plugins: {
	// 					legend: {
	// 						display: true,
	// 						position: "top",
	// 					},
	// 				},
	// 			},
	// 		});
	// 	},
	// },
	// beforeDestroy() {
	// 	// 컴포넌트가 소멸될 때 차트를 삭제
	// 	if (this.chart) {
	// 		this.chart.destroy();
	// 	}
	// },
// };

</script>
  
<style scoped>
canvas {
	max-width: 100%;
	max-height: 400px;
}
</style>
