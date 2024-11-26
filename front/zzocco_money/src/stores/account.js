import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const token = ref(null)
  const user = ref(null)

  const logIn = async function (payload) {
    const username = payload.username;
    const password = payload.password;
    try {
      const res = await axios.post('http://127.0.0.1:8000/accounts/login/', {
        username: username,
        password: password,
      });
      token.value = res.data.key;
  
      // 사용자 정보 가져오기
      await fetchUser();
      router.push('/');
    } catch (err) {
      console.error('로그인 실패:', err);
    }
  };

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const logout = function () {
    token.value = null
    user.value = null
    try {
      // router.go(0)
      router.push('/');

    } catch (err) {
      console.log(err)
      // router.go(-1)
  
      router.push('/');
    }
    // router.go(0)
  }

  const fetchUser = async() => {
    if (!token.value) {
      return
    }
    console.log(token.value)
    try {
      const res = await axios.get('http://127.0.0.1:8000/accounts/user/', {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }) 
      user.value = res.data
      console.log(res.data)
    } catch (err) {
      console.error('user data 가져오는 데 오류', err)
    }
  }

  const updateUser = function (updatedUserData) {
    user.value = { ...user.value, ...updatedUserData };
  }

  return { logIn, token, isLogin, logout, fetchUser, user, updateUser }
}, { persist: true }) 
