import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const token = ref(null)
  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/login/',
      data: {
        username: username, password: password
      }
    })
      .then(res => {
        // console.log(res.data)
        token.value = res.data.key
        router.push('/')
      })
      .catch(err => console.log(err))
  }

  return { logIn, token }
}, { persist: true }) 
