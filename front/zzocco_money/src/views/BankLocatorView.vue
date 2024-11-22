<template>
	<div class="savings-page">
		<h1 class="page-title">근처 은행 찾기</h1>
		<div class="bank-view">
			<SearchBar
				:provinces="provinces"
				:cities-data="citiesData"
				:banks="banks"
				@selection-changed="updateSelection"
			/>
			<div ref="mapContainer" style="width: 40rem; height: 30rem; margin: 50px 0 10px;"></div>
		</div>
	</div>
</template>
  
<script setup>
import { ref, onMounted, watch } from 'vue'
import SearchBar from '@/components/banklocator/SearchBar.vue'

// 행정구역 데이터
const citiesData = ref({
	"서울특별시":[
			"종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"
	],
	"부산광역시":[
			"중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "강서구", "해운대구", "사하구", "금정구", "연제구", "수영구", "사상구", "기장군"
	],
	"인천광역시":[
			"중구", "동구", "남구", "연수구", "남동구", "부평구", "계양구", "서구", "강화군", "옹진군"
	],
	"대구광역시":[
			"중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"
	],
	"광주광역시":[
			"동구", "서구", "남구", "북구", "광산구"
	],
	"대전광역시":[
			"동구", "중구", "서구", "유성구", "대덕구"
	],
	"울산광역시":[
			"중구", "남구", "동구", "북구", "울주군"
	],
	"세종특별자치시":[
			
	],
	"경기도":[
			"가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"
	],
	"강원도":[
			"원주시", "춘천시", "강릉시", "동해시", "속초시", "삼척시", "홍천군", "태백시", "철원군", "횡성군", "평창군", "영월군", "정선군", "인제군", "고성군", "양양군", "화천군", "양구군"
	],
	"충청북도":[
			"청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"
	],
	"충청남도":[
			"천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"
	],
	"경상북도":[
			"포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "군위군", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"
	],
	"경상남도":[
			"창원시", "김해시", "진주시", "양산시", "거제시", "통영시", "사천시", "밀양시", "함안군", "거창군", "창녕군", "고성군", "하동군", "합천군", "남해군", "함양군", "산청군", "의령군"
	],
	"전라북도":[
			"전주시", "익산시", "군산시", "정읍시", "완주군", "김제시", "남원시", "고창군", "부안군", "임실군", "순창군", "진안군", "장수군", "무주군"
	],
	"전라남도":[
			"여수시", "순천시", "목포시", "광양시", "나주시", "무안군", "해남군", "고흥군", "화순군", "영암군", "영광군", "완도군", "담양군", "장성군", "보성군", "신안군", "장흥군", "강진군", "함평군", "진도군", "곡성군", "구례군"
	],
	"제주특별자치도":[
			"제주시", "서귀포시"
	]
})

// 광역시 / 도
const provinces = Object.keys(citiesData.value)
// 은행
const banks = ref(["국민은행", "신한은행", "하나은행", "우리은행", "기업은행", "농협은행", "산업은행", "부산은행", "SC제일은행", "한국씨티은행", "대구은행", "수협은행", "경남은행", "광주은행", "전북은행", "제주은행"])

// 선택 위치 및 은행
const selectedProvince = ref("")
const selectedCity = ref("")
const selectedBank = ref("")

// 지도객체 및 데이터
const mapContainer = ref(null)
const map = ref(null)
const infowindow = ref(null)

const APP_KEY = import.meta.env.VITE_APP_API_KEY

// 검색 시 콜백함수 호출
const updateSelection = (selection) => {
	selectedProvince.value = selection.province
	selectedCity.value = selection.city
	selectedBank.value = selection.bank
	clearMarkers()  // 마커 초기화
  searchPlaces()  // 새로운 검색 시작
}


const markers = ref([])  // 마커를 저장할 배열

// 마커 초기화
const clearMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
}

// 지도 초기화
const initMap = () => {
  const options = {
    center: new window.kakao.maps.LatLng(37.566826, 126.9786567),
    level: 3
  }
  map.value = new window.kakao.maps.Map(mapContainer.value, options)
  infowindow.value = new window.kakao.maps.InfoWindow({zIndex:1})
}

// 지도 검색
const searchPlaces = () => {
  if (!map.value) return

  const ps = new window.kakao.maps.services.Places()
  const keyword = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`

  ps.keywordSearch(keyword, placesSearchCB, {
		category_group_code: 'BK9',
	})
}

// 지도 검색 시 콜백함수 실행
const placesSearchCB = (data, status) => {
  if (status === window.kakao.maps.services.Status.OK) {
    const bounds = new window.kakao.maps.LatLngBounds()


    for (let i = 0; i < data.length; i++) {
      displayMarker(data[i])
      bounds.extend(new window.kakao.maps.LatLng(data[i].y, data[i].x))
    }

    map.value.setBounds(bounds)
  }
}

// 지도에 마커 표시하기
const displayMarker = (place) => {
  const marker = new window.kakao.maps.Marker({
    map: map.value,
    position: new window.kakao.maps.LatLng(place.y, place.x)
  })
	markers.value.push(marker)  // 마커를 배열에 추가
  window.kakao.maps.event.addListener(marker, 'click', () => {
    infowindow.value.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>')
    infowindow.value.open(map.value, marker)
  })
}

// 스크립트 로드하기
const loadScript = () => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${APP_KEY}&libraries=services&autoload=false`
  script.onload = () => window.kakao.maps.load(() => {
    initMap()
    searchPlaces()
  })
  document.head.appendChild(script)
}

onMounted(() => {
  loadScript()
})

watch([selectedProvince, selectedCity, selectedBank], () => {
  if (map.value) {
    searchPlaces()
  }
})
</script>

<style scoped>

.bank-view {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}


.mapContainer {
  margin-top: 50px;
}
</style>