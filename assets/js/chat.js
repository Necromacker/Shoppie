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
            background: var(--bg-roman-silver-alpha-30);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            background: var(--bg-white);
            width: 90%;
            max-width: 800px;
            height: 80vh;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-1);
            border: 2px solid var(--border-eerie-black);
        }
        .chat-header {
            background: var(--bg-white);
            padding: 1.5rem;
            border-radius: 12px 12px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border-eerie-black);
        }
        .chat-header h2 {
            color: var(--text-eerie-black);
            margin: 0;
            font-size: var(--fontSize-5);
        }
        .close-chat {
            background: none;
            border: none;
            color: var(--text-eerie-black);
            font-size: 2.4rem;
            cursor: pointer;
            padding: 0.5rem;
            transition: var(--transition-1);
        }
        .close-chat:hover {
            color: var(--text-orange-crayola);
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
            padding: 1.2rem;
            border-radius: 8px;
            animation: fadeIn 0.3s ease;
            border: 2px solid var(--border-eerie-black);
        }
        .user-message {
            background: var(--bg-white);
            color: var(--text-eerie-black);
            align-self: flex-end;
        }
        .bot-message {
            background: var(--bg-gainsboro);
            color: var(--text-eerie-black);
            align-self: flex-start;
        }
        .chat-input-container {
            padding: 1.5rem;
            background: var(--bg-white);
            border-radius: 0 0 12px 12px;
            display: flex;
            gap: 1rem;
            border-top: 2px solid var(--border-eerie-black);
        }
        #userInput {
            flex: 1;
            padding: 0.8rem;
            border: 2px solid var(--border-eerie-black);
            border-radius: 8px;
            background: var(--bg-white);
            color: var(--text-eerie-black);
            resize: none;
            height: 50px;
            
            font-family: var(--fontFamily-inter);
            font-size: var(--fontSize-9);
        }
        #userInput:focus {
            outline: none;
            border-color: var(--text-orange-crayola);
        }
        #sendMessage {
            padding: 1.2rem 2rem;
            background: var(--bg-white);
            color: var(--text-eerie-black);
            border: 2px solid var(--border-eerie-black);
            border-radius: 8px;
            cursor: pointer;
            transition: var(--transition-1);
            box-shadow: var(--shadow-2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            height: 50px;
            font-size:1.2rem;
        }
        #sendMessage:hover {
            box-shadow: none;
            color: var(--text-orange-crayola);
        }
        #sendMessage:disabled {
            background: var(--bg-gainsboro);
            cursor: not-allowed;
            box-shadow: none;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Loading animation */
        .loading {
            display: flex;
            gap: 0.5rem;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }
        .loading::after {
            content: '';
            width: 1.5rem;
            height: 1.5rem;
            border: 3px solid var(--bg-gainsboro);
            border-top-color: var(--text-orange-crayola);
            border-radius: 50%;
            animation: loading 0.8s linear infinite;
        }
        @keyframes loading {
            to { transform: rotate(360deg); }
        }
        /* Error message */
        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 1rem;
            border-radius: 8px;
            border: 2px solid #c62828;
            margin: 1rem 0;
            text-align: center;
        }
        /* Text formatting styles */
        .code-block {
            background: var(--bg-gainsboro);
            border: 2px solid var(--border-eerie-black);
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
        }
        .code-header {
            background: var(--bg-white);
            padding: 0.8rem 1.2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border-eerie-black);
        }
        .code-language {
            color: var(--text-eerie-black);
            font-size: var(--fontSize-9);
        }
        .copy-button {
            background: var(--bg-white);
            color: var(--text-eerie-black);
            border: 2px solid var(--border-eerie-black);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: var(--fontSize-9);
            transition: var(--transition-1);
            box-shadow: var(--shadow-3);
        }
        .copy-button:hover {
            box-shadow: none;
            color: var(--text-orange-crayola);
        }
        .code-text {
            padding: 1.2rem;
            margin: 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            color: var(--text-eerie-black);
            font-size: var(--fontSize-9);
        }
        .inline-code {
            background: var(--bg-gainsboro);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: var(--text-eerie-black);
            border: 1px solid var(--border-eerie-black);
        }
        .heading-1 {
            font-size: var(--fontSize-5);
            color: var(--text-eerie-black);
            margin: 1rem 0;
            font-family: var(--fontFamily-clashDisplay);
        }
        .bold-text {
            font-weight: var(--weight-semiBold);
            color: var(--text-eerie-black);
        }
        .italic-text {
            font-style: italic;
            color: var(--text-eerie-black);
        }
        .highlight-text {
            background: var(--bg-orange-crayola);
            color: var(--text-eerie-black);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
        }
        .strikethrough-text {
            text-decoration: line-through;
            color: var(--text-eerie-black);
        }
        .underlined-text {
            text-decoration: underline;
            color: var(--text-eerie-black);
        }
        .numbered-point {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        .bullet-point {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        .bullet-point::before {
            content: "•";
            position: absolute;
            left: 0.5rem;
            color: var(--text-orange-crayola);
        }
        .blockquote {
            border-left: 4px solid var(--text-orange-crayola);
            padding-left: 1rem;
            margin: 1rem 0;
            color: var(--text-eerie-black);
        }
        .link-text {
            color: var(--text-blue-crayola);
            text-decoration: none;
        }
        .link-text:hover {
            text-decoration: underline;
        }
        .image-link {
            max-width: 100%;
            border-radius: 8px;
            margin: 1rem 0;
            border: 2px solid var(--border-eerie-black);
        }
        /* Custom scrollbar */
        .chat-messages::-webkit-scrollbar {
            width: 8px;
        }
        .chat-messages::-webkit-scrollbar-track {
            background: var(--bg-gainsboro);
        }
        .chat-messages::-webkit-scrollbar-thumb {
            background: var(--text-eerie-black);
            border-radius: 4px;
        }
        .chat-messages::-webkit-scrollbar-thumb:hover {
            background: var(--text-orange-crayola);
        }
    `;
    document.head.appendChild(style);

    // Chat functionality
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendMessage');
    const closeButton = document.querySelector('.close-chat');

    function formatMessage(text) {
        // Format code blocks
        text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, language, code) => {
            return `<div class="code-block">
                <div class="code-header">
                    <span class="code-language">${language || 'text'}</span>
                    <button class="copy-button" onclick="navigator.clipboard.writeText(\`${code}\`)">Copy</button>
                </div>
                <pre><code class="code-text">${code}</code></pre>
            </div>`;
        });

        // Format inline code
        text = text.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

        // Format headings
        text = text.replace(/^# (.*?)$/gm, '<h1 class="heading-1">$1</h1>');

        // Format bold text
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong class="bold-text">$1</strong>');

        // Format italic text
        text = text.replace(/\*(.*?)\*/g, '<em class="italic-text">$1</em>');

        // Format highlighted text
        text = text.replace(/==(.*?)==/g, '<span class="highlight-text">$1</span>');

        // Format strikethrough text
        text = text.replace(/~~(.*?)~~/g, '<del class="strikethrough-text">$1</del>');

        // Format underlined text
        text = text.replace(/__(.*?)__/g, '<u class="underlined-text">$1</u>');

        // Format blockquotes
        text = text.replace(/^> (.*?)$/gm, '<blockquote class="blockquote">$1</blockquote>');

        // Format links
        text = text.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="link-text" target="_blank">$1</a>');

        // Format lists
        text = text.replace(/^\d+\. (.*?)$/gm, '<li class="ordered-list-item">$1</li>');
        text = text.replace(/^\* (.*?)$/gm, '<li class="unordered-list-item">$1</li>');

        return text;
    }

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = isUser ? message : formatMessage(message);
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message';
        loadingDiv.innerHTML = '<div class="loading"></div>';
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return loadingDiv;
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        chatMessages.appendChild(errorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function handleUserMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            
            const loadingDiv = showLoading();
            
            try {
                const response = await fetch('http://localhost:5000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                loadingDiv.remove();
                addMessage(data.response);
            } catch (error) {
                loadingDiv.remove();
                showError('Sorry, there was an error connecting to the AI service. Please make sure the backend server is running.');
                console.error('Error:', error);
            }
        }
    }

    // Event listeners
    askAiBtn.addEventListener('click', () => {
        chatModal.style.display = 'flex';
        userInput.focus();
    });

    closeButton.addEventListener('click', () => {
        chatModal.style.display = 'none';
    });

    sendButton.addEventListener('click', handleUserMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleUserMessage();
        }
    });

    // Close modal when clicking outside
    chatModal.addEventListener('click', (e) => {
        if (e.target === chatModal) {
            chatModal.style.display = 'none';
        }
    });

    // Add initial welcome message
    addMessage('Hello! I\'m Buymax AI, your shopping assistant. How can I help you today?');

    // Function to copy code
    window.copyCode = function(button) {
        const codeBlock = button.closest('.code-block');
        const code = codeBlock.querySelector('.code-text').textContent;
        navigator.clipboard.writeText(code).then(() => {
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        });
    };
}); 