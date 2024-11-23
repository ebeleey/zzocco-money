<template>
    <div class="post">
        <!-- 제목과 작성 정보 -->
        <div class="header">
            <h5>{{ article.title }}</h5>
            <!-- {{ article }} -->

            <img class="profile-img" :src="authorImg" alt="프사" />
            <span class="author"> | {{ article.user.username }} | </span>
            <span class="time">time: {{ article.created_at.slice(0, 10) }}</span>
        </div>
    
        <!-- 본문 -->
        <hr>
        <div class="content">
            <p>{{ article.content }}</p>
        </div>
        askdfjsdkvx

        <hr>
        <!-- 좋아요와 댓글 정보 -->
        <div class="actions">
            <button @click="likePost">👍 3</button>
            <span>💬 {{ comments.length }}</span>
        </div>
    
        <!-- 댓글 컴포넌트 -->
        <div class="comment-box">
            <form @submit.prevent="uploadComment">
                <label for="comment"></label>
                <input v-model="newComment" type="text" id="comment">
                <input type="submit">
            </form>
            <hr>
            
            <div v-if="comments.length" v-for="comment in comments">
                {{ comment.user.username }} | {{ comment.created_at }}
                <p>{{ comment.content }}</p>
            
                <hr>
            </div>
            <div v-else style="text-align: center;">
                아직 작성된 댓글이 없습니다.
            </div>

        </div>
    </div>
  </template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';

const route = useRoute()
const router = useRouter()
const account = useAccountStore()
const store = useCommunityStore()
const article = store.articles[route.params.id - 1]
// const comments = ref([])
onMounted(() => {
    store.getComments(route.params.id)
})
const comments = computed(() => store.comments)

const newComment = ref("")
const uploadComment = function () {
    axios({
        method: 'post',
        url: `http://127.0.0.1:8000/articles/${article.id}/comments/create/`,
        data: {
            article: article.id,
            content: newComment.value
        },
        headers: {
            Authorization: `Token ${account.token}`
        }
    }).then(res => {
        console.log(res)
        router.go(0)
    })
    .catch(err => {
        if (confirm("로그인이 필요합니다. 로그인 하시겠습니까?")) {
            router.push("/login")
        }
    })
}

</script>

<style scoped>

</style>