<script setup>

</script>

<template>
<a-button type="primary" @click="deleteRoom" danger ghost>DeleteRoom</a-button>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    currentRoomId: {
      type: Number,
      required: false,
    },
    currentRoomName: {
      type: String,
      required: false,
    },
  },
  methods: {
    async deleteRoom() {
      const room_id = this.currentRoomId;
      const room_name = this.currentRoomName;
      console.log("Room ID:", room_id);
      console.log("Room Name:", room_name);
      if (!room_id && !room_name) {
        alert("no room selected");
        return;
      }
      try {
        const response = await axios.post('http://127.0.0.1:5000/delete_room',{
            room_id: room_id,
            room_name: room_name,
        },{
      withCredentials: true
        });
        console.log(response.data.message);
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>

<style scoped>

</style>