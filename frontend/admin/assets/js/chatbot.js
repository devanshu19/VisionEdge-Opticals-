document.addEventListener('DOMContentLoaded', () => {
    // Only initialize chatbot if the user is logged in
    const token = localStorage.getItem('token');
    if (!token) return;

    const widget = document.getElementById('ai-chatbot-widget');
    const toggleBtn = document.getElementById('chatbot-toggle-btn');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const chatWindow = document.getElementById('chatbot-window');
    
    const inputField = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send-btn');
    const messagesArea = document.getElementById('chatbot-messages');
    
    if (!widget || !toggleBtn) return;
    
    // Show widget
    widget.style.display = 'block';
    
    toggleBtn.addEventListener('click', () => {
        chatWindow.classList.toggle('d-none');
        chatWindow.classList.toggle('d-flex');
        if(!chatWindow.classList.contains('d-none')) {
            inputField.focus();
        }
    });
    
    closeBtn.addEventListener('click', () => {
        chatWindow.classList.add('d-none');
        chatWindow.classList.remove('d-flex');
    });
    
    sendBtn.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    async function sendMessage() {
        const text = inputField.value.trim();
        if (!text) return;
        
        inputField.value = '';
        appendMessage('user', text);
        
        // Show typing indicator
        const typingId = 'typing-' + Date.now();
        appendTypingIndicator(typingId);
        
        try {
            // Check if we are on a customer page to provide customer context
            let customerId = null;
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('id') && window.location.pathname.includes('customer')) {
                customerId = urlParams.get('id');
            } else if (urlParams.has('customer_id')) {
                customerId = urlParams.get('customer_id');
            }
            
            const payload = { message: text };
            if (customerId) payload.customer_id = customerId;
            
            const response = await fetchWithAuth(`${API_BASE_URL}/chatbot/message`, {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            
            removeTypingIndicator(typingId);
            
            if (response.ok) {
                const data = await response.json();
                appendMessage('ai', data.answer);
            } else {
                appendMessage('ai', "Sorry, I couldn't process that request at the moment.");
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            appendMessage('ai', "Connection error. Please try again later.");
        }
    }
    
    function appendMessage(sender, text) {
        const div = document.createElement('div');
        div.className = `d-flex mb-3 ${sender === 'user' ? 'justify-content-end' : ''}`;
        
        const bubble = document.createElement('div');
        bubble.className = `p-2 rounded shadow-sm ${sender === 'user' ? 'bg-primary text-white' : 'bg-white'}`;
        bubble.style.maxWidth = '85%';
        bubble.style.fontSize = '0.9rem';
        bubble.innerText = text; // innerText to sanitize basic html and preserve newlines
        
        div.appendChild(bubble);
        messagesArea.appendChild(div);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
    
    function appendTypingIndicator(id) {
        const div = document.createElement('div');
        div.id = id;
        div.className = "d-flex mb-3";
        div.innerHTML = `
            <div class="bg-white p-2 rounded shadow-sm d-flex align-items-center gap-1" style="max-width: 85%;">
                <div class="spinner-grow spinner-grow-sm text-primary" style="width: 0.5rem; height: 0.5rem;" role="status"></div>
                <div class="spinner-grow spinner-grow-sm text-primary" style="width: 0.5rem; height: 0.5rem;" role="status"></div>
                <div class="spinner-grow spinner-grow-sm text-primary" style="width: 0.5rem; height: 0.5rem;" role="status"></div>
            </div>
        `;
        messagesArea.appendChild(div);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
    
    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});
