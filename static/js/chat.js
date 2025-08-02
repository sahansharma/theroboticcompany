// Minimal AI Chat UI glue

function addMessage(content, type = "user") {
  const messagesContainer = document.getElementById("chat-messages")
  const messageDiv = document.createElement("div")
  messageDiv.className = `message ${type}-message`
  messageDiv.innerHTML = `
        <div class="message-avatar">
            ${
              type === "bot"
                ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10 4 4 0 1 1-4-4"></path><path d="M12 8a4 4 0 1 0 4 4"></path><circle cx="12" cy="12" r="1"></circle></svg>`
                : `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`
            }
        </div>
        <div class="message-content">${type === "bot" ? marked.parse(content) : content}</div>
    `
  messagesContainer.appendChild(messageDiv)
  messagesContainer.scrollTop = messagesContainer.scrollHeight
}

async function sendMessage() {
  const input = document.getElementById("chat-input")
  const sendBtn = document.getElementById("send-btn")
  const message = input.value.trim()
  if (!message) return
  addMessage(message, "user")
  input.value = ""
  sendBtn.disabled = true
  try {
    const response = await fetch("http://127.0.0.1:5000/ai/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: message }),
    })
    const data = await response.json()
    addMessage(data.answer || data.error || "Sorry, I encountered an error.", "bot")
  } catch (error) {
    addMessage("Sorry, I encountered an error. Please try again.", "bot")
  } finally {
    sendBtn.disabled = false
  }
}

function handleChatKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage()
  }
}

// On page load, get welcome message from backend
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/ai/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: "Say hello and introduce yourself as a robotics AI expert." }),
    })
    const data = await response.json()
    addMessage(data.answer || data.error || "Hello! I'm your robotics AI assistant.", "bot")
  } catch (error) {
    addMessage("Hello! I'm your robotics AI assistant.", "bot")
  }
})
