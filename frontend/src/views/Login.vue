<script setup>
import { reactive } from 'vue';
import axios from "axios";
import routers from "@/routers";

const formState = reactive({
  username: '',
  password: '',
  // remember: true,
});

const onFinish = (values) => {
  console.log('Success:', values);
};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/login', JSON.stringify({
      username: formState.username,
      password: formState.password,
    }),{
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        'Access-Control-Allow-Origin':'*',
      },
      withCredentials: true
    });
    console.log(response.data.message);
    if (response.data.message === 'Login successfully') {
        await routers.push('/home');
      }
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<template>
  <div class="container">
    <a-form
    :model="formState"
    name="basic"
    :label-col="{ span: 8 }"
    :wrapper-col="{ span: 16 }"
    autocomplete="off"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <a-form-item
      label="Username"
      name="username"
      :rules="[{ required: true, message: 'Please input your username!' }]"
    >
      <a-input v-model:value="formState.username" />
    </a-form-item>

    <a-form-item
      label="Password"
      name="password"
      :rules="[{ required: true, message: 'Please input your password!' }]"
    >
      <a-input-password v-model:value="formState.password" />
    </a-form-item>

<!--    <a-form-item name="remember" :wrapper-col="{ offset: 8, span: 16 }">-->
<!--      <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>-->
<!--    </a-form-item>-->

    <a-form-item     :wrapper-col="{ offset: 8, span: 16 }">
      <a-button type="primary" html-type="submit" @click="handleSubmit">Submit</a-button>
    </a-form-item>
  </a-form>
  </div>
</template>
<script>

</script>
<style>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
