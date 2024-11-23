<template>
	<h1 class="page-title">게시판</h1>
    <div class="detail-page">
      <div v-if="isLoading" class="loading">Loading...</div>
      <div v-else-if="!currentArticle" class="error-message">게시글을 찾을 수 없습니다.</div>
      <div v-else>
        <!-- 게시글 상세 정보 -->
        <div class="article-details">
          <h2 class="article-title">{{ currentArticle.title }}</h2>
		  <br>
          <p class="article-meta">
            작성자: {{ currentArticle.user.username }} &nbsp|&nbsp 
            작성일: {{ formatDate(currentArticle.created_at) }}
          </p>
          <p class="article-content">{{ currentArticle.content }}</p>
        </div>
  
        <hr />
  
        <!-- 댓글 섹션 -->
        <div class="comments-section">
          <h6>댓글 ({{ comments.length }})</h6>
			<br>
          
		  <ul class="comments-list">
			<li v-for="(comment, index) in [...comments].reverse()" :key="index" class="comment-item">
				<p class="comment-author">{{ comment.user.username }}</p>
				<p class="comment-content">{{ comment.content }}</p>
				<p class="comment-meta"></p>
                작성일: {{ formatDate(comment.created_at) }}
			</li>
		</ul>

          <!-- 댓글 작성 -->
          <form @submit.prevent="submitComment" class="comment-form">
            <textarea
              v-model="newComment"
              placeholder="댓글을 입력하세요"
              class="form-control"
              rows="3"
            ></textarea>
            <button class="btn btn-primary" :disabled="!newComment">댓글 작성</button>
          </form>
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
    const articleId = route.params.id;
    await communityStore.getArticle(articleId);
    await communityStore.getComments(articleId);
    isLoading.value = false;
  } catch (error) {
    console.error("Failed to load article or comments:", error);
    isLoading.value = false;
  }
});
  
  // 댓글 작성
  // 댓글 작성
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
  
  
  // 날짜 포맷 함수
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  </script>
  
  <style scoped>
h2 {
	text-align: left;
  font-family: Pretendard-Regular;
}
  .detail-page {
    margin: 20px auto;
    max-width: 800px;
  }
  
  .article-details {
    margin-bottom: 30px;
  }
  
  .article-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .article-meta {
    color: #666;
    font-size: 14px;
    margin-bottom: 20px;
  }
  
  .article-content {
    font-size: 16px;
    line-height: 1.6;
  }
  
  .comments-section {
    margin-top: 30px;
  }
  
  .comments-list {
    list-style: none;
    padding: 0;
  }
  
  .comment-item {
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
  }
  
  .comment-author {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .comment-content {
    margin-bottom: 5px;
  }
  
  .comment-meta {
    color: #666;
    font-size: 12px;
  }
  
  .comment-form {
    margin-top: 20px;
  }
  
  .comment-form textarea {
    margin-bottom: 10px;
  }
  
  .comment-form button {
    background-color: #3f2411;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
  }
  
  .comment-form button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  