import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useSavingsStore = defineStore('savings', () => {
    const depositsData = ref(null);
    const savingsData = ref(null);

    const getDeposit = async (pk) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/savings/get-single-deposit/${pk}/`);
            depositsData.value = response.data;
            return response.data;
        } catch (error) {
            console.error(`Error fetching deposit data for pk=${pk}:`, error.response?.data || error.message);
            throw error;
        }
    };

    const getSaving = async (pk) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/savings/get-single-saving/${pk}/`);
            savingsData.value = response.data;
            return response.data;
        } catch (error) {
            console.error(`Error fetching saving data for pk=${pk}:`, error.response?.data || error.message);
            throw error;
        }
    };
    
    return { getDeposit, getSaving };
});
