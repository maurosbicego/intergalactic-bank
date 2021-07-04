<template>
  <div class="w-full h-screen flex flex-wrap items-center justify-center">
      <img class="w-1/4" src="@/assets/cards.png">
      <h1 class="text-4xl w-full text-center text-green-700">Welcome to the Intergalactic Bank!</h1>
      <h3 class="text-2xl w-full text-center">You can now find a special offer on our site. Thanks to our partners, we're able to offer you a spaceship for only $1'000'000!!</h3>
      <h4 class="text-xl w-full text-center">Please <a class="text-blue-800" href="/login">Login</a> or <a class="text-blue-800" href="/register">Register</a></h4>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MainComponent',
  data: function () {
    return {
      email: "",
      password: ""
    }
  },
  methods: {
    login() {
      axios.post(`${process.env.VUE_APP_BACKEND}/user/login`, { "email": this.email, "password": this.password }).then(data => {
        if (data.data.status === "Ok") {
          this.$cookies.set('auth',data.data.auth)
          let userid = data.data.userid
          axios.post(`${process.env.VUE_APP_BACKEND}/user/getbyid`, { "id": userid },{ headers: { "auth": this.$cookies.get('auth')}}).then(user => {
            this.$cookies.set('name',user.data.name)
            window.location.href = 'bank';
          })
        }
      })
    }
  }
}
</script>
