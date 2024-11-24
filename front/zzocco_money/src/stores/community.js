import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useAccountStore } from './account';

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

  const updateArticle = async (articleId, updatedData) => {
    try {
      const response = await axios.put(`http://127.0.0.1:8000/articles/${articleId}/`, updatedData, {
        headers: {
          Authorization: `Token ${useAccountStore().token}`,
        },
      });
    } catch (error) {
      console.error("Error updating article:", error.response?.data || error.message);
      throw error;
    }
  }

  const deleteArticle = async (articleId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${useAccountStore().token}`,
        },
      });
      // 삭제 후 articles 배열에서도 해당 게시글 제거
      articles.value = articles.value.filter(article => article.id !== articleId);
    } catch (error) {
      console.error('게시글 삭제 중 오류 발생:', error);
      throw error;
    }
  };

  // 댓글 수정
  const updateComment = async (articleId, commentId, content) => {
    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/articles/comments/${commentId}/`,
        { content },
        {
          headers: {
            Authorization: `Token ${useAccountStore().token}`,
          },
        }
      );
      
      // 댓글 배열 업데이트
      const index = comments.value.findIndex(comment => comment.id === commentId);
      if (index !== -1) {
        comments.value[index] = response.data;
      }
      
      return response.data;
    } catch (error) {
      console.error('댓글 수정 중 오류 발생:', error);
      throw error;
    }
  };

  // 댓글 삭제
  const deleteComment = async (articleId, commentId) => {
    try {
      await axios.delete(
        `http://127.0.0.1:8000/articles/comments/${commentId}/`,
        {
          headers: {
            Authorization: `Token ${useAccountStore().token}`,
          },
        }
      );
      
      // 댓글 배열에서 삭제된 댓글 제거
      comments.value = comments.value.filter(comment => comment.id !== commentId);
    } catch (error) {
      console.error('댓글 삭제 중 오류 발생:', error);
      throw error;
    }
  };
  

  return {
    articles,
    comments,
    currentArticle,
    getArticles,
    getArticle,
    getComments,
    addComment, // 추가된 댓글 작성 함수
    loadArticle,
    createComment,
    updateArticle,
    deleteArticle,
    updateComment,
    deleteComment,
  };
});
