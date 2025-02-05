# Chatty Application

A secure, real-time chat application that allows users to create and join private chat rooms with end-to-end encryption.

## Features

- 🔐 End-to-end encryption for all messages
- 🚀 Real-time communication using WebSocket
- 🎨 Modern UI with Vuetify
- 🔒 Password-protected rooms
- 📱 Responsive design
- 🐳 Docker support
- ☁️ AWS deployment ready

## Tech Stack

- **Frontend:**
  - Vue.js 3
  - Vuetify 3
  - Vite
  - CryptoJS for encryption

- **Backend:**
  - FastAPI
  - WebSockets
  - Python 3.9+

- **Infrastructure:**
  - Docker
  - AWS CDK
  - GitHub Actions (optional)

## Getting Started

### Prerequisites

- Node.js 16+
- Python 3.9+
- Docker (optional)
- AWS CLI (optional, for deployment)

### Local Development

1. Clone the repository:

```bash
git clone <repository-url>
cd chatty
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm run dev
```

4. Open your browser and navigate to:
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

### Docker Deployment

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

2. Access the application at http://localhost:3000

### AWS Deployment

1. Install and configure AWS CDK:
```bash
npm install -g aws-cdk
cdk bootstrap
```

2. Deploy the infrastructure:
```bash
cd cdk
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cdk deploy
```

## Usage

1. **Create a Room:**
   - Enter your username
   - Click "Create Room"
   - Share the room ID and password with others

2. **Join a Room:**
   - Enter your username
   - Input the room ID and password
   - Click "Join Room"

3. **Chat:**
   - Type your message
   - Press enter or click send
   - All messages are automatically encrypted/decrypted

## Security Features

- End-to-end encryption using AES-256
- Secure room access with password protection
- No message storage - all communications are ephemeral
- WebSocket secure connection (when deployed with SSL)

## Project Structure
```
chatty/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── styles/
│   │   ├── utils/
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   └── package.json
├── cdk/
│   └── stacks/
└── docker-compose.yml
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Vuetify](https://vuetifyjs.com/)
- [AWS CDK](https://aws.amazon.com/cdk/)