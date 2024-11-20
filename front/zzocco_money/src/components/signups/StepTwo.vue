<template>
  <div>
    <h2>상세 정보 입력</h2>
    <form>
      <!-- 성별 선택 -->
      <div>
        <label for="gender">성별:</label>
        <div class="checkbox-container">
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.gender === 'male'}"
            @click="formData.detailedInfo.gender = 'male'"
          >
            남성
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.gender === 'female'}"
            @click="formData.detailedInfo.gender = 'female'"
          >
            여성
          </div>
        </div>
      </div>

      <!-- 혼인 여부 선택 -->
      <div>
        <label for="marriage">혼인 여부:</label>
        <div class="checkbox-container">
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.marriage === 'single'}"
            @click="formData.detailedInfo.marriage = 'single'"
          >
            미혼
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.marriage === 'married'}"
            @click="formData.detailedInfo.marriage = 'married'"
          >
            기혼
          </div>
        </div>
      </div>

      <!-- 현재와 미래 수입 전망 -->
      <div>
        <label for="income_prospect">현재와 미래 수입 전망:</label>
        <div class="checkbox-container">
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_prospect === 'stable_increase'}"
            @click="formData.detailedInfo.income_prospect = 'stable_increase'"
          >
            안정적 증가
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_prospect === 'unstable'}"
            @click="formData.detailedInfo.income_prospect = 'unstable'"
          >
            불안정
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_prospect === 'decreasing'}"
            @click="formData.detailedInfo.income_prospect = 'decreasing'"
          >
            감소
          </div>
        </div>
      </div>

      <!-- 자산 규모 선택 -->
      <div>
        <label for="asset_level">총 자산 규모:</label>
        <div class="checkbox-container">
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.asset_level === 'below_10m'}"
            @click="formData.detailedInfo.asset_level = 'below_10m'"
          >
            1천만 원 이하
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.asset_level === '10m_to_50m'}"
            @click="formData.detailedInfo.asset_level = '10m_to_50m'"
          >
            1천만~5천만원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.asset_level === '50m_to_100m'}"
            @click="formData.detailedInfo.asset_level = '50m_to_100m'"
          >
            5천만~1억 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.asset_level === '100m_to_500m'}"
            @click="formData.detailedInfo.asset_level = '100m_to_500m'"
          >
            1억~5억 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.asset_level === '500m_to_1b'}"
            @click="formData.detailedInfo.asset_level = '500m_to_1b'"
          >
            5억~10억 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.asset_level === 'above_1b'}"
            @click="formData.detailedInfo.asset_level = 'above_1b'"
          >
            10억 원 이상
          </div>
        </div>
      </div>

      <!-- 연 평균 소득 선택 -->
      <div>
        <label for="income_level">연 평균 소득:</label>
        <div class="checkbox-container">
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_level === 'below_30m'}"
            @click="formData.detailedInfo.income_level = 'below_30m'"
          >
            3천만 원 이하
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_level === '30m_to_50m'}"
            @click="formData.detailedInfo.income_level = '30m_to_50m'"
          >
            3천만~5천만 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_level === '50m_to_70m'}"
            @click="formData.detailedInfo.income_level = '50m_to_70m'"
          >
            5천만~7천만 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_level === '70m_to_100m'}"
            @click="formData.detailedInfo.income_level = '70m_to_100m'"
          >
            7천만~1억 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_level === '100m_to_300m'}"
            @click="formData.detailedInfo.income_level = '100m_to_300m'"
          >
            1억~3억 원
          </div>
          <div
            class="checkbox-box"
            :class="{'selected': formData.detailedInfo.income_level === 'above_300m'}"
            @click="formData.detailedInfo.income_level = 'above_300m'"
          >
            3억 원 이상
          </div>
        </div>
      </div>
    </form>
    <br>

    <!-- '이전' 버튼 추가 -->
    <button @click="$emit('previous-step')">이전</button>
    <!-- '다음' 버튼 추가 -->
    <button @click="$emit('next-step')">다음</button>
  </div>
</template>

<script setup>
defineProps({
  formData: Object
})
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.checkbox-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.checkbox-box {
  padding: 10px 20px;
  border: 2px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.checkbox-box.selected {
  background-color: #583423;
  color: white;
  border-color: #583423;
}

.checkbox-box:hover {
  background-color: #f0f0f0;
}
</style>
