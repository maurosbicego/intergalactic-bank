<template>
  <div class="w-full h-screen flex items-center justify-center">
    <p>Hello</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BankComponent',
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
