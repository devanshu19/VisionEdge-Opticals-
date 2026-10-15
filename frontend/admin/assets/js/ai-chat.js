document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('aiChatForm');
    if (form) {
        form.addEventListener('submit', handleSendMessage);
    }
});

async function handleSendMessage(e) {
    e.preventDefault();

    const input = document.getElementById('chatInput');
    const msgText = input.value.trim();
    if (!msgText) return;

    const chatBody = document.getElementById('chatMessages');

    // Append User Message
    const userMsg = document.createElement('div');
    userMsg.className = 'msg-bubble msg-user shadow-sm';
    userMsg.textContent = msgText;
    chatBody.appendChild(userMsg);

    input.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;

    // Loading indicator
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'msg-bubble msg-ai shadow-sm text-muted';
    loadingMsg.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>AI is thinking...';
    chatBody.appendChild(loadingMsg);
    chatBody.scrollTop = chatBody.scrollHeight;

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/chatbot/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msgText })
        });

        chatBody.removeChild(loadingMsg);

        if (response.ok) {
            const data = await response.json();
            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble msg-ai shadow-sm';
            aiMsg.innerHTML = data.reply || data.response || 'I have analyzed your request. Please check our inventory catalog for available matching products.';
            chatBody.appendChild(aiMsg);
        } else {
            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble msg-ai shadow-sm text-danger';
            aiMsg.textContent = 'Sorry, I ran into an error processing your query. Please try again.';
            chatBody.appendChild(aiMsg);
        }

    } catch (err) {
        chatBody.removeChild(loadingMsg);
        const aiMsg = document.createElement('div');
        aiMsg.className = 'msg-bubble msg-ai shadow-sm text-danger';
        aiMsg.textContent = 'Connection error. Could not reach AI service.';
        chatBody.appendChild(aiMsg);
    }

    chatBody.scrollTop = chatBody.scrollHeight;
}
