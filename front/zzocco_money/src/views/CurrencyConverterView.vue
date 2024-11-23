<template>
  <div>
    <h1 class="page-title">환율 계산기</h1>

    <div class="currency-converter">
      <div class="input-container">
        <div class="currency-input">
          <select v-model="fromCurrency">
            <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency.cur_unit">
              {{ currency.cur_unit }}
            </option>
          </select>
          <div class="amount-box">
            <input v-model.number="amount" type="number" class="amount-input" />
            <span class="currency-name">{{ getCurrencyName(fromCurrency) }}</span>
          </div>
        </div>
      </div>

      <div class="convert-icon">
        <button @click="convert">
          <img src="../assets/transfer.png" alt="Swap Currencies" />
        </button>
      </div>

      <div class="input-container">
        <div class="currency-input">
          <select v-model="toCurrency">
            <option v-for="currency in currencies" :key="currency.cur_unit" :value="currency.cur_unit">
              {{ currency.cur_unit }}
            </option>
          </select>
          <div class="amount-box" style="background-color: #f5f5f5;">
            <input :value="convertedAmount" type="text" class="amount-output" readonly />
            <span class="currency-name">{{ getCurrencyName(toCurrency) }}</span>
          </div>
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
    const convertedAmount = ref(0);
    const exchangeRates = ref([]);
    const currencies = ref([]);

    // 통화명 가져오기 함수
    const getCurrencyName = (currencyCode) => {
      const currency = exchangeRates.value.find(rate => rate.cur_unit === currencyCode);
      return currency ? currency.cur_nm : currencyCode;
    };

    // 환율 데이터 가져오기
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/currency/get_exchange_rates/"
        );
        exchangeRates.value = response.data;
        
        // KRW 추가 (API에서 제공하지 않음)
        exchangeRates.value.push({
          cur_unit: "KRW",
          cur_nm: "한국 원",
          deal_bas_r: 1
        });
        
        currencies.value = exchangeRates.value;
      } catch (error) {
        console.error("Error fetching exchange rates:", error);
      }
    };

    // 환율 가져오기 함수
    const getExchangeRate = (currencyCode) => {
      const currency = exchangeRates.value.find(rate => rate.cur_unit === currencyCode);
      return currency ? currency.deal_bas_r : 1;
    };

    // 통화 변환 로직
    const convert = () => {
      if (toCurrency.value === "KRW") {
        convertedAmount.value = amount.value * getExchangeRate(fromCurrency.value);
      } else if (fromCurrency.value === "KRW") {
        convertedAmount.value = amount.value / getExchangeRate(toCurrency.value);
      } else {
        const fromRate = getExchangeRate(fromCurrency.value);
        const toRate = getExchangeRate(toCurrency.value);
        convertedAmount.value = (amount.value * fromRate) / toRate;
      }
      // 소수점 둘째자리까지 반올림
      convertedAmount.value = Math.round(convertedAmount.value * 100) / 100;
    };

    // 컴포넌트가 마운트될 때 데이터 로드
    onMounted(fetchData);

    // 값 변경 시 변환 수행
    watch([fromCurrency, toCurrency, amount], convert);

    return {
      fromCurrency,
      toCurrency,
      amount,
      convertedAmount,
      currencies,
      convert,
      getCurrencyName,
    };
  },
};
</script>

<style scoped>
.amount-box {
  flex: 1;
  border: 1px solid #ddd;
  padding: 10px 15px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.currency-name {
  text-align: right;
}

.amount-input, 
.amount-output {
  border: none;
  background: transparent;
  font-size: 18px;
  width: 60%;
  outline: none;
  text-align: right;
}

.amount-output {
  margin-right: 10px;
}

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

.currency-input {
  display: flex;
  gap: 20px;
}

.currency-input select {
  padding: 20px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  position: relative;
  display: inline-block;
  width: 120px;
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



</style>