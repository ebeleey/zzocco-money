<template>
  <div>
    <h1 class="page-title">게시글 수정</h1>
    
    <div class="post-page">
      <div v-if="isLoading" class="loading">Loading...</div>
      <div v-else>
        <div class="post-title">
          <!-- 게시판 선택 (읽기 전용) -->
          <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" disabled>
                  {{ board_name || '게시판 선택' }}
              </button>
          </div>
          <div class="form-title">
            <input
              type="text"
              id="title"
              v-model="title"
              placeholder="제목을 입력하세요"
              class="form-control"
            />
          </div>
        </div>
        <form class="form-content" @submit.prevent="submitEdit">
          <div class="form-group">
            <textarea
              id="content"
              v-model="content"
              placeholder="내용을 입력하세요"
              rows="15"
              class="form-control"
            ></textarea>
          </div>
          <div v-if="error" class="error-message">
            <p>{{ error }}</p>
          </div>
          <div class="button-group">
            <button type="button" class="cancel-button" @click="goBack">취소</button>
            <button type="submit" class="edit-button">수정</button>
          </div>

          
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCommunityStore } from '@/stores/community';
import { storeToRefs } from 'pinia';

const route = useRoute();
const router = useRouter();
const communityStore = useCommunityStore();
const { currentArticle } = storeToRefs(communityStore);

const title = ref('');
const content = ref('');
const board_name = ref('');
const error = ref('');
const isLoading = ref(true);

onMounted(async () => {
  try {
    await communityStore.getArticle(route.params.id);
    
    // currentArticle이 로드된 후 데이터 설정
    if (currentArticle.value) {
      title.value = currentArticle.value.title;
      content.value = currentArticle.value.content;
      board_name.value = currentArticle.value.board_name;
    } else {
      error.value = '게시글을 찾을 수 없습니다.';
    }
  } catch (err) {
    console.error('게시글 로드 에러:', err);
    error.value = '게시글 로드 중 오류가 발생했습니다.';
  } finally {
    isLoading.value = false;
  }
});

const submitEdit = async () => {
  if (!title.value || !content.value) {
    error.value = '제목과 내용을 모두 작성해 주세요.';
    return;
  }

  try {
    await communityStore.updateArticle(route.params.id, {
      title: title.value,
      content: content.value,
    });
    router.push(`/articles/${route.params.id}/`);
  } catch (err) {
    console.error('게시글 수정 에러:', err);
    error.value = '게시글 수정 중 오류가 발생했습니다.';
  }
};

const goBack = () => {
  router.push(`/articles/${route.params.id}`);
};
</script>

<style scoped>
.post-page {
  margin: 20px auto;
  max-width: 60%;
}

.dropdown button {
  font-size: 15px;
  background-color: white;
  border-color: #ccc;
  padding: 0.57rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: black;
}

.form-title {
  flex: 1;
}

.post-title {
  display: flex;
  gap: 5px;
}

.form-content {
  margin: 20px 0;
  text-align: center;
}

h1 {
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
}

.button-group {
  display: flex;
  justify-content: center;
}

.edit-button,
.cancel-button {
  margin-left: 10px;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button {
  background-color: #857c75;
}

input,
textarea {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: black;
}

.error-message {
  color: red;
  font-size: 0.875rem;
  margin-top: 1rem;
}
</style>
