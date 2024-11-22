<template>
  <div>
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
          :class="{ active: selectedTab === '금융 꿀팁' }" 
          href="#" 
          @click.prevent="selectTab('금융 꿀팁')"
        >
          금융 꿀팁
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
    <ul class="article-list">
      <li v-for="(article, index) in paginatedArticles" :key="index" class="article-item">
        <div class="article-category">
          {{ article.board_name }}
        </div>  
        <div class="article-content">
          <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="article-title">
              {{ article.title }}
          </RouterLink>
          <p class="article-meta">
            <img :src="article.profile_image" alt="프로필 이미지" class="profile-img" />
            작성자: {{ article.author }} &nbsp |  &nbsp
            작성일: {{ article.created_at }}
          </p>
        </div>
        <div class="article-stats">
          <span>🤎 {{ article.likes }}</span>
          <span>💬 {{ article.comments }}</span>
        </div>
      </li>
    </ul>


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
    <form class="search-bar" @submit="handleSearch" role="search">
      <input 
        v-model="searchQuery" 
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
import { ref, computed } from 'vue';
  

// 더미 데이터
const articles = ref([
  { id: 1, title: "Tree whatever participant need bed.", profile_image: "https://via.placeholder.com/50", author: "Linda Fields", created_at: "2024-03-15 08:54", likes: 17, comments: 17, board_name: "금융 꿀팁" },
  { id: 2, title: "Teach energy store.", profile_image: "https://via.placeholder.com/50", author: "Scott Roberts", created_at: "2024-03-28 04:22", likes: 30, comments: 5, board_name: "금융 꿀팁" },
  { id: 3, title: "Woman everything some several heart bag.", profile_image: "https://via.placeholder.com/50", author: "Mark Humphrey", created_at: "2024-02-19 15:45", likes: 33, comments: 9, board_name: "금융 꿀팁" },
  { id: 4, title: "Then big task rest while.", profile_image: "https://via.placeholder.com/50", author: "Crystal Weber", created_at: "2024-03-10 21:30", likes: 22, comments: 7, board_name: "전체게시판" },
  { id: 5, title: "Answer analysis then performance bit everybody.", profile_image: "https://via.placeholder.com/50", author: "Barry Bush", created_at: "2024-02-13 10:21", likes: 23, comments: 20, board_name: "전체게시판" },
  { id: 6, title: "Out choose help chair tough money.", profile_image: "https://via.placeholder.com/50", author: "Mr. Steven Mendez", created_at: "2024-02-17 13:28", likes: 1, comments: 16, board_name: "금융 꿀팁" },
  { id: 7, title: "Certain investment level traditional.", profile_image: "https://via.placeholder.com/50", author: "Taylor Moore", created_at: "2024-04-16 23:01", likes: 48, comments: 20, board_name: "전체게시판" },
  { id: 8, title: "Song against here.", profile_image: "https://via.placeholder.com/50", author: "Alan Li", created_at: "2024-04-21 20:19", likes: 42, comments: 2, board_name: "자유게시판" },
  { id: 9, title: "Somebody no unit.", profile_image: "https://via.placeholder.com/50", author: "Shane Rodriguez", created_at: "2024-10-07 15:33", likes: 19, comments: 19, board_name: "전체게시판" },
  { id: 10, title: "Final trouble paper forget stage table.", profile_image: "https://via.placeholder.com/50", author: "Brian Davis", created_at: "2024-06-10 00:58", likes: 42, comments: 15, board_name: "전체게시판" },
  { id: 11, title: "Ability direction approach receive president condition.", profile_image: "https://via.placeholder.com/50", author: "Kathryn Long", created_at: "2024-02-17 04:08", likes: 20, comments: 14, board_name: "자유게시판" },
  { id: 12, title: "Wait turn hotel mean fact.", profile_image: "https://via.placeholder.com/50", author: "William Cruz", created_at: "2024-02-03 04:52", likes: 40, comments: 5, board_name: "금융 꿀팁" },
  { id: 13, title: "Attorney dark television nor carry find.", profile_image: "https://via.placeholder.com/50", author: "Elizabeth Kaiser", created_at: "2024-11-03 11:34", likes: 25, comments: 16, board_name: "자유게시판" },
  { id: 14, title: "Physical car drug color trip.", profile_image: "https://via.placeholder.com/50", author: "Charles Ellison", created_at: "2024-08-04 12:59", likes: 26, comments: 17, board_name: "전체게시판" },
  { id: 15, title: "Up lot may.", profile_image: "https://via.placeholder.com/50", author: "Brandon Rosales", created_at: "2024-10-15 13:59", likes: 20, comments: 6, board_name: "전체게시판" },
  { id: 16, title: "Eye American bit general maybe mouth.", profile_image: "https://via.placeholder.com/50", author: "Timothy Myers", created_at: "2024-01-31 14:28", likes: 15, comments: 11, board_name: "전체게시판" },
  { id: 17, title: "Budget next offer positive law note.", profile_image: "https://via.placeholder.com/50", author: "Lisa Gallagher", created_at: "2024-08-19 09:44", likes: 30, comments: 7, board_name: "전체게시판" },
  { id: 18, title: "On wide war agency apply.", profile_image: "https://via.placeholder.com/50", author: "James Griffin", created_at: "2024-10-09 06:19", likes: 44, comments: 16, board_name: "금융 꿀팁" },
  { id: 19, title: "Arrive ability sort.", profile_image: "https://via.placeholder.com/50", author: "Kimberly Mckay", created_at: "2024-11-04 14:57", likes: 46, comments: 14, board_name: "전체게시판" },
  { id: 20, title: "Apply system expect cup natural.", profile_image: "https://via.placeholder.com/50", author: "Heather Hernandez", created_at: "2024-07-03 01:39", likes: 41, comments: 8, board_name: "전체게시판" },
  { id: 21, title: "Ask have young.", profile_image: "https://via.placeholder.com/50", author: "Michael Kelly", created_at: "2024-03-22 23:24", likes: 5, comments: 15, board_name: "금융 꿀팁" },
  { id: 22, title: "Feeling note student meeting ten.", profile_image: "https://via.placeholder.com/50", author: "Evan Smith", created_at: "2024-08-29 07:30", likes: 26, comments: 16, board_name: "자유게시판" },
  { id: 23, title: "One sell against.", profile_image: "https://via.placeholder.com/50", author: "Aaron Jackson", created_at: "2024-07-07 19:11", likes: 45, comments: 20, board_name: "전체게시판" },
  { id: 24, title: "Economy west less note serious.", profile_image: "https://via.placeholder.com/50", author: "Frederick Miller", created_at: "2024-04-28 04:33", likes: 47, comments: 17, board_name: "전체게시판" },
  { id: 25, title: "Star Democrat nice way budget.", profile_image: "https://via.placeholder.com/50", author: "Paige Chan", created_at: "2024-10-31 15:14", likes: 18, comments: 16, board_name: "자유게시판" },
  { id: 26, title: "Good eight campaign one.", profile_image: "https://via.placeholder.com/50", author: "Robert Ferguson", created_at: "2024-08-05 11:42", likes: 40, comments: 14, board_name: "전체게시판" },
  { id: 27, title: "Dark house answer national film four.", profile_image: "https://via.placeholder.com/50", author: "Richard Smith", created_at: "2024-05-21 04:59", likes: 24, comments: 6, board_name: "금융 꿀팁" },
  { id: 28, title: "Where really responsibility.", profile_image: "https://via.placeholder.com/50", author: "Christina Garcia", created_at: "2024-04-28 12:46", likes: 47, comments: 19, board_name: "전체게시판" },
  { id: 29, title: "Involve support near activity reason together.", profile_image: "https://via.placeholder.com/50", author: "Sarah Taylor", created_at: "2024-01-19 16:15", likes: 22, comments: 6, board_name: "전체게시판" }
])

const selectedTab = ref("전체게시판");
const currentPage = ref(1); // 현재 페이지
const articlesPerPage = 10; // 페이지당 표시할 게시글 수

// 탭 선택 함수
const selectTab = (tab) => {
  selectedTab.value = tab;
  currentPage.value = 1; // 탭 변경 시 첫 페이지로 이동
};

// 필터링된 게시글
const filteredArticles = computed(() => {
  if (selectedTab.value === "전체게시판") {
    return articles.value;
  }
  return articles.value.filter((article) => article.board_name === selectedTab.value);
});

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / articlesPerPage);
});

// 현재 페이지에 표시할 게시글
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage;
  const end = start + articlesPerPage;
  return filteredArticles.value.slice(start, end);
});

// 페이지 변경 함수
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};
</script>
  
<style lang="scss" scoped>

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
  width: 120px;
  margin: auto;
  padding: 6px 12px;
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
  margin-bottom: 8px;
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
