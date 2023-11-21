<script setup>
import {ref} from "vue";
import axios from "axios";

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

    const response = await axios.post('http://127.0.0.1:5000/join_room', {
      room_name: formState.value.room_name,
    }, {
      withCredentials: true
        })
    console.log(response.data.message);

    // 关闭模态框
    open.value = false;

  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<template>
 <a-float-button-group
    type="primary"
    shape="square"
    :style="{
      bottom: '150px',
      right: '24px',
    }"
  >
   <a-float-button title="Search Rooms" @click="showModal">
     <template #icon>
       <SearchOutlined />
     </template>
   </a-float-button>
   <a-modal v-model:open="open" ok-text="Submit" @ok="handleSubmit">
      <a-form :form="form">
        <a-form-item label="Room Name" name="room_name" style="margin-top: 50px;">
          <a-input v-model:value="formState.room_name" />
        </a-form-item>
      </a-form>
    </a-modal>
   <a-float-button title="Logout" @click="Logout">
     <template #icon>
      <LogoutOutlined />
    </template>
   </a-float-button>
  </a-float-button-group>
</template>

<script>
import {LogoutOutlined, SearchOutlined} from "@ant-design/icons-vue";
import routers from "@/routers";
import axios from "axios";

export default {
  components: {
    SearchOutlined,
    LogoutOutlined
  },
  methods: {
    async Logout() {
      try{
        const response = await axios.get('http://127.0.0.1:5000/logout',
        {
      withCredentials: true
        });
        console.log(response.data.message);
        if(response.data.message==="return to index page")
        await routers.push("/");
      }catch(error){
        console.log('Error:', error)
      }
    }
  },
}
</script>

<style scoped>

</style>