<script setup>
import SigninButton from "@/components/SignInButton.vue";
import SignupButton from "@/components/SignUpButton.vue";
</script>
<template>
  <div class="image-container">
    <img alt="ChatRoom Logo" class="centered-image" src="../../public/Logo.png">
    <div class="title-container">
          <h1>CI-IAT</h1>
    </div>
  </div>
  <hr style="margin-top: -150px;"><br>
  <div>
    <div class="component-container">
      <component :is="SignupButton" />
    <div class="horizontal-space"></div> <!-- 增加横向间隔 -->
     <component :is="SigninButton" />
    </div>
  </div>
</template>

<script>
import axios from "axios";


 export default {
  data() {
    return {
      message: ''
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/');
        this.message = response.data.message;
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
};
</script>
<style scoped>
.image-container {
  display: flex;
  justify-content: left;
  align-items: center;
  height: 100vh;
}
.centered-image {
  max-width: 100%;
  max-height: 100%
}
.title-container{
  text-align: center;
  font-size: 100px;
  padding-left: 220px;
}
.component-container {
  display: flex;
  align-items: center;
  margin-top: 20px;
  text-align: center;
  justify-content: center;
  width: 100%;
}
.horizontal-space {
  width: 20px;
}
</style>


