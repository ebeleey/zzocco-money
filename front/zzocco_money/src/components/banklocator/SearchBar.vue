
<template>
	<div>
		<div class="select-bar">
			<!-- 광역시/도 선택 -->
			<div class="dropdown">
				<button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
					{{ selectedProvince || '광역시/도' }}
				</button>
				<ul class="dropdown-menu">
					<li class="dropdown-item" v-for="province in provinces" :key="province" @click="selectProvince(province)">
						{{ province }}
					</li>
				</ul>
			</div>

			<!-- 시/군/구 선택 -->
			<div class="dropdown">
				<button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
					{{ selectedCity || '시/군/구' }}
				</button>
				<ul class="dropdown-menu">
					<li class="dropdown-item" v-for="city in cities" :key="city" @click="selectCity(city)">
						{{ city }}
					</li>
				</ul>
			</div>

			<!-- 은행 선택 -->
			<div class="dropdown">
				<button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
					{{ selectedBank || '은행 선택' }}
				</button>
				<ul class="dropdown-menu">
					<li class="dropdown-item" v-for="bank in banks" :key="bank" @click="selectBank(bank)">
						{{ bank }}
					</li>
				</ul>
			</div>

			<button @click="emitSelectionChange">
				찾기
			</button>
		</div>
	</div>
</template>
  
<script setup>
import { ref, watch } from 'vue'

// 부모로부터 전달받은 props
const props = defineProps({
	provinces: Array,
	citiesData: Object,
	banks: Array,
})
  
const emit = defineEmits(['selection-changed', 'bank-locations-found', 'search'])

// 선택된 province, city, bank 상태
const selectedProvince = ref(null)
const selectedCity = ref(null)
const selectedBank = ref(null)

const showProvinceDropdown = ref(false);
const showCityDropdown = ref(false);
const showBankDropdown = ref(false);

watch(selectedProvince, (newProvince) => {
	cities.value = props.citiesData[newProvince] || [];
	selectedCity.value = null;
});

// province에 따라 동적으로 업데이트 될 cities
const cities = ref([])

const selectProvince = (province) => {
	selectedProvince.value = province;
	showProvinceDropdown.value = false;
};

const selectCity = (city) => {
	selectedCity.value = city;
	showCityDropdown.value = false;
};

const selectBank = (bank) => {
	selectedBank.value = bank;
	showBankDropdown.value = false;
};

// 부모 컴포넌트에 선택된 값 전달
const emitSelectionChange = () => {
	emit('selection-changed', {
		province: selectedProvince.value,
		city: selectedCity.value,
		bank: selectedBank.value,
	})
}
</script>

<style scoped>
  
button {
	background-color: #3f2411; /* 버튼 기본 배경색 */
	border-color: #3f2411; /* 버튼 기본 테두리 색상 */
	color: white; /* 텍스트 색상 */
	padding: 10px 20px; /* 드롭다운 버튼과 동일한 패딩 */
	font-size: 16px; /* 드롭다운 버튼과 동일한 글꼴 크기 */
	border-radius: 4px; /* 버튼의 모서리를 동일하게 둥글림 */
	height: auto; /* 높이를 자동으로 조정 */
	transition: background-color 0.3s ease, color 0.3s ease;
}

button:hover {
	background-color: rgba(228, 217, 211, 0.829); /* hover 상태의 배경색 */
	color: black; /* hover 상태의 텍스트 색상 */
	border-color: rgba(228, 217, 211, 0.829);
}

button.btn:focus {
	background-color: rgba(228, 217, 211, 0.829); /* 클릭 후 포커스 상태의 배경색 */
	color: #111; /* 포커스 상태의 텍스트 색상 */
	border-color: rgba(228, 217, 211, 0.829); /* 포커스 상태의 테두리 색상 */
	outline: none; /* 포커스 테두리 제거 */
}

.select-bar button:last-child {
	height: 100%; /* 다른 버튼의 높이와 일치 */
	display: flex;
	align-items: center; /* 텍스트를 중앙 정렬 */
	justify-content: center;
}


.select-bar {
	display: flex;
	justify-content: center; /* 가로 중앙 정렬 */
	align-items: center; /* 세로 중앙 정렬 */
	gap: 20px; /* 각 dropdown 사이 간격 */
}

.dropdown {
	min-width: 180px; /* 각 dropdown의 최소 너비 설정 */
}

.dropdown-toggle {
	display: flex; /* flexbox 레이아웃 사용 */
	justify-content: space-between; /* 텍스트와 화살표를 양 끝에 배치 */
	align-items: center; /* 세로 중앙 정렬 */
	width: 100%; /* 버튼이 부모 요소 크기만큼 차지하도록 설정 */
	padding: 10px 20px; /* 버튼 크기 조정 */
}

.dropdown-toggle::after {
	margin-left: 10px; /* 화살표와 텍스트 간의 간격 */
	position: relative;
	left: auto;
}
</style>