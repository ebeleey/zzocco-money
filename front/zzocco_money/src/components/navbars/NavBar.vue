<template>
  <div>
    <nav class="navbar navbar-expand-md navbar-dark"> <!-- bg-dark로 배경을 검정색으로, navbar-dark로 글씨를 흰색으로 설정 -->
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggler" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarToggler">
          <!-- 로고는 왼쪽에 기본적으로 위치합니다. -->
          <RouterLink :to="{name: 'home'}" class="nav-link"><img src="../../assets/logo_wave.png" alt="logo"></RouterLink>

          
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


/* Navbar */
.navbar {
  font-size: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;

}

img {
  height: 4rem;
  width: 8rem;
}
</style>


