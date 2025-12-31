// Chatbot Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8001',
    BOOK_ID: 'my-book',
    SESSION_TIMEOUT: 30 * 60 * 1000, // 30 minutes
};

// State Management
const state = {
    sessionId: null,
    isConnected: false,
    isLoading: false,
    selectedText: null,
    chatHistory: [],
};

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const statusText = document.getElementById('statusText');
const statusIndicator = document.querySelector('.status-dot');
const contextInfo = document.getElementById('contextInfo');
const selectionDisplay = document.getElementById('selectionDisplay');
const selectedTextDisplay = document.getElementById('selectedText');
const bookContent = document.querySelector('.book-content');

// Initialize on Page Load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing RAG Chatbot...');
    initializeChatbot();
    setupSelectionListener();
});

// Initialize Chatbot
async function initializeChatbot() {
    try {
        // Test connection to backend
        const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
        if (response.ok) {
            state.isConnected = true;
            setStatus('Connected', true);
            console.log('✅ Backend connected');

            // Create session
            await createSession();
        } else {
            throw new Error('Backend not responding');
        }
    } catch (error) {
        console.error('❌ Connection error:', error);
        setStatus('Offline - Check backend', false);
        showSystemMessage('⚠️ Cannot connect to backend. Make sure the server is running on http://localhost:8001');
    }
}

// Create Session
async function createSession() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/session`, {
            method: 'POST',
        });

        if (response.ok) {
            const data = await response.json();
            state.sessionId = data.session_id;
            console.log('✅ Session created:', state.sessionId);
            showSystemMessage(`✅ Session started. Session ID: ${state.sessionId.substring(0, 8)}...`);
        }
    } catch (error) {
        console.error('❌ Session creation error:', error);
        showSystemMessage('❌ Failed to create session');
    }
}

// Setup Text Selection Listener
function setupSelectionListener() {
    bookContent.addEventListener('mouseup', () => {
        const selected = window.getSelection().toString().trim();
        if (selected.length > 10) {
            state.selectedText = selected;
            displaySelectedText(selected);
            updateContextInfo(selected);
        } else {
            clearSelection();
        }
    });

    bookContent.addEventListener('click', () => {
        if (window.getSelection().toString().length === 0) {
            clearSelection();
        }
    });
}

// Display Selected Text
function displaySelectedText(text) {
    selectionDisplay.style.display = 'block';
    selectedTextDisplay.textContent = text;
    selectedTextDisplay.scrollTop = 0;
}

// Clear Selection
function clearSelection() {
    state.selectedText = null;
    selectionDisplay.style.display = 'none';
    updateContextInfo(null);
    window.getSelection().removeAllRanges();
}

// Update Context Info
function updateContextInfo(text) {
    if (text) {
        contextInfo.innerHTML = `<strong>📌 Using selected text (${text.length} chars)</strong> - Ask a question to use it as context`;
    } else {
        contextInfo.innerHTML = '<strong>💡 Tip:</strong> Select text from the book to use it as query context';
    }
}

// Set Status
function setStatus(text, isConnected) {
    statusText.textContent = text;
    if (isConnected) {
        statusIndicator.classList.add('connected');
    } else {
        statusIndicator.classList.remove('connected');
    }
}

// Handle Key Press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey && !state.isLoading) {
        event.preventDefault();
        sendQuestion();
    }
}

// Send Question
async function sendQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        showSystemMessage('⚠️ Please enter a question');
        return;
    }

    if (!state.isConnected) {
        showSystemMessage('❌ Not connected to backend');
        return;
    }

    if (!state.sessionId) {
        showSystemMessage('❌ No active session');
        return;
    }

    // Display user message
    displayMessage('user', question);
    questionInput.value = '';
    state.isLoading = true;
    sendBtn.disabled = true;

    // Show typing indicator
    showTypingIndicator();

    try {
        // Prepare request
        const requestBody = {
            question: question,
            book_id: CONFIG.BOOK_ID,
            top_k: 5,
        };

        // Add selected text if available
        if (state.selectedText) {
            requestBody.selected_text = state.selectedText;
        }

        console.log('📤 Sending query:', requestBody);

        // Send request to backend
        const response = await fetch(`${CONFIG.API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        // Remove typing indicator
        removeTypingIndicator();

        if (response.ok) {
            const data = await response.json();
            console.log('✅ Response received:', data);

            // Display bot response
            displayBotResponse(data);

            // Add to history
            state.chatHistory.push({
                question: question,
                response: data,
                timestamp: new Date(),
                selectedText: state.selectedText,
            });

            // Clear selected text after use
            clearSelection();
        } else {
            removeTypingIndicator();
            const error = await response.json();
            showSystemMessage(`❌ Error: ${error.detail}`);
        }
    } catch (error) {
        console.error('❌ Query error:', error);
        removeTypingIndicator();
        showSystemMessage(`❌ Failed to get response: ${error.message}`);
    } finally {
        state.isLoading = false;
        sendBtn.disabled = false;
        questionInput.focus();
    }
}

// Display Message
function displayMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Display Bot Response
function displayBotResponse(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    let html = '';

    // Add fallback badge if applicable
    if (data.is_fallback) {
        html += '<span class="fallback-badge">⚠️ General Knowledge (not from book)</span><br>';
    }

    // Add answer
    html += `<strong>Answer:</strong><br>${escapeHtml(data.answer)}<br>`;

    // Add sources if available
    if (data.sources && data.sources.length > 0) {
        html += '<div class="sources">';
        html += `<strong>📚 Sources (${data.sources.length} relevant sections):</strong>`;

        data.sources.forEach((source, index) => {
            const excerpt = escapeHtml(source.chunk_text).substring(0, 150) + '...';
            const score = (source.similarity_score * 100).toFixed(1);
            html += `
                <div class="source-item">
                    <strong>Source ${index + 1}</strong> - Page ${source.page_num} (${score}% relevant)<br>
                    <em>"${excerpt}"</em>
                </div>
            `;
        });

        html += '</div>';
    }

    // Add metadata
    html += `<div style="margin-top: 10px; font-size: 12px; color: #999;">`;
    html += `Model: ${data.model} | Response time: ${data.latency_ms}ms`;
    html += '</div>';

    contentDiv.innerHTML = html;
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Show Typing Indicator
function showTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.id = 'typingIndicator';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'typing-indicator';

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        contentDiv.appendChild(dot);
    }

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Remove Typing Indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Show System Message
function showSystemMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.background = '#fff3cd';
    contentDiv.style.color = '#856404';
    contentDiv.textContent = message;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Ask Question (for sample buttons)
function askQuestion(question) {
    questionInput.value = question;
    questionInput.focus();
    setTimeout(() => sendQuestion(), 100);
}

// Escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Session Management
window.addEventListener('beforeunload', () => {
    console.log('👋 Closing session:', state.sessionId);
    // Session will auto-expire on backend
});

// Periodic session check
setInterval(() => {
    if (state.sessionId && state.isConnected) {
        checkSessionStatus();
    }
}, 30000); // Check every 30 seconds

async function checkSessionStatus() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/session/${state.sessionId}`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Session still active:', data.message_count, 'messages');
        } else {
            console.warn('⚠️ Session may be expired');
            state.sessionId = null;
            await createSession();
        }
    } catch (error) {
        console.error('Session check error:', error);
    }
}

// Console welcome message
console.log(`
╔════════════════════════════════════════════╗
║                                            ║
║  🚀 RAG Chatbot Frontend Initialized       ║
║                                            ║
║  Backend: ${CONFIG.API_BASE_URL}
║  Book ID: ${CONFIG.BOOK_ID}
║  Session: Waiting for creation...          ║
║                                            ║
║  💡 Tips:                                  ║
║  - Select text from the book               ║
║  - Ask questions with that context         ║
║  - Responses include citations             ║
║                                            ║
╚════════════════════════════════════════════╝
`);
