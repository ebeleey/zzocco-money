<template>
  <div>
    <h2>비밀번호 변경</h2>
    <form @submit.prevent="changePassword">
      <div>
        <label for="current_password">현재 비밀번호</label>
        <input
          id="current_password"
          v-model="current_password"
          type="password"
          required
        />
      </div>
      <div>
        <label for="new_password1">새 비밀번호</label>
        <input
          id="new_password1"
          v-model="new_password1"
          type="password"
          required
        />
      </div>
      <div>
        <label for="new_password2">새 비밀번호 확인</label>
        <input
          id="new_password2"
          v-model="new_password2"
          type="password"
          required
        />
      </div>
      <button type="submit">변경</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
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

        this.successMessage = "비밀번호가 성공적으로 변경되었습니다.";
        this.errorMessage = "";
        
        // Optional: Reset form fields after successful change
        this.current_password = "";
        this.new_password1 = "";
        this.new_password2 = "";
      } catch (error) {
        console.error("Password change error:", error.response);
        
        this.successMessage = "";
        
        // More detailed error handling
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
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