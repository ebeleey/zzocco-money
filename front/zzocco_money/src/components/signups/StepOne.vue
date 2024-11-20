<template>
	<div>
		<form @submit.prevent="handleSubmit">
			<div class="form-group">
				<label for="name">이름</label>
				<input type="text" id="name" v-model="formData.basicInfo.name" placeholder="이름을 입력하세요." required />
			</div>

			<div class="form-group">
				<label for="username">아이디</label>
				<input type="username" id="username" v-model="formData.basicInfo.username" placeholder="이메일을 입력하세요." required />
			</div>

			<div class="form-group">
				<label for="password">비밀번호</label>
				<input type="password" id="password" v-model="formData.basicInfo.password" placeholder="비밀번호를 입력하세요." required />
			</div>

			<div class="form-group">
				<label for="passwordConfirm">비밀번호 확인</label>
				<input type="password" id="passwordConfirm" v-model="passwordConfirm" placeholder="비밀번호를 확인하세요." required />
			</div>
		</form>
		<br>
		<!-- '이전' 버튼 추가 -->
		<button @click="$emit('previous-step')">이전</button>

		<!-- '회원가입 완료' 버튼 -->
		<button @click="nextStep">다음</button>
	</div>
</template>
  
<script setup>
import { ref } from 'vue'

const props = defineProps({
	formData: Object
})

const passwordConfirm = ref('')
const emit = defineEmits(['nextStep'])

const nextStep = function() {
	console.log(props)
	if (props.formData.basicInfo.password === passwordConfirm.value) {
		emit('nextStep')
	} else {
		alert('비밀번호가 불일치합니다.')
	}
}
</script>
  

<style scoped>

</style>