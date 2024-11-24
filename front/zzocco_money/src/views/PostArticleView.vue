<template>
  <div>
    <h1 class="page-title">게시판</h1>
    
    <div class="post-page">
      <div class="post-title">
        <div class="dropdown">
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                {{ board_name || '게시판 선택' }}
            </button>
            <ul class="dropdown-menu">
                <li class="dropdown-item" @click="selectBoard(board_name)" v-for="board_name in categories" :key="board_name">
                    {{ board_name }}
                </li>
            </ul>
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
      <form class="form-content" @submit.prevent="submitPost">
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
        <button type="submit" style="padding: 10px 20px;">작성 완료</button>
      </form>
    </div>
  </div>

</template>
  
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios';
import { useAccountStore } from '@/stores/account';
import { useCommunityStore } from '@/stores/community';

const account = useAccountStore()
const community = useCommunityStore()
const title = ref('')
const content = ref('')
const board_name = ref('')
const error = ref('')
const router = useRouter()

const categories = ['자유게시판', '금융꿀팁']

const selectBoard = (category) => board_name.value = category
const submitPost = async () => {
    // 제목, 내용 확인
    if (!title.value || !content.value) {
        error.value = '제목과 내용을 모두 작성해 주세요.';
        return;
    }
    // 게시판 선택 확인
    if (!board_name.value) {
        error.value = '게시판을 선택해주세요.';
        return;
    }
    // 게시글 작성 요청
    try {
        await axios({
            method: 'post',
            url: `http://127.0.0.1:8000/articles/`,
            data: {
                title: title.value,
                content: content.value,
                board_name: board_name.value,
                board_id: board_name.value === '자유게시판' ? 1 : 2,
            },
            headers: {
                Authorization: `Token ${account.token}`,
            },
        });
        community.getArticles();
        router.push('/community');
    } catch (err) {
        // 로그인 필요 시 처리
        if (err.response && err.response.status === 401) {
            if (confirm("로그인이 필요합니다. 로그인 하시겠습니까?")) {
                router.push("/login");
            }
        } else {
            console.error(err);
            error.value = '게시글 작성 중 문제가 발생했습니다.';
        }
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
  