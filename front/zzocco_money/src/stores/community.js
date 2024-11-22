import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCommunityStore = defineStore('community', () => {
  const articles = ref([])
  
  const getArticles = function () {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/articles/',
    })
      .then(res => {
		console.log(res.data)
        articles.value = res.data
      })
      .catch(err => console.log(err))
  }   

  return { articles, getArticles }
}, { persist: true })