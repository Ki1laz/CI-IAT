<script setup>
import CreateRoomButton from "@/components/CreateRoomButton.vue";
import DeleteRoomButton from "@/components/DeleteRoomButton.vue";
import FloatButtonGroups from "@/components/FloatButtonGroups.vue";

import {ref} from 'vue';

const size = ref('large');
</script>

<template>
  <div class="chat-container">
    <div class="side-panel">
      <a-button ghost type="primary" :size="size" class="room-title">Room List</a-button>
      <div class="button-separator"></div>
      <div class="button-container">
        <component :is="CreateRoomButton"/>
        <div class="button-separator"></div>
        <component :is="DeleteRoomButton" :currentRoomId="current_room_id" :currentRoomName="current_room_name"/>
      </div>
      <div class="button-separator"></div>
      <div class="room-list">
        <a-button v-for="room in chatroom_list" :key="room.id" :size="size" class="room-item" type="primary"
                  style="width: 100%; margin-bottom: 10px;" @click="changeChatroom(room)">
          {{ room.room_name }}
        </a-button>
      </div>
      <div class="avatar-container">
        <a-upload
            name="file"
            :show-upload-list="false"
            action="http://127.0.0.1:5000/modify_avatar"
            @change="handleChange">
          <a-avatar v-if="userAvatarUrl" :size="userAvatarSize" :src="'http://127.0.0.1:5000'+userAvatarUrl"/>
          <a-avatar v-else :size="defaultAvatarSize">
            <template #icon>
              <UserOutlined/>
            </template> <!-- 若未上传头像则显示默认头像 -->
          </a-avatar>
        </a-upload>
      </div>
    </div>
    <component :is="FloatButtonGroups"></component>
    <div class="chat-box">
      <a-button type="primary" :size="size" class="room-title">{{ current_room_name }}</a-button>
      <div class="chat-area" ref="chatArea" @scroll="checkScroll">
        <div v-for="message in messages" :key="message.id" :class="{ 'message-item': true, 'self-message': message.sender_id === sender_id }">
          <strong :style="{ color: 'white' }">{{ message.sender_name }}:</strong>
          <span :style="{ color: 'white' }">{{ message.content }}</span>
        </div>
      </div>
      <div class="input-container">
        <textarea v-model="newMessage" @keyup.enter="sendMessage" class="sent-message"
                  placeholder="Type your message"></textarea>
        <a-button type="primary" :size="size" @click="sendMessage" style="height: 100%">Send</a-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {io} from 'socket.io-client';
import {message} from 'ant-design-vue';
import UserOutlined from "@ant-design/icons-vue/lib/icons/UserOutlined";
import routers from "@/routers";


export default {
  components: {
    UserOutlined
  },
  data() {
    return {
      current_room_id: null,
      current_room_name: '',
      chatroom_list: [],
      messages: [],
      newMessage: '',
      userAvatarUrl: null,
      userAvatarSize: 'large',
      defaultAvatarSize: 'large',
      sender_id: null,
      sender_name: null
    };
  },
  created() {
    //加载用户聊天室
    this.fetchChatrooms();
    //加载用户头像
    this.getUserAvatar();
    //加载用户信息
    this.getUserInfo()
    //创建socketio连接
    this.socket = io('http://127.0.0.1:5000');
    //监听服务器信息
    this.socket.on("response", (data) => {
      console.log('Response from server:', data);
      this.messages.push(data.message);
    });
    // 获取聊天历史
    this.socket.on("chat_history", (data) => {
      // this.messages = this.messages.concat(data.history);
      const room_id = data.room_id;
      const history = data.history;
      console.log("history:", data)
      // 找到当前房间
      const currentRoom = this.chatroom_list.find(room => room.id === room_id);
      // 将历史消息添加到对应房间的 messages 数组中
      if (currentRoom) {
        currentRoom.messages = history;
        this.messages = this.messages.concat(history);
      }
    });
  },
  methods: {
    // 获取用户信息
    async getUserInfo() {
      try {
        // 向后端发送请求，获取用户信息
        const response = await axios.get('http://127.0.0.1:5000/get_info', {
          withCredentials: true
        });

        // 处理从服务器返回的用户信息
        const userInfo = response.data;
        console.log('User Info:', userInfo);
        this.sender_id = userInfo.id;// 更新 sender_id
        this.sender_name = userInfo.username //更新 sender_name
      } catch (error) {
        console.error('Error:', error);
      }
    },
    //获取聊天室列表
    async fetchChatrooms() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/room_list', {
          withCredentials: true
        });
        console.log('Response data:', response.data);
        this.chatroom_list = response.data;
      } catch (error) {
        console.log('Error:', error);
      }
    },
    //获取用户选择的当前聊天室
    changeChatroom(room) {
      this.current_room_id = room.id
      this.current_room_name = room.room_name;
      if(this.current_room_id && this.current_room_name){
        this.socket.emit("check", {
          room_id: this.current_room_id,
        });
      }
    },
    async getUserAvatar() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get_avatar', {
          withCredentials: true
        })
        console.log(response.data.avatar)
        this.userAvatarUrl = response.data.avatar
        console.log("userAvatarUrl:", this.userAvatarUrl)
      } catch (error) {
        console.log(error)
      }
    },
    //处理用户选择头像的状态
    async handleChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      } else if (info.file.status === 'done') {
        message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
      await this.uploadAvatar(info.file.originFileObj);
      await this.getUserAvatar();
    },
    //用户头像上传
    async uploadAvatar(file) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        const response = await axios.post('http://127.0.0.1:5000/modify_avatar',
            formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              },
              withCredentials: true
            });
        console.log('Response data:', response.data);
      } catch (error) {
        console.log('Error:', error)
      }
    },
    //用户消息发送
    async sendMessage() {
      if (this.newMessage && this.current_room_id && this.sender_id) {
        this.socket.emit("message", {
          message: this.newMessage,
          room_id: this.current_room_id,
          sender_id: this.sender_id,
        });
        this.newMessage = '';
      }
    },
    checkScroll() {
      const chatArea = this.$refs.chatArea;
      if (chatArea.scrollTop === 0) {
        // 向后端请求历史消息记录
        this.socket.emit("check", {room_id: this.current_room_id});
      }
    },
  }
};
</script>

<style>
.chat-container {
  display: flex;
  height: 100vh;
  background-color: rgb(42, 41, 41);
}

.side-panel {
  width: 15%;
  background-color: #1e1c1c;
  padding: 10px;
  position: relative;
}

.room-list {
  margin-bottom: 10px;
}

.room-title {
  width: 100%;
}

.room-item {
  padding: 5px;
  cursor: pointer;
  border: 1px solid #195fc9;
  margin-bottom: 5px;
}

.button-container {
  display: flex;
  justify-content: space-between;
}

.chat-box {
  flex: 1;
  width: 85%;
  display: flex;
  flex-direction: column;
}

.chat-area {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  border-bottom: 1px solid #383535;
}

.message-item {
  margin-bottom: 10px;
}

.input-container {
  display: flex;
  padding: 10px;
}

textarea {
  flex: 1;
  border: 1px solid #1e1c1c;
  border-radius: 5px;
  padding: 8px;
  margin-right: 10px;
  background-color: #1e1c1c;
}

.button-separator {
  width: 100%;
  height: 10px;
}

.sent-message {
  color: white;
}

.avatar-container {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}

.self-message {
    text-align: right;
    background-color: #4c86af; /* 自己发送的消息背景色，可以根据需要调整 */
}
</style>