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
    <a-button @click="RedirectToRegister" type="primary" size="large">Sign up</a-button>
  </a-config-provider>
</template>

<script>
import routers from "@/routers";


export default {
  methods:{
    RedirectToRegister(){
      routers.push('/register')
    }
  }
}
</script>

<style scoped>

</style>