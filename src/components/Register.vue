<template>
  <div class="w-full h-screen flex items-center justify-center">
        <form class="w-full md:w-1/3 bg-white rounded-lg" @submit.prevent="register">
            <div class="flex font-bold justify-center mt-6">
                <img class="h-20 w-20" src="@/assets/rm.png">
            </div>
            <h2 class="text-3xl text-center text-gray-700 mb-4">Register</h2>
            <div class="px-12 pb-10">
                <div class="w-full mb-2">
                  <div class="flex items-center">
                      <i class='ml-3 fill-current text-gray-400 text-xs z-10 fas fa-user'></i>
                      <input v-model="name" type='text' placeholder="Name"
                          class="-mx-6 px-8  w-full border rounded px-3 py-2 text-gray-700 focus:outline-none" />
                  </div>
                </div>
                <div class="w-full mb-2">
                  <div class="flex items-center">
                      <i class='ml-3 fill-current text-gray-400 text-xs z-10 fas fa-user'></i>
                      <input v-model="email" type='email' placeholder="E-Mail"
                          class="-mx-6 px-8  w-full border rounded px-3 py-2 text-gray-700 focus:outline-none" />
                  </div>
                </div>
                <div class="w-full mb-2">
                  <div class="flex items-center">
                      <i class='ml-3 fill-current text-gray-400 text-xs z-10 fas fa-lock'></i>
                      <input type='password' placeholder="Password" v-model="password" class="-mx-6 px-8 w-full border rounded px-3 py-2 text-gray-700 focus:outline-none" />
                  </div>
                </div>
                <button type="submit"
                    class="w-full py-2 rounded-full bg-green-600 text-gray-100 focus:outline-none">Register now</button>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterComponent',
  data: function () {
    return {
      email: "",
      password: "",
      name: ""
    }
  },
  methods: {
    register() {
      axios.post(`${process.env.VUE_APP_BACKEND}/user/register`, { "name": this.name, "email": this.email, "password": this.password }).then(data => {
        if (data.data.status === "Ok") {
          this.$cookies.set('auth',data.data.auth)
          let userid = data.data.userid
          axios.post(`${process.env.VUE_APP_BACKEND}/user/getbyid`, { "id": userid },{ headers: { "auth": this.$cookies.get('auth')}}).then(user => {
            this.$cookies.set('name',user.data.name)
            window.location.href = 'bank';
          })
        }
      }).catch(error => {
        alert(error)
      })
    }
  }
}
</script>
