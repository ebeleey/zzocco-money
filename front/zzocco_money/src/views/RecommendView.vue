<template>
  <div>
    <h1 class="page-title">
      {{ user.name }}님에게<br />
      딱 맞는 예적금 상품 Top3
    </h1>
    <!-- <h4>{{ user.name }}님과 비슷한 관심사와 상황의<br />
      다른 사용자들이 선택한 인기 예적금 상품을 모아봤어요.</h4> -->

    <!-- <h4>{{ user.name }}님의 소비 성향과 재정 목표를 기반으로<br />
      최적의 예적금 상품을 추천드려요.</h4> -->
    <h4>{{ user.name }}님의 소비 성향과 재정 목표를 기반으로<br />
      다른 사용자들이 선택한 인기 예적금 상품을 모아봤어요.</h4>

    <!-- 슬라이드 생성 -->
    <div class="recommend-page">
      <div
      v-for="(item, index) in slides"
      :key="index"
      class="recommendations"
      >
        <div class="recommendation">
          <div class="recommendation-header">
            <h3>{{ item.product_type === 'deposit' ? item.deposit_id__kor_co_nm : item.saving_id__kor_co_nm }}</h3>
            <h2 class="product-name">{{ item.product_type === 'deposit' ? item.deposit_id__fin_prdt_nm : item.saving_id__fin_prdt_nm }}</h2>
          </div>
          <hr />
          <div class="recommendation-content">
            <p>기본 금리: {{ item.intr_rate }}% | </p>
            <br>
            <p> 최고 우대 금리: {{ item.intr_rate2 }}%</p>
          </div>
        </div>
      </div>
    </div>

 
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import axios from "axios";
import { ref, onMounted } from "vue";

const accountStore = useAccountStore();
const user = ref({});
const slides = ref([]);
const currentSlide = ref(0); // 현재 슬라이드 인덱스

onMounted(async () => {
  try {
    await accountStore.fetchUser();
    user.value = accountStore.user;

    await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/savings/similar-users/${user.value.id}/`
    }) .then((res)  => {
      slides.value = res.data.top_3_products
      console.log(res)
    })
      .catch(err => console.log(err))
    
  } catch (error) {
    console.error(error);
  }
});
</script>

<style lang="scss" scoped>
.recommend-page {
  margin-top: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap; // Allows items to wrap to the next line if needed
}

.recommendations {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #fff;
  flex-direction: row; // Default to horizontal layout
}

.recommendation {
  display: flex;
  flex-direction: column;
  padding: 30px;
  width: 350px;
  height: 400px;
  margin: 10px; // Add some margin for spacing between items
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Media query for smaller screens */
@media (max-width: 768px) {
  .recommendations {
    flex-direction: column; // Change to vertical layout on smaller screens
    width: 100%; // Make sure it takes full width
    align-items: stretch; // Align items to stretch full width
  }

  .recommendation {
    margin-bottom: 20px; // Add spacing between items in vertical layout
    width: calc(100% - 20px); // Adjust width to fit within container with margin
    box-sizing: border-box; // Ensure padding and border are included in the width
  }
}

.recommendation-header {
  height: 30%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 10px;
}


.recommendation-content {
  flex: 1;
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
}

h1 {
  margin-bottom: 20px;
}

h2 {
  text-align: center;
  font-weight: bolder;
  font-size: 32px;
  line-height: 1.2; // 줄 간격 조정
  word-break: keep-all; // 단어 단위로 줄바꿈
  white-space: pre-wrap; // 공백 유지 및 자동 줄바꿈
}

h3 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 0;
}

h4 {
  font-size: 15px;
  text-align: center;
}

hr {
  height: 3px;
  margin: 0px;
  background-color: #3f2411;

}

p {
  margin-top: 20px;


}
</style>