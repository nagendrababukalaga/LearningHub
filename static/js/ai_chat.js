/**
 * LearningHub — AI Learning Assistant Interactive Chat Script
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('ai-chat-form');
  const chatInput = document.getElementById('ai-chat-input');
  const messagesContainer = document.getElementById('ai-messages-list');
  const topicSelect = document.getElementById('ai-topic-select');
  const actionPills = document.querySelectorAll('.ai-action-pill');

  if (!chatForm || !messagesContainer) return;

  // 1. Submit Custom Prompt
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const prompt = chatInput.value.trim();
    if (!prompt) return;

    appendMessage('user', prompt);
    chatInput.value = '';
    
    sendAIQuery(prompt, topicSelect?.value, 'general');
  });

  // 2. Preset Action Pills
  actionPills.forEach(pill => {
    pill.addEventListener('click', () => {
      const mode = pill.getAttribute('data-mode');
      const topicId = topicSelect?.value;
      const topicName = topicSelect?.options[topicSelect.selectedIndex]?.text || "this concept";

      const promptLabel = pill.innerText;
      appendMessage('user', `${promptLabel} for ${topicName}`);
      
      sendAIQuery('', topicId, mode);
    });
  });

  function sendAIQuery(prompt, topicId, actionMode) {
    const loadingId = appendLoadingIndicator();

    const formData = new FormData();
    formData.append('prompt', prompt);
    if (topicId) formData.append('topic_id', topicId);
    formData.append('action_mode', actionMode);

    fetch('/ai-assistant/api/query/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(res => res.json())
    .then(data => {
      removeLoadingIndicator(loadingId);
      if (data.status === 'ok') {
        appendMessage('assistant', data.response);
      } else {
        appendMessage('assistant', `⚠️ ${data.message || 'Error communicating with AI assistant.'}`);
      }
    })
    .catch(err => {
      removeLoadingIndicator(loadingId);
      appendMessage('assistant', '⚠️ Network error. Please try asking again.');
    });
  }

  function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `ai-message-row ${sender}`;

    const bubble = document.createElement('div');
    bubble.className = `ai-bubble ${sender}`;

    if (sender === 'assistant') {
      bubble.innerHTML = formatMarkdown(text);
    } else {
      bubble.innerText = text;
    }

    msgDiv.appendChild(bubble);
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendLoadingIndicator() {
    const id = 'ai-loading-' + Date.now();
    const loadDiv = document.createElement('div');
    loadDiv.id = id;
    loadDiv.className = 'ai-message-row assistant';
    loadDiv.innerHTML = `
      <div class="ai-bubble assistant loading">
        <div class="typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
    `;
    messagesContainer.appendChild(loadDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
  }

  function removeLoadingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  // Simple, safe client-side Markdown formatter for AI responses
  function formatMarkdown(text) {
    if (!text) return '';
    let html = text
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      // Code blocks ```python ... ```
      .replace(/```(?:python|py)?\n([\s\S]*?)```/g, (match, code) => {
        return `<div class="code-viewer-block"><div class="code-header"><span class="code-lang-tag">python</span></div><pre><code>${code.trim()}</code></pre></div>`;
      })
      // Inline code
      .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
      // Headers
      .replace(/^### (.*$)/gim, '<h4>$1</h4>')
      .replace(/^## (.*$)/gim, '<h3>$1</h3>')
      .replace(/^# (.*$)/gim, '<h2>$1</h2>')
      // Blockquotes
      .replace(/^\> (.*$)/gim, '<blockquote class="ai-quote">$1</blockquote>')
      // Bold
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      // Bullet points
      .replace(/^\s*[-*]\s+(.*)$/gim, '<li>$1</li>')
      .replace(/\n\n/g, '<p></p>');

    return html;
  }
});
