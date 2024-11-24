<template>
  <div class="article-page">
    <h1 class="page-title">게시판</h1>
    <!-- 탭 버튼 -->
    <ul class="nav justify-content-center">
      <li class="nav-item">
        <a 
          class="nav-link" 
          :class="{ active: selectedTab === '전체게시판' }" 
          href="#" 
          @click.prevent="selectTab('전체게시판')"
        >
          전체게시판
        </a>
      </li>
      <li class="nav-item">
        <a 
          class="nav-link" 
          :class="{ active: selectedTab === '금융꿀팁' }" 
          href="#" 
          @click.prevent="selectTab('금융꿀팁')"
        >
          금융꿀팁
        </a>
      </li>
      <li class="nav-item">
        <a 
          class="nav-link" 
          :class="{ active: selectedTab === '자유게시판' }" 
          href="#" 
          @click.prevent="selectTab('자유게시판')"
        >
          자유게시판
        </a>
      </li>
    </ul>
    <hr>

    <!-- 게시글 목록 -->
    <div v-if="isLoading"></div>

    <p v-else-if="!articles.length" style="text-align: center;">아직 작성된 게시글이 없습니다.</p>
    
    <ul v-else class="article-list">
      <li v-for="(article, index) in paginatedArticles" :key="index" class="article-item">
        <div class="article-category">
          {{ article.board_name }}
        </div>  
        <div class="article-content">
          <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="article-title">
              {{ article.title }}
          </RouterLink>
          <p class="article-meta">
            <!-- <img :src="article.profile_image" alt="프로필 이미지" class="profile-img" /> -->
            {{ article.user.username }} &nbsp |  &nbsp
            {{ formatDate(article.created_at) }}
          </p>
          
        </div>
        <div class="article-stats">
          <!-- <span>🤎 {{ article.likes }}</span> -->
          <!-- <span>💬 {{ comments.length }}</span> -->
        </div>
      </li>
    </ul>

    <div style="justify-content: flex-end; display: flex;">
      <button style="margin-top: 20px; padding: 12px;">
        <RouterLink to="articles/post/" style="text-decoration: none; color: white;">게시글 작성하기</RouterLink>
      </button>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button 
        v-for="page in totalPages" 
        :key="page" 
        :class="{ active: currentPage === page }" 
        @click="changePage(page)"
      >
        {{ page }}
      </button>
    </div>
    <!-- 검색 바 -->
    <form class="search-bar" @submit.prevent="handleSearch" role="search">
      <input 
        v-model="searchInput" 
        class="form-control me-2" 
        type="search" 
        placeholder="검색어를 입력하세요" 
        aria-label="Search"
      />
      <button class="btn btn-outline-success" type="submit">검색</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCommunityStore } from '@/stores/community';
import { storeToRefs } from 'pinia';

const communityStore = useCommunityStore();
const { articles } = storeToRefs(communityStore);
const isLoading = ref(true);
const selectedTab = ref("전체게시판");
const currentPage = ref(1);
const articlesPerPage = 10;

// 검색어 관련 변수 분리
const searchInput = ref(''); // 입력 중인 검색어
const searchQuery = ref(''); // 실제 검색에 사용될 검색어

// 검색 처리 함수 수정
const handleSearch = () => {
  searchQuery.value = searchInput.value; // 검색 버튼 클릭 시 searchQuery 업데이트
  currentPage.value = 1; // 페이지 초기화
};

// 필터링된 게시글 computed 속성
const filteredArticles = computed(() => {
  if (!articles.value) return [];
  let filtered = articles.value;
  
  // 탭 필터링
  if (selectedTab.value !== "전체게시판") {
    filtered = filtered.filter(article => article.board_name === selectedTab.value);
  }
  
  // 검색어 필터링 (searchQuery 사용)
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(article => 
      article.title.toLowerCase().includes(query) ||
      article.user.username.toLowerCase().includes(query)
    );
  }
  
  // 최신순 정렬 (created_at 기준 내림차순)
  filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  
  return filtered;
});

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  try {
    await loadArticles();
    
  } catch (error) {
    console.error('Failed to load articles:', error);
  }
});

// 데이터 로드 함수
const loadArticles = async () => {
  isLoading.value = true;
  try {
    await communityStore.getArticles();
  } catch (error) {
    console.error('Error loading articles:', error);
  } finally {
    isLoading.value = false;
  }
};

// 탭 변경 시 데이터 다시 로드
const selectTab = async (tab) => {
  selectedTab.value = tab;
  currentPage.value = 1;
  await loadArticles();
};

// 페이지네이션 관련 computed 속성
const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / articlesPerPage);
});

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage;
  const end = start + articlesPerPage;
  return filteredArticles.value.slice(start, end);
});

// 페이지 변경 함수
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    window.scrollTo(0, 0);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};
</script>
  
<style lang="scss" scoped>
.article-page {
  width: 60%;
}

.search-bar {
  display: flex;
  justify-content: center; /* 가로 방향 가운데 정렬 */
  align-items: center;    /* 세로 방향 가운데 정렬 */
  gap: 10px;              /* 입력창과 버튼 사이 간격 */
  margin-bottom: 20px;
}

.search-bar .form-control {
  width: 300px;           /* 검색 입력창 너비 */
}

.search-bar .btn {
  white-space: nowrap;    /* 버튼 텍스트 줄바꿈 방지 */
  background-color: #3f2411;
  border: white;
  color: white;
}
.pagination {
  display: flex;
  justify-content: center;
  margin: 20px 0;
  color: white;

}

.pagination button {
  padding: 8px 12px;
  margin: 0 5px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

.pagination button.active {
  background-color: #3f2411;
  font-weight: bold;
}

.pagination button:hover {
  background-color: #3f2411;
}

/* 게시글 목록 전체 스타일 */
.article-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* 개별 게시글 아이템 스타일 */
.article-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  border-bottom: 1px solid #eaeaea;
  gap: 16px;
}

/* 카테고리 영역 */
.article-category {
  flex-shrink: 0;
  text-align: center;
  width: 12%;
  margin: auto;
  padding: 6px;
  border-radius: 4px;
  font-size: 16px;
  color: #3f2411;
}

/* 게시글 내용 영역 */
.article-content {
  flex-grow: 1;
}

/* 게시글 제목 */
.article-title {
  display: block;
  font-size: 17px;
  font-weight: bolder;
  color: #333;
  text-decoration: none;
  margin-bottom: 4px;
}

.article-title:hover {
  color: #c43d3d;
}

/* 메타 정보 (작성자, 작성일) */
.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* 프로필 이미지 */
.profile-img {
  width: 24px;
  height: 24px;
  border-radius: 100%;
  object-fit: contain;
}

/* 통계 영역 (좋아요, 댓글) */
.article-stats {
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: #666;
}

.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}
.page-title {
  text-align: center;
  margin-top: 70px; 
  margin-bottom: 50px; 
  font-weight: bold;
}

.nav-link {
  color: black;
  font-size: 18px;
  cursor: pointer;

&.active {
  font-weight: bold;
  text-decoration: underline;
}
}

hr {
  margin: 0 auto;
  // width: 1000px;
  height: 3px;
  background-color: #3f2411;
  margin-bottom: 30px;
}
</style>
