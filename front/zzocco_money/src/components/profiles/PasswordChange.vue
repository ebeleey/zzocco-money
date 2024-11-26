<template>
  <div class="password-change-page">
    <form @submit.prevent="changePassword" class="password-change">
      <div class="password-change-title">
        <h3>비밀번호 변경</h3>
        <button type="submit" class="edit-button">변경</button>
      </div>
      <div class="password-change-container">
        <div class="password-change-item">
          <h4>현재 비밀번호</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input
            id="current_password"
            v-model="current_password"
            type="password"
            required
          />
        </div>
        <br>
        <div class="password-change-item">
          <h4>새 비밀번호</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input
            id="new_password1"
            v-model="new_password1"
            type="password"
            required
          />
        </div>
        <br>
        <div class="password-change-item">
          <h4>비밀번호 확인</h4>
          <hr style="margin: 0 0 12px; width: 80%;">
          <input
            id="new_password2"
            v-model="new_password2"
            type="password"
            required
          />
        </div>
              

      </div>

    </form>
    <div class="alert-text">
      <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import { useAccountStore } from "@/stores/account";

export default {
  data() {
    return {
      current_password: "",
      new_password1: "",
      new_password2: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async changePassword() {
      // Validate passwords match before API call
      if (this.new_password1 !== this.new_password2) {
        this.errorMessage = "새 비밀번호가 일치하지 않습니다.";
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/accounts/password/change/",
          {
            current_password: this.current_password,
            new_password1: this.new_password1,
            new_password2: this.new_password2,
          },
          {
            headers: {
              Authorization: `Token ${useAccountStore().token}`,
            },
          }
        );

        alert("비밀번호가 성공적으로 변경되었습니다.");
        this.successMessage = "비밀번호가 성공적으로 변경되었습니다.";
        this.errorMessage = "";
        
        this.current_password = "";
        this.new_password1 = "";
        this.new_password2 = "";

      } catch (error) {
        console.error("Password change error:", error.response);
        
        this.successMessage = "";
        
        if (error.response) {

          const errorData = error.response.data;
          
          if (errorData.current_password) {
            this.errorMessage = "현재 비밀번호가 올바르지 않습니다.";
          } else if (errorData.new_password1) {
            this.errorMessage = errorData.new_password1[0] || "새 비밀번호 형식이 올바르지 않습니다.";
          } else {
            this.errorMessage = errorData.detail || "비밀번호 변경에 실패했습니다.";
          }
        } else if (error.request) {
          // The request was made but no response was received
          this.errorMessage = "서버 응답이 없습니다. 네트워크 연결을 확인해주세요.";
        } else {
          // Something happened in setting up the request that triggered an Error
          this.errorMessage = "요청 중 오류가 발생했습니다.";
        }
      }
    },
  },
};
</script>

<style scoped>
.password-change-page {
  display: flex;
  flex-direction: column;
}

h3 {
	font-size: 22px;
	font-weight: bolder;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}

h4 {
	font-size: 17px;
	font-weight: bolder;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}

.password-change {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.password-change-title {
  width: 30%;
  text-align: right;
}

.password-change-container {
  flex: 1;
  margin: 0 20px;
}

.password-change-item {
  display: flex;
  flex-direction: column;
}

.password-change-item input {
  width: 70%;
  margin: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.edit-button {
  /* margin-top: 10px; */
  padding: 8px 10px;
  line-height: 1.2;
  word-break: keep-all; 
  white-space: pre-wrap; 
}

.alert-text {
  text-align: center;
}


</style>