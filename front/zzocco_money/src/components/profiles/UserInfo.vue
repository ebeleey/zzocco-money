<template>
  <div class="info-page">
    <div class="profile-section">
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
    </div>

    <div class="info-section">
      <h2>기본 정보</h2>
      <div class="info-grid">
        <div class="info-item">
          <label>이름</label>
          <input type="text" :value="user.name" readonly>
        </div>
        <div class="info-item">
          <label>아이디</label>
          <input type="text" :value="user.username" readonly>
        </div>
        <div class="info-item">
          <label>이메일</label>
          <input type="text" :value="user.email" readonly>
        </div>
      </div>
    </div>

    <div class="additional-info" v-if="!editMode">
      <h2>추가 정보</h2>
      <div class="info-grid">
        <div class="info-item">
          <label>혼인 여부</label>
          <input type="text" :value="getChoiceLabel(user.marriage, MARRIAGE_CHOICES)" readonly />
        </div>
        <div class="info-item">
          <label>수입 전망</label>
          <input type="text" :value="getChoiceLabel(user.income_prospect, INCOME_PROSPECT_CHOICES)" readonly />
        </div>
        <div class="info-item">
          <label>총 자산 규모</label>
          <input type="text" :value="getChoiceLabel(user.asset_level, ASSET_LEVEL_CHOICES)" readonly />
        </div>
        <div class="info-item">
          <label>연 평균 소득</label>
          <input type="text" :value="getChoiceLabel(user.income_level, INCOME_LEVEL_CHOICES)" readonly />
        </div>
      </div>
      <button @click="enterEditMode" class="edit-button">회원정보 수정</button>
    </div>
    <div v-else>
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

    <div>
      <RouterLink  :to="{name: 'passwordChange'}"><button>비밀번호 변경</button></RouterLink>
    </div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import { RouterLink, RouterView } from 'vue-router';
import axios from 'axios'

import defaultProfileImage from '@/assets/default_image.png';


const store = useAccountStore();
const user = ref(store.user)

const editMode = ref(false);
const passwordVerified = ref(false);
const password = ref('');
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

// 정보 수정 요청
// const submitUpdate = async () => {
//   try {
//     const response = await axios.put('/api/update-user', { ...editData.value });
//     if (response.data.success) {
//       Object.assign(user.value, editData.value);
//       editMode.value = false;
//       passwordVerified.value = false;
//       alert('회원정보가 성공적으로 업데이트되었습니다.');
//     }
//   } catch (error) {
//     console.error(error);
//   }
// };

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

// 로컬 상태
const fileInput = ref(null);
const profileImagePreview = ref(null);
const newProfileImage = ref(null);

// 파일 선택 핸들러
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (!file) return alert('파일을 선택해주세요.');

  newProfileImage.value = file;
  const reader = new FileReader();
  reader.onload = (e) => (profileImagePreview.value = e.target.result);
  reader.readAsDataURL(file);
};

// 프로필 이미지 업로드 핸들러
const uploadProfileImage = async () => {
  if (!newProfileImage.value) return alert('업로드할 이미지를 선택해주세요.');

  const formData = new FormData();
  formData.append('profile_image', newProfileImage.value);

  try {
    const { data } = await axios.post(
      'http://127.0.0.1:8000/accounts/update-profile-image/',
      formData,
      {
        headers: {
          Authorization: `Token ${store.token}`,
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    // 상태 업데이트
    if (data.imageUrl) {
      const updatedUrl = data.imageUrl.startsWith('http')
        ? data.imageUrl
        : `http://127.0.0.1:8000${data.imageUrl}`;
      store.updateUser({ ...store.user, profile_image: updatedUrl });
      profileImagePreview.value = updatedUrl;
      newProfileImage.value = null;
      alert('프로필 사진이 성공적으로 업데이트되었습니다.');
    } else {
      throw new Error('응답에 이미지 URL이 포함되지 않았습니다.');
    }
  } catch (error) {
    console.error('프로필 이미지 업로드 실패:', error);
    alert('업로드 중 오류가 발생했습니다. 다시 시도해주세요.');
  }
};

// 파일 선택 트리거
const triggerFileInput = () => fileInput.value.click();

// 전체 URL 생성기
const getFullImageUrl = (path) => {
  if (!path) return '/default-profile.png'; // 기본 이미지 경로
  if (path.startsWith('http')) return path;
  return `http://127.0.0.1:8000${path}`;
};

</script>

<<style scoped>
.info-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.profile-section {
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
}

.update-button, .edit-button, .password-change-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.update-button:hover, .edit-button:hover, .password-change-button:hover {
  background-color: #45a049;
}

.info-section, .additional-info {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-weight: bold;
  margin-bottom: 5px;
}

.info-item input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>