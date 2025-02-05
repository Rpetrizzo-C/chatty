<template>
  <v-app>
    <v-main>
      <v-container v-if="!inRoom" class="join-container">
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6">
            <v-card class="mx-auto mt-5" elevation="3">
              <v-card-title class="text-center text-h4 py-4">
                Chatty Chat
              </v-card-title>

              <v-card-text>
                <v-alert
                  v-if="error"
                  type="error"
                  variant="tonal"
                  closable
                  class="mb-4"
                >
                  {{ error }}
                </v-alert>

                <!-- Room Credentials -->
                <v-card
                  v-if="showCredentials"
                  color="primary"
                  variant="outlined"
                  class="mb-4 text-center"
                >
                  <v-card-title>Room Created!</v-card-title>
                  <v-card-text>
                    <div class="d-flex align-center mb-2 justify-center">
                      <span class="mr-2">Room ID: {{ roomId }}</span>
                      <v-btn
                        density="comfortable"
                        icon="mdi-content-copy"
                        size="small"
                        variant="text"
                        @click="copyToClipboard(roomId, 'Room ID')"
                      >
                        <v-icon>mdi-content-copy</v-icon>
                      </v-btn>
                    </div>
                    <div class="d-flex align-center justify-center">
                      <span class="mr-2">Password: {{ roomPassword }}</span>
                      <v-btn
                        density="comfortable"
                        icon="mdi-content-copy"
                        size="small"
                        variant="text"
                        @click="copyToClipboard(roomPassword, 'Password')"
                      >
                        <v-icon>mdi-content-copy</v-icon>
                      </v-btn>
                    </div>
                  </v-card-text>
                  <v-card-text class="text-center text-caption">
                    Share these credentials with people you want to invite to
                    the chat
                  </v-card-text>
                  <v-btn
                    color="primary"
                    block
                    class="mt-4"
                    @click="connectToRoom"
                  >
                    Join Room Now
                  </v-btn>
                </v-card>

                <v-row v-else>
                  <!-- Create Room Form -->
                  <v-col cols="12" md="6">
                    <v-card variant="outlined" class="mb-4">
                      <v-card-title>Create New Room</v-card-title>
                      <v-card-text>
                        <v-text-field
                          v-model="createUsername"
                          label="Username"
                          variant="outlined"
                          density="comfortable"
                          :rules="[(v) => !!v || 'Username is required']"
                        ></v-text-field>
                        <v-btn
                          color="primary"
                          block
                          @click="createRoom"
                          :disabled="!createUsername"
                        >
                          Create Room
                        </v-btn>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <!-- Join Room Form -->
                  <v-col cols="12" md="6">
                    <v-card variant="outlined" class="mb-4">
                      <v-card-title>Join Room</v-card-title>
                      <v-card-text>
                        <v-text-field
                          v-model="joinUsername"
                          label="Username"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                        <v-text-field
                          v-model="roomId"
                          label="Room ID"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                        <v-text-field
                          v-model="roomPassword"
                          label="Password"
                          type="password"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                        <v-btn
                          color="secondary"
                          block
                          @click="joinRoom"
                          :disabled="!canJoin"
                        >
                          Join Room
                        </v-btn>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- Chat Room -->
      <v-container v-else fluid class="chat-container pa-0">
        <v-card height="100vh" class="d-flex flex-column">
          <!-- Chat Header -->
          <v-app-bar color="primary">
            <v-app-bar-title> Room: {{ roomId }} </v-app-bar-title>
            <v-btn icon @click="leaveRoom">
              <v-icon>mdi-exit-to-app</v-icon>
            </v-btn>
          </v-app-bar>

          <!-- Messages Area -->
          <v-card-text
            class="flex-grow-1 overflow-y-auto"
            ref="messageContainer"
          >
            <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="[
                'd-flex',
                'mb-3',
                msg.sender === (joinUsername || createUsername)
                  ? 'justify-end'
                  : 'justify-start',
              ]"
            >
              <v-card
                :color="getMessage(msg).color"
                :class="getMessage(msg).class"
                variant="tonal"
                max-width="70%"
              >
                <v-card-text class="pa-2">
                  <div
                    class="text-caption font-weight-medium"
                    v-if="!msg.system"
                  >
                    {{ msg.sender }}
                  </div>
                  <div :class="getMessage(msg).textClass">
                    {{ getMessage(msg).message }}
                  </div>
                  <div class="text-caption text-right" v-if="!msg.system">
                    {{ new Date(msg.timestamp).toLocaleTimeString() }}
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>

          <!-- Input Area -->
          <v-card-actions class="pa-4 bg-grey-lighten-4">
            <v-text-field
              v-model="newMessage"
              placeholder="Type a message..."
              variant="outlined"
              density="comfortable"
              hide-details
              @keyup.enter="sendMessage"
            >
              <template v-slot:append>
                <v-btn
                  color="primary"
                  icon
                  @click="sendMessage"
                  :disabled="!newMessage.trim()"
                >
                  <v-icon>mdi-send</v-icon>
                </v-btn>
              </template>
            </v-text-field>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="2000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-app>
</template>

<script>
import {
  generateRoomKey,
  encryptMessage,
  decryptMessage,
  hashPassword,
} from "./utils/encryption";

export default {
  data() {
    return {
      createUsername: "",
      joinUsername: "",
      roomId: "",
      roomPassword: "",
      inRoom: false,
      messages: [],
      newMessage: "",
      ws: null,
      showCredentials: false,
      error: null,
      encryptionKey: null,
      snackbar: {
        show: false,
        text: "",
        color: "success",
      },
    };
  },

  computed: {
    canJoin() {
      return this.joinUsername && this.roomId && this.roomPassword;
    },
  },

  methods: {
    getMessage(msg) {
      if (msg.system) {
        return {
          color: "accent",
          class: "text-center mx-auto",
          textClass: "text-grey-darken-1",
          message: msg.message,
        };
      }

      const isOwn = msg.sender === (this.joinUsername || this.createUsername);
      return {
        color: isOwn ? "message-own" : "message-other",
        class: isOwn ? "ml-auto" : "mr-auto",
        textClass: "text-black",
        message: msg.message,
      };
    },

    async createRoom() {
      try {
        console.log("Creating room...");
        const encryptionKey = generateRoomKey();
        const roomPassword = generateRoomKey().slice(0, 8);
        const hashedPassword = hashPassword(roomPassword);

        console.log("Sending create room request...");
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/rooms/create?` +
            new URLSearchParams({
              creator_name: this.createUsername,
              hashed_password: hashedPassword,
              encryption_key: encryptionKey,
            }),
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();
        console.log("Room created successfully:", data);

        this.roomId = data.room_id;
        this.roomPassword = roomPassword;
        this.encryptionKey = encryptionKey;
        this.showCredentials = true;
        this.error = null;
      } catch (error) {
        console.error("Error creating room:", error);
        this.error = "Failed to create room";
      }
    },

    async joinRoom() {
      try {
        console.log("Joining room...");
        const hashedPassword = hashPassword(this.roomPassword);

        console.log("Verifying room...");
        const response = await fetch(
          "http://localhost:8000/api/rooms/verify?" +
            new URLSearchParams({
              room_id: this.roomId,
              hashed_password: hashedPassword,
            }),
          {
            method: "POST",
          }
        );

        const data = await response.json();
        console.log("Room verification response:", data);

        if (response.ok) {
          this.error = null;
          this.encryptionKey = data.encryption_key;
          console.log("Room verified, connecting...");
          this.connectToRoom();
        } else {
          this.error = data.detail || "Failed to join room";
        }
      } catch (error) {
        console.error("Error joining room:", error);
        this.error = "Failed to join room";
      }
    },

    connectToRoom() {
      console.log("Starting connection process...");
      const username = this.joinUsername || this.createUsername;
      if (!this.roomId || !username) {
        console.error("Room ID or username is missing");
        return;
      }

      try {
        const wsUrl = `${import.meta.env.VITE_WS_URL}/ws/${
          this.roomId
        }/${username}`;
        console.log("Connecting to WebSocket:", wsUrl);

        if (this.ws) {
          this.ws.close();
        }

        this.ws = new WebSocket(wsUrl);

        this.ws.onmessage = (event) => {
          console.log("Received message:", event.data);
          const data = JSON.parse(event.data);

          if (data.system) {
            this.messages.push({
              sender: "System",
              message: data.message,
              timestamp: new Date(),
              system: true,
            });
          } else {
            try {
              // Only decrypt the message content, not the username
              const decryptedMessage = decryptMessage(
                data.message,
                this.encryptionKey
              );

              this.messages.push({
                sender: data.sender,
                message: decryptedMessage,
                timestamp: data.timestamp,
              });
            } catch (error) {
              console.error("Error decrypting message:", error);
            }
          }
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        };

        this.ws.onopen = () => {
          console.log("WebSocket connection established");
          this.inRoom = true;
          this.showCredentials = false;
          this.error = null;
        };

        this.ws.onclose = (event) => {
          console.log("WebSocket connection closed:", event);
          if (!event.wasClean) {
            this.error = "Connection closed unexpectedly";
          }
          this.leaveRoom();
        };

        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
          this.error = "Failed to connect to the room";
        };
      } catch (error) {
        console.error("Error in connectToRoom:", error);
        this.error = "Failed to connect to the room";
      }
    },

    sendMessage() {
      if (!this.newMessage.trim()) return;

      try {
        const message = {
          content: encryptMessage(this.newMessage, this.encryptionKey),
          timestamp: new Date().toISOString(),
        };

        this.ws.send(JSON.stringify(message));
        this.newMessage = "";
      } catch (error) {
        console.error("Error sending message:", error);
        this.error = "Failed to send message";
      }
    },

    leaveRoom() {
      if (this.ws) {
        this.ws.close();
      }
      this.inRoom = false;
      this.messages = [];
      this.roomId = "";
      this.roomPassword = "";
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },

    async copyToClipboard(text, type) {
      try {
        await navigator.clipboard.writeText(text);
        this.snackbar.color = "success";
        this.snackbar.text = `${type} copied to clipboard!`;
        this.snackbar.show = true;
      } catch (err) {
        console.error("Failed to copy text: ", err);
        this.snackbar.color = "error";
        this.snackbar.text = "Failed to copy to clipboard";
        this.snackbar.show = true;
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  height: 100vh;
  background-color: rgb(245, 240, 255, 0.5);
}

.v-card-text.overflow-y-auto {
  height: calc(100vh - 128px);
  padding-bottom: 20px;
}

.message-system {
  text-align: center;
  color: #666;
  margin: 10px 0;
}

/* Add some shadow to messages for better depth */
.v-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

/* Make message text more readable */
.v-card-text {
  font-size: 1rem;
  line-height: 1.5;
}

.v-btn.v-btn--density-comfortable {
  opacity: 1 !important;
}
</style>
