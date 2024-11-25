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
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import { RouterLink, RouterView } from 'vue-router';
import axios from 'axios'

const store = useAccountStore();
const user = store.user

const fileInput = ref(null);
const profileImagePreview = ref(null);
const newProfileImage = ref(null);

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