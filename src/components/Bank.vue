<template>
  <div class="w-full h-screen text-center flex flex-wrap items-center justify-center">
    <div v-if="accounts.length > 0" class="flex flex-col mt-8">
      <div class="overflow-x-auto">
        <div class="min-w-full align-middle inline-block shadow overflow-hidden rounded">
          <table class="min-w-full">
            <thead class="bg-color-image text-gray-900">
              <tr>
                <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                  Nr.
                </th>
                <th class="py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                  Balance
                </th>
                <th class="px-6 py-6 text-left text-xs leading-4 font-medium uppercase tracking-wider">
                  Buy
                </th>
                <th class="px-6 py-6"></th>
              </tr>
            </thead>
            <tbody class="bg-color-form">
              <tr v-for="(a, index) in accounts" :key="index" class="border-b-2 border-gray-200">
                <td class="px-6 py-4 whitespace-no-wrap">
                  <div class="flex items-center">
                    <div class="ml-4">
                      <div class="text-sm leading-5 font-medium text-gray-900">
                        {{ index }} - {{ a._id }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-no-wrap">
                  <div class="flex items-center">
                    <div class="ml-4">
                      <div class="text-sm leading-5 font-medium text-gray-900">
                        {{ a.balance }}
                      </div>
                    </div>
                  </div>
                </td>

                <td class="px-6 py-4 whitespace-no-wrap text-right text-sm leading-5 font-medium">
                  <button v-if="a.balance >= 1000000" v-on:click="buy_spaceship(a._id)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Buy Spaceship</button>
                  <button v-else class="bg-gray-500 text-white font-bold py-2 px-4 rounded" disabled>Disabled</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="w-full" v-else>
      <p>You don't have any accounts!</p>
    </div>
    <div class="w-full">
      <button v-on:click="newAccount" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Open Account</button>
    </div>
    <div v-if="accounts.length > 0" class="container text-center justify-center flex">
      <div class="flex flex-wrap -mx-3 mb-2 align-middle w-1/2 text-center">
        <div class="w-full md:w-1/4 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-city">
            From
          </label>
          <select v-model="from" class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500">
            <option v-for="account in accounts" :key="account._id"> {{ account._id }}</option>
          </select>
        </div>
        <div class="w-full md:w-1/4 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-state">
            To
          </label>
          <div class="relative">
            <select  v-model="to" class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500">
              <option v-for="account in possibleto" :key="account._id"> {{ account._id }}</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
        </div>
        <div class="w-full md:w-1/4 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-zip">
            Amount
          </label>
          <input v-model="amount" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" type="number" placeholder="1000">
        </div>
        <div class="w-full md:w-1/4 px-3 mb-6 md:mb-0">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-zip">
            Transfer
          </label>
          <button @click="transfer" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Transfer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BankComponent',
  data: function () {
    return {
      accounts: [],
      from: "",
      to: "",
      amount: 0
    }
  },
  mounted() {
    if (this.$cookies.get('auth') === null) {
      window.location.href = 'login';
    }
    this.getAccounts()

  },
  computed: {
    possibleto: function () {
      let lst = []
      this.accounts.forEach(acc => {
        if (acc._id !== this.from) {
          lst.push(acc)
        }
      });
      return lst

    }
  },
  methods: {
    getAccounts() {
      axios.get(`${process.env.VUE_APP_BACKEND}/account/list`, { headers: { "auth": this.$cookies.get('auth')}}).then(data => {
        this.accounts = data.data.accounts
      })
    },
    buy_spaceship(acc) {
      axios.get(`${process.env.VUE_APP_BACKEND}/buy_spaceship/${acc}/`, { headers: { "auth": this.$cookies.get('auth')}}).then(data => {
        alert("The passphrase to enter your spaceship is: " + data.data.message)
        console.log(data.data.message)
      })
    },
    newAccount() {
      axios.get(`${process.env.VUE_APP_BACKEND}/account/new`, { headers: { "auth": this.$cookies.get('auth')}}).then(data => {
        alert("Created new Account")
        console.log(data)
        this.getAccounts()
      }).catch(error => {
        console.log(error)
        alert("Error. Please note that you can only open 5 accounts")
      })
    },
    transfer() {
      axios.post(`${process.env.VUE_APP_BACKEND}/account/transfer/${this.from}/${this.to}/`, { "amount": this.amount },{ headers: { "auth": this.$cookies.get('auth')}}).then(() => {
        alert("Transfered funds")
        this.getAccounts()
      }).catch(error => {
        console.log(error)
        alert("Error transfering funds")
      })
    }
  }
}
</script>
