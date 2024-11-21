<template>
    <div>
        <h1 class="page-title">게시판</h1>
        <!-- 탭 버튼 -->
        <ul class="nav justify-content-center">
            <li class="nav-item">
                <a class="nav-link active" href="#">전체</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">금융 꿀팁</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">인증게시판</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">자유게시판</a>
            </li>
        </ul>
        <hr>
    </div>
</template>

<script setup>

</script>

<style lang="scss" scoped>
.page-title {
  text-align: center;
  margin-top: 70px; 
  margin-bottom: 50px; 
  font-weight: bold;
}

.nav-link {
//   font-size:large;
  color: black;
}

hr {
  margin: 0 auto;
  width: 50%;
  color: #3f2411;
}
</style>