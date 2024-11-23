import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRoute } from 'vue-router';

export const useCommunityStore = defineStore('community', () => {
  const articles = ref([]);
  const comments = ref([]);
  const currentArticle = ref(null);

  const route = useRoute();

  // 게시글 조회
  const getArticle = async (articleId) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/articles/${articleId}/`);
      currentArticle.value = response.data;
    } catch (error) {
      console.error('게시글 조회 중 오류 발생:', error);
      throw error;
    }
  };

  // 게시글 목록 조회
  const getArticles = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/articles/');
      articles.value = response.data;
    } catch (error) {
      console.error('게시글 목록 조회 중 오류 발생:', error);
      throw error;
    }
  };

  // 댓글 목록 조회
  const getComments = async (articleId) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/articles/${articleId}/comments/`);
      comments.value = response.data;
    } catch (error) {
      console.error('댓글 조회 중 오류 발생:', error);
      throw error;
    }
  };

  // 댓글 추가
  const addComment = async (articleId, content) => {
    try {
      const response = await axios.post(`http://127.0.0.1:8000/articles/${articleId}/comments/create/`, {
        content: content,
      });
      return response; // 작성된 댓글 반환
    } catch (error) {
      console.error('댓글 작성 중 오류 발생:', error);
      throw error;
    }
  };

  // 데이터 로드 (게시글 + 댓글)
  const loadArticle = async () => {
    const articleId = currentArticle.id
    if (articleId) {
      await Promise.all([getArticle(articleId), getComments(articleId)]);
    }
  };

  const createComment = async ({ content, article, token }) => {
    const response = await axios.post(`http://127.0.0.1:8000/articles/${article}/comments/create/`,
      
      { content, article },
      {
        headers: {
          'Authorization': `Token ${token}`
        }
      }
    );
    return response.data;
  }

  return {
    articles,
    comments,
    currentArticle,
    getArticles,
    getArticle,
    getComments,
    addComment, // 추가된 댓글 작성 함수
    loadArticle,
    createComment
  };
});
