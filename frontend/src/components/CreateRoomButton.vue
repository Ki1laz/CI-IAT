<script setup>
import { ref } from 'vue';
import axios from 'axios';


const open = ref(false);
const form = ref(null);
const formState = ref({
  room_name: '',
});

const showModal = () => {
  open.value = true;
};

const handleSubmit = async () => {
  try {

    const response = await axios.post('http://127.0.0.1:5000/create_room', {
      room_name: formState.value.room_name,
    }, {
      withCredentials: true
        })
    console.log(response.data.message);

    // 关闭模态框
    open.value = false;

    // 这里你可以更新房间列表，重新调用获取房间列表的函数
    // 例如：fetchChatrooms();
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<template>
  <div>
    <a-button ghost @click="showModal">CreateRoom</a-button>
    <a-modal v-model:open="open" ok-text="Submit" @ok="handleSubmit">
      <a-form :form="form">
        <a-form-item label="Room Name" name="room_name" style="margin-top: 50px;">
          <a-input v-model:value="formState.room_name" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>

</style>



