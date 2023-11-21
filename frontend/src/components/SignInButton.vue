<script setup>

</script>

<template>
 <a-config-provider
    :theme="{
      token: {
        colorPrimary: '#008eb9',
      },
    }"
  >
    <a-button @click="RedirectToLogin" type="primary" size="large">Sign in</a-button>
  </a-config-provider>
</template>

<script>
import routers from "@/routers";


export default {
  methods:{
    RedirectToLogin(){
      routers.push('/login')
    }
  }
}
</script>

<style scoped>

</style>





