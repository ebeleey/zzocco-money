<template>
  <div>
    <div>
      <h2>회원정보 수정</h2>
      <form @submit.prevent="submitUpdate">
        <div class="basic-info-item">
          <label>이름</label>
          <input type="text" v-model="editData.name" />
        </div>
        <div class="basic-info-item">
          <label>성별</label>
          <select v-model="editData.gender">
            <option v-for="(label, key) in GENDER_CHOICES" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
        <div class="basic-info-item">
          <label>혼인 여부</label>
          <select v-model="editData.marriage">
            <option v-for="(label, key) in MARRIAGE_CHOICES" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
        <div class="basic-info-item">
          <label>수입 전망</label>
          <select v-model="editData.income_prospect">
            <option v-for="(label, key) in INCOME_PROSPECT_CHOICES" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
        <div class="basic-info-item">
          <label>총 자산 규모</label>
          <select v-model="editData.asset_level">
            <option v-for="(label, key) in ASSET_LEVEL_CHOICES" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
        <div class="basic-info-item">
          <label>연 평균 소득</label>
          <select v-model="editData.income_level">
            <option v-for="(label, key) in INCOME_LEVEL_CHOICES" :key="key" :value="key">{{ label }}</option>
          </select>
        </div>
        <button type="submit">저장</button>
        <button @click="cancelEdit">취소</button>
      </form>
  </div>
</template>

<script setup>

</script>

<style lang="scss" scoped>

</style>