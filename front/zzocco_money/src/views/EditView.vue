<template>
  <div>
    <h1 class="page-title">게시글 수정</h1>
    
    <div class="post-page">
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
        <button type="submit" style="padding: 10px 20px;">수정 완료</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCommunityStore } from '@/stores/community';

const route = useRoute();
const router = useRouter();
const communityStore = useCommunityStore();

const title = ref('');
const content = ref('');
const board_name = ref('');
const error = ref('');

onMounted(async () => {
  try {
    const article = await communityStore.getArticle(route.params.id);
    title.value = article.title;
    content.value = article.content;
    board_name.value = article.board_name; // 게시판 이름 읽기 전용으로 설정
  } catch (err) {
    console.error(err);
    error.value = '게시글 로드 중 오류가 발생했습니다.';
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
    router.push(`/community/${route.params.id}`);
  } catch (err) {
    console.error(err);
    error.value = '게시글 수정 중 오류가 발생했습니다.';
  }
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
