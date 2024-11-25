<template>
	<div class="info-page">
    <div class="profile-image-info">
      <div class="profile-image">
        <!-- 이미지가 없을 경우 기본 이미지를 보여주도록 수정 -->
        <img 
          :src="getFullImageUrl(profileImagePreview || user.profile_image)" 
          alt="Profile Image" 
        />
        <input 
          type="file" 
          @change="onFileChange" 
          accept="image/*" 
          ref="fileInput" 
          style="display:none"
        >
        <button @click="triggerFileInput">프로필 사진 변경</button>
      </div>
      <button 
        @click="uploadProfileImage" 
        v-if="newProfileImage"
      >프로필 사진 저장</button>
    </div>
		<div class="basic-info">
			<div class="basic-info-item">
				<label for="">이름</label>
				<input type="text" :value="user.name" readonly>
			</div>

			<div class="basic-info-item">
				<label for="">아이디</label>
				<input type="text" :value="user.username" readonly>
			</div>

			<div class="basic-info-item">
				<label for="">이메일</label>
				<input type="text" :value="user.email" readonly>
			</div>
		</div>

    <div v-if="!editMode">
      <div class="basic-info-item">
        <label>혼인 여부</label>
        <input type="text" :value="getChoiceLabel(user.marriage, MARRIAGE_CHOICES)" readonly />
      </div>
      <div class="basic-info-item">
        <label>수입 전망</label>
        <input type="text" :value="getChoiceLabel(user.income_prospect, INCOME_PROSPECT_CHOICES)" readonly />
      </div>
      <div class="basic-info-item">
        <label>총 자산 규모</label>
        <input type="text" :value="getChoiceLabel(user.asset_level, ASSET_LEVEL_CHOICES)" readonly />
      </div>
      <div class="basic-info-item">
        <label>연 평균 소득</label>
        <input type="text" :value="getChoiceLabel(user.income_level, INCOME_LEVEL_CHOICES)" readonly />
      </div>
      <button @click="enterEditMode">회원정보 수정</button>
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


const store = useAccountStore();
const user = ref(store.user)

const fileInput = ref(null);
const profileImagePreview = ref(null);
const newProfileImage = ref(null);

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
const submitUpdate = async () => {
  try {
    const response = await axios.put('/api/update-user', { ...editData.value });
    if (response.data.success) {
      Object.assign(user.value, editData.value);
      editMode.value = false;
      passwordVerified.value = false;
      alert('회원정보가 성공적으로 업데이트되었습니다.');
    }
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

onMounted(() => {
	console.log(user)
	console.log(user.profile_image)
  if (user && user.profile_image) {
    profileImagePreview.value = user.profile_image;
  }
});
// 전체 이미지 URL을 생성하는 함수
const getFullImageUrl = (path) => {
  if (!path) return '../assets/default_image.png'; // 기본 이미지
  if (path.startsWith('http')) return path; // 이미 전체 URL인 경우
  // 백엔드 서버의 기본 URL을 추가
  return `http://127.0.0.1:8000${path}`;
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const onFileChange = (event) => {
  const file = event.target.files[0];
	console.log(file)
  if (file) {
    newProfileImage.value = file;
    const reader = new FileReader();
    reader.onload = e => {
      profileImagePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const uploadProfileImage = async () => {
  if (newProfileImage.value) {
    const formData = new FormData();
    formData.append('profile_image', newProfileImage.value);

    try {
      const response = await axios.post('http://127.0.0.1:8000/accounts/update-profile-image/', formData, {
        headers: {
          Authorization: `Token ${store.token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data.message) {
        // ref로 감싼 user 객체 업데이트
        user.profile_image = response.data.imageUrl;
        // 프리뷰도 업데이트
        profileImagePreview.value = response.data.imageUrl;
        
        alert('프로필 사진이 성공적으로 업데이트되었습니다.');
      }
    } catch (error) {
      console.error('프로필 이미지 업로드 실패:', error);
      alert('프로필 사진 업로드에 실패했습니다.');
    }
  }
};
</script>

<style scoped>
.info-page {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.basic-info {
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.basic-info-item {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	gap: 10px;
}

.basic-info-item label {
	display: flex;
	align-items: center;
}

.basic-info-item input {
	padding: 8px;
	border-radius: 4px;
  border: 1px solid #ccc;
  border-radius: 4px;
	color: #666;
} 

</style>