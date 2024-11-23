<template>
    <div class="post-create-container">
      <h1>게시글 작성</h1>
      <form @submit.prevent="submitPost">
        <div class="dropdown" style="margin: 40px 0 20px;">
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                {{ board_name || '게시판을 선택해주세요' }}
            </button>
            <ul class="dropdown-menu">
                <li class="dropdown-item" @click="selectBoard(board_name)" v-for="board_name in categories" :key="board_name">
                    {{ board_name }}
                </li>
            </ul>
        </div>
        <div class="form-group">
          <label for="title">제목</label>
          <input
            type="text"
            id="title"
            v-model="title"
            placeholder="게시글 제목을 입력하세요"
            class="form-control"
          />
        </div>
  
        <div class="form-group">
          <label for="content">내용</label>
          <textarea
            id="content"
            v-model="content"
            placeholder="게시글 내용을 입력하세요"
            rows="6"
            class="form-control"
          ></textarea>
        </div>
        

  
        <div v-if="error" class="error-message">
          <p>{{ error }}</p>
        </div>
  
        <button type="submit" class="btn btn-primary">작성 완료</button>
      </form>
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
    if (!title.value || !content.value) {
        error.value = '제목과 내용을 모두 작성해 주세요.'
        return
    }
    axios({
        method: 'post',
        url: `http://127.0.0.1:8000/articles/`,
        data: {
            title: title.value,
            content: content.value,
            board_name: board_name.value,
            board_id: board_name.value === '자유게시판' ? 1 : 2
        },
        headers: {
            Authorization: `Token ${account.token}`
        }
    })
    .then(res => {
        console.log(res)
        community.getArticles()
        router.push('/community')
    })
    .catch(err => {
        if (confirm("로그인이 필요합니다. 로그인 하시겠습니까?")) {
            router.push("/login")
        }
    })
}
</script>
  
<style scoped>
.post-create-container {
max-width: 600px;
margin: 0 auto;
padding: 2rem;
border: 1px solid #ddd;
border-radius: 8px;
background-color: #f9f9f9;
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
padding: 0.5rem;
border: 1px solid #ccc;
border-radius: 4px;
}

button {
	background-color: #3f2411; /* 버튼 기본 배경색 */
	border-color: #3f2411; /* 버튼 기본 테두리 색상 */
	color: white; /* 텍스트 색상 */
	padding: 10px 20px; /* 드롭다운 버튼과 동일한 패딩 */
	font-size: 16px; /* 드롭다운 버튼과 동일한 글꼴 크기 */
	border-radius: 4px; /* 버튼의 모서리를 동일하게 둥글림 */
	height: auto; /* 높이를 자동으로 조정 */
	transition: background-color 0.3s ease, color 0.3s ease;
}

button:hover {
	background-color: rgba(228, 217, 211, 0.829); /* hover 상태의 배경색 */
	color: #3f2411; /* hover 상태의 텍스트 색상 */
	border-color: rgba(228, 217, 211, 0.829);
}
button:focus {
	background-color: rgba(228, 217, 211, 0.829); /* 클릭 후 포커스 상태의 배경색 */
	color: #3f2411; /* 포커스 상태의 텍스트 색상 */
	border-color: rgba(228, 217, 211, 0.829); /* 포커스 상태의 테두리 색상 */
	outline: none; /* 포커스 테두리 제거 */
}

.error-message {
color: red;
font-size: 0.875rem;
margin-top: 1rem;
}
</style>
  