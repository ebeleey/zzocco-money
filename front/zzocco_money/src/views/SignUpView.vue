<template>
	<div id="signup-page">
		
		<!-- Signup Form -->
		
		<div class="signup-form-container">
			<h1>회원 가입</h1>
			<p class="login-link">
        이미 가입한 계정이 있다면 <RouterLink to="/login">로그인 </RouterLink>해주세요.
      </p>

		

			<!-- 단계별 컴포넌트 렌더링 -->
			<component
				:is="currentStepComponent"
				:form-data="formData"
				@next-step="goToNextStep"
				@previous-step="goToPreviousStep"
				@submit="handleSubmit"
			/>
		</div>
	</div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { useRouter } from 'vue-router'
import { useAccountStore } from "@/stores/account";
import axios from "axios";
import StepOne from "@/components/signups/StepOne.vue";
import StepTwo from "@/components/signups/StepTwo.vue";
import StepThree from "@/components/signups/StepThree.vue";


const store = useAccountStore()
const router = useRouter()
const goToLogin = function() {
  router.push('/login')
}
const currentStep = ref(1); // 현재 단계
const formData = ref({
	basicInfo: { name: "", username: "", password: "" },
	detailedInfo: { gender: "", marriage: "", income_prospect: "", asset_level: "", income_level: "" },
	financialInfo: { selectedProducts: null },
});

// 단계별로 렌더링할 컴포넌트 설정
const currentStepComponent = computed(() => {
	if (currentStep.value === 1) return StepOne;
	if (currentStep.value === 2) return StepTwo;
	if (currentStep.value === 3) return StepThree;
});

// 다음 단계로 이동
const goToNextStep = () => {
	if (currentStep.value < 3) {
		currentStep.value += 1;
	}
};

// 이전 단계로 이동
const goToPreviousStep = () => {
	if (currentStep.value > 1) {
		currentStep.value -= 1;
	}
};

// 최종 데이터 제출 처리
const handleSubmit = () => {
  const user = formData.value
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/accounts/signup/`,
    data: {
      name: user.basicInfo.name,
      username: user.basicInfo.username,
      password: user.basicInfo.password,
      gender: user.detailedInfo.gender,
      marriage: user.detailedInfo.marriage,
      income_prospect: user.detailedInfo.income_prospect,
      asset_level: user.detailedInfo.asset_level,
      income_level: user.detailedInfo.income_level,
    }
  })
  .then(res => {
    console.log(formData)
    alert("회원가입이 완료되었습니다!");
	  router.push({name: 'home'})
  })
  .catch(err => console.log(err))
};

</script>
  
<style>
h1 {
  margin: 20px;
}
span {
  text-decoration: underline;
}
/* General Styles */
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

  background-color: #583423;
  color: #fff;
  border-radius: 5px;
}
.login-button {
  background-color: transparent;
  color: #333;
}

.login-link a {
	text-decoration: solid;
	color: #000000;
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

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

/* button {
	margin: 0 20px 0;
	padding: 5px 30px 5px;
} */
</style>

  