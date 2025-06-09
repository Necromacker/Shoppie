import config from './config.js';

// Chat interface functionality
document.addEventListener('DOMContentLoaded', function() {
    const askAiBtn = document.getElementById('askAiBtn');
    if (!askAiBtn) return; // Exit if button not found
    
    // Create chat modal
    const chatModal = document.createElement('div');
    chatModal.className = 'chat-modal';
    chatModal.innerHTML = `
        <div class="chat-container">
            <div class="chat-header">
                <h2 class="title">Buymax AI Assistant</h2>
                <button class="close-chat">&times;</button>
            </div>
            <div class="chat-messages" id="chatMessages"></div>
            <div class="chat-input-container">
                <textarea id="userInput" placeholder="Ask Buymax AI anything..."></textarea>
                <button id="sendMessage" class="btn btn-primary">
                    <span class="span">Send</span>
                    <ion-icon name="arrow-forward" aria-hidden="true"></ion-icon>
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(chatModal);

    // Add chat modal styles
    const style = document.createElement('style');
    style.textContent = `
        .chat-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            background: white;
            width: 90%;
            max-width: 800px;
            height: 80vh;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .chat-header {
            padding: 1.5rem;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-header h2 {
            margin: 0;
            font-size: 1.5rem;
        }
        .close-chat {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
        }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .message {
            max-width: 80%;
            padding: 1rem;
            border-radius: 8px;
        }
        .user-message {
            background: #007bff;
            color: white;
            align-self: flex-end;
        }
        .bot-message {
            background: #f8f9fa;
            color: #212529;
            align-self: flex-start;
        }
        .chat-input-container {
            padding: 1.5rem;
            border-top: 1px solid #eee;
            display: flex;
            gap: 1rem;
        }
        #userInput {
            flex: 1;
            padding: 0.8rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            resize: none;
            height: 50px;
        }
        #sendMessage {
            padding: 0.8rem 1.5rem;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        #sendMessage:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .loading {
            display: flex;
            gap: 0.5rem;
            align-items: center;
            padding: 1rem;
        }
        .loading::after {
            content: '';
            width: 1.5rem;
            height: 1.5rem;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    // Event Listeners
    askAiBtn.addEventListener('click', (e) => {
        e.preventDefault();
        chatModal.style.display = 'flex';
    });

    const closeChat = chatModal.querySelector('.close-chat');
    closeChat.addEventListener('click', () => {
        chatModal.style.display = 'none';
    });

    const sendMessage = chatModal.querySelector('#sendMessage');
    const userInput = chatModal.querySelector('#userInput');

    sendMessage.addEventListener('click', handleUserMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleUserMessage();
        }
    });

    // Functions
    function addMessage(message, isUser = false) {
        const messagesDiv = chatModal.querySelector('#chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function showLoading() {
        const messagesDiv = chatModal.querySelector('#chatMessages');
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        messagesDiv.appendChild(loadingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        return loadingDiv;
    }

    function showError(message) {
        const messagesDiv = chatModal.querySelector('#chatMessages');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message bot-message';
        errorDiv.style.color = '#dc3545';
        errorDiv.textContent = message;
        messagesDiv.appendChild(errorDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    async function handleUserMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        userInput.value = '';
        const loadingDiv = showLoading();

        try {
            const response = await fetch(`${config.API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Failed to get response from AI');
            }

            const data = await response.json();
            loadingDiv.remove();
            addMessage(data.response);
        } catch (error) {
            console.error('Error:', error);
            loadingDiv.remove();
            showError('Failed to get response from AI. Please try again.');
        }
    }
}); 