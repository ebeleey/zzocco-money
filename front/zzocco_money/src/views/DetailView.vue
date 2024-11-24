<template>
  <div>
    <h1 class="page-title">게시판</h1>

    <div class="detail-page">
      <div v-if="isLoading" class="loading">Loading...</div>
      <div v-else-if="!currentArticle" class="error-message">게시글을 찾을 수 없습니다.</div>
      <div v-else>

        <div class="article-details">
          <h2 class="article-title">
            <span>[{{currentArticle.board_name}}]</span> {{ currentArticle.title }}
          </h2>
          <br>
          <p class="article-meta">
            작성자: {{ currentArticle.user.username }} &nbsp|&nbsp 
            작성일: {{ formatDate(currentArticle.created_at) }}
          </p>
        </div>
        <div class="article-actions" v-if="currentArticle.user.username === store.user.username">
          <button @click="editArticle" class="edit-button">수정 ✏️ </button>
          <button @click="deleteArticle" class="delete-button">삭제 ❌</button>
        </div>
        <hr>
        <br>
        <p class="article-content">{{ currentArticle.content }}</p>  
        <br>
        <!-- <hr> -->

        <div class="comments-section">
          <p class="comments-count">🗨️ 댓글 {{ comments.length }}</p>
          <ul class="comments-list">
            <li v-if="comments.length === 0" class="no-comments-message">
              아직 작성된 댓글이 없습니다.
            </li>
            <li v-else v-for="(comment, index) in comments" :key="index" class="comment-item">
              <p class="comment-author">{{ comment.user.username }}</p>
              <p class="comment-content">{{ comment.content }}</p>
              <p class="comment-meta">{{ formatDate(comment.created_at) }}</p>
            </li>
          </ul>
          <!-- 댓글 작성 -->
          <form @submit.prevent="submitComment" class="comment-form">
            <textarea
              v-model="newComment"
              placeholder="댓글을 입력하세요"
              class="form-control"
              rows="2"
            ></textarea>
            <button class="btn btn-primary" :disabled="!newComment">댓글 작성</button>
          </form>
          </div>
        </div>
      </div>
    </div>
	
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useAccountStore } from "@/stores/account";
  import { useCommunityStore } from "@/stores/community";
  import { storeToRefs } from "pinia";
  
  import { useRoute } from "vue-router";

  const route = useRoute()

  const store = useAccountStore()
  const communityStore = useCommunityStore();
  const { currentArticle, comments } = storeToRefs(communityStore);
  
  const isLoading = ref(true);
  const newComment = ref("");
  
  onMounted(async () => {
  try {
    await store.fetchUser();
    const user = store.user
    const articleId = route.params.id;
    await communityStore.getArticle(articleId);
    await communityStore.getComments(articleId);

    console.log("user", user)
    isLoading.value = false;
  } catch (error) {
    console.error("Failed to load article or comments:", error);
    isLoading.value = false;
  }
});
  
const submitComment = async () => {
  if (!newComment.value.trim()) return;
  try {
    const response = await communityStore.createComment({
      content: newComment.value,
      article: currentArticle.value.id,
	  token: store.token
    });

    // 새 댓글을 comments 배열에 추가
    comments.value.push(response);

    // 입력 필드 초기화
    newComment.value = "";
  } catch (error) {
    console.error("Failed to submit comment:", error);
    // 여기에 에러 처리 로직을 추가할 수 있습니다 (예: 사용자에게 알림)
  }
};

const editArticle = () => {
  router.push({ name: 'EditView', params: { id: currentArticle.value.id } });
};
  

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};
</script>

<style scoped>
hr {
  margin: 0 auto;
  height: 3px;
  background-color: #3f2411;
  margin-bottom: 30px;
}

h2 {
text-align: left;
font-family: 'Pretendard-Regular';
}

.article-actions {
  text-algin: right;
}

.article-actions button {
  background-color: white;
  color: #5f5858;
}



.detail-page {
  margin: 20px auto;
  max-width: 60%;
}

.article-details {
  padding: 0 10px;
}


.article-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;

}

.article-title span {
  color: #3f2411;
}

.article-meta {
  color: #666;
  font-size: 14px;
  text-align: right;
  margin-bottom: 5px;
}

.article-content {
  font-size: 16px;
  line-height: 1.6;
}

.comments-section {
  margin-top: 30px;
  background-color: #cabcb38a;
  padding: 20px;
  border-radius: 20px;
}

.comments-count {
  font-size: 14px;
}

.comments-list {
  list-style: none;
  padding: 10px;
}

.comment-item {
  margin-bottom: 20px;
  border-bottom: 1px solid #3f241144;
  padding-bottom: 0px;
}

.comment-author {
  font-weight: bold;
  margin-bottom: 5px;
}

.comment-content {
  margin-bottom: 5px;
}

.comment-meta {
  color: #3f241191;
  font-size: 12px;
}

.comment-form {
  margin: 5px;
  display: flex;
  height: 60px;
}

.comment-form textarea {
  font-size: 15px;
}

.comment-form button {
  background-color: #3f2411;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  width: 100px;
  margin: 0 10px;
  font-size: 14px;
}

.comment-form button:disabled {
  background-color: #968d84;
  cursor: not-allowed;
}

.no-comments-message {
  color: #968d84;
  font-size: 14px;
  padding: 0 10px;;
}
</style>
