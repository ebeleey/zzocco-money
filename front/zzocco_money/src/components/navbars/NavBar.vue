<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #331C11"> <!-- bg-dark로 배경을 검정색으로, navbar-dark로 글씨를 흰색으로 설정 -->
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
          <!-- 로고는 왼쪽에 기본적으로 위치합니다. -->
          <RouterLink :to="{name: 'home'}" class="nav-link"><img src="../../assets/logo_white.png" alt="미낭;러ㅣㅁㄴ아러"></RouterLink>
          
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0"> <!-- ms-auto 클래스를 사용하여 오른쪽으로 정렬 -->
            <li class="nav-item">
              <a class="nav-link text-white active" aria-current="page" href="#">금융 상품 비교</a> <!-- text-white로 글씨 색상 변경 -->
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'currency-converter' }" class="nav-link">환율 계산기</RouterLink>
            </li>
            <li class="nav-item">
              <a class="nav-link text-white disabled" href="#" tabindex="-1" aria-disabled="true">근처 은행 찾기</a> <!-- text-white로 글씨 색상 변경 -->
            </li>
						<li class="nav-item">
              <a class="nav-link text-white active" aria-current="page" href="#">커뮤니티</a> <!-- text-white로 글씨 색상 변경 -->
            </li>
						<li class="nav-item">
              <RouterLink :to="{ name: 'profile' }" class="nav-link">마이페이지</RouterLink>
            </li>
						<li class="nav-item">
              <RouterLink :to="{ name: 'signup' }" class="nav-link">회원가입</RouterLink>
            </li>
						<li class="nav-item">
              <RouterLink :to="{ name: 'login' }" class="nav-link">로그인</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
</script>

<style scoped>
.nav-link {
  color: white; /* 부모 요소의 색상 상속 */
  text-decoration: none; /* 밑줄 제거 */
  font-size: inherit; /* 폰트 크기 상속 */
  cursor: pointer; /* 마우스 포인터 설정 */
}
<style scoped>
/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #8B4513; /* 갈색 */
  border-bottom: 1px solid #6D3510; /* 어두운 갈색 테두리 */
}
.nav-links {
  list-style: none;
  display: flex;
  gap: 15px;
}
.nav-links .nav-link {
  text-decoration: none;
  color: #fff; /* 글자 색상을 흰색으로 설정 */
  font-size: inherit;
}
.nav-links .nav-link:hover {
  color: #FFD700; /* 호버 시 글자 색상을 금색으로 변경 */
}

img {
  height: 4rem;
  width: 8rem;
}
</style>


