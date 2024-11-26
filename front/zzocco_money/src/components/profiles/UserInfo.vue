<template>
  <div class="info-page">
    <!-- <div class="profile-section">
      <div class="profile-image-container" @click="triggerFileInput">
        <img :src="getFullImageUrl(profileImagePreview || user.profile_image)" alt="Profile Image" />
        <div class="image-overlay">
          <i class="fas fa-camera"></i>
        </div>
      </div>
      <input
        type="file"
        accept="image/*"
        ref="fileInput"
        @change="onFileChange"
        style="display: none"
      />
      <button @click="uploadProfileImage" class="update-button">프로필 사진 변경</button>
    </div> -->

    <!-- 기본 정보는 수정 불가능 -->
    <div class="basic-info">
      <div class="basic-info-title">
        <h3>기본 정보</h3>
      </div>
      <div class="basic-info-container">
        <div class="basic-info-item">
          <h4>이름</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="user.name" readonly>
        </div>
        <br>
        <div class="basic-info-item">
          <h4>아이디</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="user.username" readonly>
        </div>
        <br>
        <div class="basic-info-item">
          <h4>이메일</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="user.email" readonly>
        </div>
      </div>
    </div>

    <!-- 추가 정보는 수정 가능 -->
    <div v-if="!editMode" class="additional-info" >
      <div class="additional-info-title">
        <h3>추가 정보</h3>
        <button @click="enterEditMode">회원정보 수정</button>
      </div>
      <div class="additional-info-container" >
        <div class="additional-info-item">
          <h4>성별</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="getChoiceLabel(user.gender, GENDER_CHOICES)" readonly />
        </div>
        <br>
        <div class="additional-info-item">
          <h4>혼인 여부</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="getChoiceLabel(user.marriage, MARRIAGE_CHOICES)" readonly />
        </div>
        <br>
        <div class="additional-info-item">
          <h4>현재와 미래 수입 전망</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="getChoiceLabel(user.income_prospect, INCOME_PROSPECT_CHOICES)" readonly />
        </div>
        <br>
        <div class="additional-info-item">
          <h4>총 자산 규모</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="getChoiceLabel(user.asset_level, ASSET_LEVEL_CHOICES)" readonly />
        </div>
        <br>
        <div class="additional-info-item">
          <h4>연 평균 소득</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input type="text" :value="getChoiceLabel(user.income_level, INCOME_LEVEL_CHOICES)" readonly />
        </div>
      </div>
    </div>
    <div v-else>
      <form @submit.prevent="submitUpdate" class="additional-info">   
        <div class="additional-info-title">
          <h3>추가 정보</h3>
          <div class="additional-info-button">
            <button @click="cancelEdit" class="edit-button cancel-button">취소</button>
            <button type="submit" class="edit-button">저장</button>
          </div>
        </div>
        <div class="additional-info-container">
          <div class="additional-info-item">
            <h4>성별</h4>
            <hr style="margin: 0 0 12px; width: 80%;">
            <select v-model="editData.gender">
              <option v-for="(label, key) in GENDER_CHOICES" :key="key" :value="key">{{ label }}</option>
            </select>
          </div>
          <br>
          <div class="additional-info-item">
            <h4>혼인 여부</h4>
            <hr style="margin: 0 0 12px; width: 80%;">
            <select v-model="editData.marriage">
              <option v-for="(label, key) in MARRIAGE_CHOICES" :key="key" :value="key">{{ label }}</option>
            </select>          
          </div>
          <br>
          <div class="additional-info-item">
            <h4>현재와 미래 수입 전망</h4>
            <hr style="margin: 0 0 12px; width: 80%;">
            <select v-model="editData.income_prospect">
              <option v-for="(label, key) in INCOME_PROSPECT_CHOICES" :key="key" :value="key">{{ label }}</option>
            </select>
          </div>
          <br>
          <div class="additional-info-item">
            <h4>총 자산 규모</h4>
            <hr style="margin: 0 0 12px; width: 80%;">
            <select v-model="editData.asset_level">
              <option v-for="(label, key) in ASSET_LEVEL_CHOICES" :key="key" :value="key">{{ label }}</option>
            </select>          
          </div>
          <br>
          <div class="additional-info-item">
            <h4>연 평균 소득</h4>
            <hr style="margin: 0 0 12px; width: 80%;">
            <select v-model="editData.income_level">
              <option v-for="(label, key) in INCOME_LEVEL_CHOICES" :key="key" :value="key">{{ label }}</option>
            </select>
          </div>
        </div>
      </form>
    </div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useRouter, RouterLink, RouterView } from 'vue-router';
import axios from 'axios'



const store = useAccountStore();
const router = useRouter()

const user = ref(store.user)
const editMode = ref(false);
const editData = ref({ ...user.value });

const GENDER_CHOICES = {
  'male': '남성',
  'female': '여성',
};
const MARRIAGE_CHOICES = {
  'single': '미혼',
  'married': '기혼',
};
const INCOME_PROSPECT_CHOICES = {
  'stable_increase': '안정적 증가',
  'unstable': '불안정',
  'decreasing': '감소',
};
const ASSET_LEVEL_CHOICES = {
  'below_10m': '1천만 원 이하',
  '10m_to_50m': '1천만~5천만 원',
  '50m_to_100m': '5천만~1억 원',
  '100m_to_500m': '1억~5억 원',
  '500m_to_1b': '5억~10억 원',
  'above_1b': '10억 원 이상',
};
const INCOME_LEVEL_CHOICES = {
  'below_30m': '3천만 원 이하',
  '30m_to_50m': '3천만~5천만 원',
  '50m_to_70m': '5천만~7천만 원',
  '70m_to_100m': '7천만~1억 원',
  '100m_to_300m': '1억~3억 원',
  'above_300m': '3억 원 이상',
};

const getChoiceLabel = (key, choices) => choices[key];

const submitUpdate = async () => {
  try {
    // console.log("user : ", user.value)
    // console.log("editData : ", editData.value) 
    const response = await axios.put('http://127.0.0.1:8000/accounts/user/', { ...editData.value }, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    store.fetchUser()
    alert("회원 정보가 성공적으로 수정되었습니다.");

    editMode.value = false
    router.go(0)
  } catch (error) {
    console.error(error);
  }
};

// 수정 모드 진입
const enterEditMode = () => {
  editMode.value = true;
};

// 수정 취소
const cancelEdit = () => {
  editMode.value = false;
  passwordVerified.value = false;
  password.value = '';
  editData.value = { ...user.value };
};

</script>

<style scoped>

.info-page {
  display: flex;
  flex-direction: column;
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

.basic-info,
.additional-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.basic-info-title,
.additional-info-title {
  width: 30%;
  text-align: right;
}

.basic-info-container,
.additional-info-container {
  flex: 1;
  margin: 0 20px;
}

.basic-info-item,
.additional-info-item {
  display: flex;
  flex-direction: column;
}

.basic-info-container input,
.additional-info-container input {
  width: 70%;
  margin: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #dddddd2a;
  color: gray;
}

.additional-info-container select {
  width: 70%;
  margin: 10px;
  padding: 11px;
  border: 1px solid #ddd;
  border-radius: 4px;
}



.additional-info-button {
  display: flex;
  flex-direction: row;
  justify-content: end;
  gap: 5px;
}

.edit-button {
  /* margin-top: 10px; */
  padding: 8px 10px;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}

.cancel-button {
  background-color: rgb(180, 178, 178);
}

/* .profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.profile-image-container {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 15px;
}

.profile-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-overlay:hover {
  opacity: 1;
  cursor: pointer;
}

.image-overlay i {
  color: white;
  font-size: 24px;
} */

</style>