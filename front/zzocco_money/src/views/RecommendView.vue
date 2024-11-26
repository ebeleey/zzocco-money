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
            {{ explanations[index] }}
            <br>
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
const api_key = import.meta.env.VITE_OPENAI_KEY

const explanations = ref([]); // 각 상품에 대한 설명을 저장할 배열

// ChatGPT API 호출 함수
const getExplanation = async (product) => {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: "gpt-3.5-turbo",
        messages: [{
          role: "user",
          content: `
          너는 시중은행 최고의 실적왕이야. 고객들에게 맞춤형 금융 상품을 추천하는 실력이 아주 뛰어나.
          나는 사용자의 개인 성향에 맞춰서 예적금 상품을 추천해주는 서비스를 만들려고 해. 해당 예금 상품에 대해 50자 이내로 간단한 설명을 해줬으면 좋겠어. 유저 정보는 다음과 같아.
          ${user.value}

          그리고 추천할 상품의 정보는 다음과 같아.
          상품명: ${product.product_type === 'deposit' ? product.deposit_id__fin_prdt_nm : product.saving_id__fin_prdt_nm}
          기관: ${product.product_type === 'deposit' ? product.deposit_id__kor_co_nm : product.saving_id__kor_co_nm}
          상품 종류: ${product.product_type}
          금리유형: ${product.intr_rate_type_nm}
          저축 기간: ${product.save_trm}개월
          기본 금리: ${product.intr_rate}%
          최고 우대 금리: ${product.intr_rate2}%
          기본 금리: ${product.intr_rate}%
          가입방법: ${product.product_type === 'deposit' ? product.deposit_id__join_way : product.saving_id__join_way}
          가입대상: ${product.product_type === 'deposit' ? product.deposit_id__join_member : product.saving_id__join_member}
          가입 제한: ${product.product_type === 'deposit' ? product.deposit_id__join_deny : product.saving_id__join_deny}
          우대조건: ${product.product_type === 'deposit' ? product.deposit_id__spcl_cnd : product.saving_id__spcl_cnd}
          기타 유의사항: ${product.product_type === 'deposit' ? product.deposit_id__etc_note : product.saving_id__etc_note}
          최고 한도: ${product.product_type === 'deposit' ? product.deposit_id__max_limit : product.saving_id__max_limit}
          참고로 가입 제한의 숫자가 나타내는 의미는 다음과 같아.
          1:제한없음, 2:서민전용, 3:일부제한

          단순 상품 설명은 제외하고, 상품의 특성을 해석해서 이 상품을 왜 사용자에게 추천하는지에 대해서만 알려줬으면 좋겠어. 예를 들면, "고수익 적금을 원한다면 이 상품을 추천합니다.", "우대금리 혜택이 풍부한 예금 상품입니다.", "스마트한 금융 상품으로, 유동성에 적합합니다." 같은 설명이었으면 좋겠어.
          `
        }]
      },
      {
        headers: {
          'Authorization': `Bearer ${api_key}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error calling ChatGPT API:', error);
    return "설명을 불러오는 데 실패했습니다.";
  }
};

onMounted(async () => {
  try {
    await accountStore.fetchUser();
    user.value = accountStore.user;

    const response = await axios.get(`http://127.0.0.1:8000/savings/similar-users/${user.value.id}/`);
    slides.value = response.data.top_3_products;
    
    // 각 상품에 대한 설명 요청
    for (const product of slides.value) {
      const explanation = await getExplanation(product);
      explanations.value.push(explanation);
    }
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
  font-size: 24px;
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