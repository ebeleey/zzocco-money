<template>
  <div>
    <h1 class="page-title">환율 계산기</h1>
    <div class="currency-converter">
      <div class="input-container">
        <label>Amount</label>
        <div class="currency-input">
          <select v-model="fromCurrency" @change="convertCurrency">
            <option v-for="currency in currencyList" :key="currency" :value="currency">
              {{ currency }}
            </option>
          </select>
          <input type="number" v-model="amount" @input="convertCurrency" />
        </div>
      </div>

      <div class="convert-icon">
        <button @click="swapCurrencies">
          <img src="../assets/transfer.png" alt="Swap Currencies" />
        </button>
      </div>

      <div class="input-container">
        <label>Converted Amount</label>
        <div class="currency-input">
          <select v-model="toCurrency" @change="convertCurrency">
            <option v-for="currency in currencyList" :key="currency" :value="currency">
              {{ currency }}
            </option>
          </select>
          <input type="text" :value="convertedAmount" readonly />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CurrencyConverter',
  data() {
    return {
      amount: 1,
      fromCurrency: 'USD',
      toCurrency: 'KRW',
      currencyList: [],
      rates: null,
      convertedAmount: ''
    }
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:3000/api/exchange-rates');
      this.rates = response.data.rates;
      this.currencyList = Object.keys(this.rates).sort();
      this.convertCurrency();
    } catch (error) {
      console.error('환율 정보를 가져오는데 실패했습니다:', error);
    }
  },
  methods: {
    convertCurrency() {
      if (!this.rates || !this.amount) return;

      const fromRate = this.rates[this.fromCurrency];
      const toRate = this.rates[this.toCurrency];
      const converted = ((this.amount / fromRate) * toRate).toFixed(2);
      this.convertedAmount = `${converted} ${this.toCurrency}`;
    },
    swapCurrencies() {
      [this.fromCurrency, this.toCurrency] = [this.toCurrency, this.fromCurrency];
      this.convertCurrency();
    }
  }
}
</script>

<style scoped>
.page-title {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.currency-converter {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-container label {
  font-size: 0.9rem;
  color: #666;
}

.currency-input {
  display: flex;
  gap: 1rem;
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
  padding: 0.5rem;
  transition: transform 0.2s;
}

.convert-icon button:hover {
  transform: scale(1.1);
}

.convert-icon img {
  width: 24px;
  height: 24px;
}

input[readonly] {
  background-color: #f5f5f5;
}
</style>