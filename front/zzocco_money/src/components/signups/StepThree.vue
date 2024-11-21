<template>
	<div>
		<h2>가입한 금융 상품 입력</h2>
		<form>
			<div>
				<label>금융 상품</label>
				<input
					v-model="formData.financialInfo.selectedProducts"
					type="text"
					placeholder="가입한 금융 상품을 입력하세요"
				/>
			</div>
		</form>
        <br>
        <div class="button-container">
            <!-- '이전' 버튼 추가 -->
            <button @click="$emit('previous-step')">이전</button>
    
            <!-- '회원가입 완료' 버튼 -->
            <button @click="$emit('submit')">회원가입 완료</button>
        </div>

		

	</div>
</template>
  
  <script>
  export default {
    props: ["formData"], // 부모로부터 데이터를 전달받음
  };
  </script>
  

<style scoped>
  body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
  }
  
  /* Navbar */
  .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 20px;
      background-color: #f8f8f8;
      border-bottom: 1px solid #eaeaea;
  }
  .nav-links {
      list-style: none;
      display: flex;
      gap: 15px;
  }
  .nav-links li {
      display: inline;
  }
  .nav-links a {
      text-decoration: none;
      color: #333;
  }
  button {
      border: none;
      padding: 5px 10px;
      cursor: pointer;
  }
  .login-button {
      background-color: transparent;
      color: #333;
  }
  .signup-button {
      background-color: #333;
      color: #fff;
  }
  
  /* Signup Form */
  .signup-form-container {
      max-width: 500px;
      margin: 20px auto;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 5px;
      background-color: #fff;
  }
  .signup-form-container h1 {
      font-size: 24px;
      margin-bottom: 10px;
  }
  .signup-form-container p {
      margin-bottom: 20px;
      color: #666;
  }
  
  .steps {
      display: flex;
      justify-content: space-between;
      margin-bottom: 20px;
  }
  .step {
      flex: 1;
      text-align: center;
      padding: 5px 0;
      border-bottom: 2px solid #ddd;
      color: #999;
  }
  .step.active {
      border-bottom: 2px solid #333;
      color: #333;
  }
  
  .form-group {
      margin-bottom: 15px;
  }
  .form-group label {
      display: block;
      margin-bottom: 5px;
  }
  .form-group input {
      width: 100%;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 5px;
  }
  
  .submit-button {
      width: 100%;
      padding: 10px;
      background-color: #333;
      color: #fff;
      border-radius: 5px;
      font-size: 16px;
  }
</style>