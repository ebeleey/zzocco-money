<template>
  <div>
    <h1 class="page-title">환율 계산기</h1>

    <div class="currency-converter">

      <div class="input-container">
        <div class="currency-input">
          <select v-model="fromCurrency">
            <option v-for="currency in currencies" :key="currency" :value="currency">
              {{ currency }}
            </option>
          </select>
          <input class="amount" v-model.number="amount" type="number" />
        </div>
      </div>

      <div class="convert-icon">
        <button @click="swapCurrencies">
          <img src="../assets/transfer.png" alt="Swap Currencies" />
        </button>
      </div>

      <div class="input-container">
        <div class="currency-input">
          <select v-model="toCurrency">
            <option v-for="currency in currencies" :key="currency" :value="currency">
              {{ currency }}
            </option>
          </select>
          <input class="amount" type="text" :value="convertedAmount" readonly />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

export default {
  setup() {
    const fromCurrency = ref("KRW");
    const toCurrency = ref("USD");
    const amount = ref(1);
    const convertedAmount = ref();
    const currencies = ref([]);

    // 환율 데이터 가져오기
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/currency/get_exchange_rates/"
        );
        currencies.value = Object.keys(response.data); // 통화 목록
      } catch (error) {
        console.error("Error fetching exchange rates:", error);
      }
    };

    // 통화 변환 요청
    const convert = async () => {
      if (!fromCurrency.value || !toCurrency.value || !amount.value) {
        convertedAmount.value = null;
        return;
      }
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/currency/convert/",
          {
            amount: amount.value,
            from_currency: fromCurrency.value,
            to_currency: toCurrency.value,
          }
        );
        convertedAmount.value = response.data.result;
      } catch (error) {
        console.error("Error in currency converter:", error);
      }
    };

    // 컴포넌트가 마운트될 때 환율 데이터 가져오기
    onMounted(() => {
      fetchData();
    });

    // 값 변경 시 변환 수행
    watch([fromCurrency, toCurrency, amount], convert);

    return {
      fromCurrency,
      toCurrency,
      amount,
      convertedAmount,
      currencies,
      convert
    };
  }
};
</script>

<style scoped>

.currency-converter {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border: 1px solid #ddd;
}

.amount {
  text-align: right;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.currency-input {
  display: flex;
  gap: 20px;
}

.currency-input select,
.currency-input input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.currency-input select {
  width: 100px;
}

.currency-input input {
  flex: 1;
}

.convert-icon {
  display: flex;
  justify-content: center;
  align-items: center;
}

.convert-icon button {
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s;
}

.convert-icon button:hover {
  transform: scale(1.1);
}

.convert-icon img {
  width: 50px;
  height: 50px;
}

input[readonly] {
  background-color: #f5f5f5;
}

</style>