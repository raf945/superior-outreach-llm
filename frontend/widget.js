console.log("script loaded");

document.addEventListener("DOMContentLoaded", function () {

  console.log("DOM loaded");

  //injectChatButton();
  injectChatStyles();
  injectChatWidget();

  const chatWidget = document.getElementById("chat-widget");
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const sendBtn = document.getElementById("chat-send-btn");
  const openBtn = document.getElementById("test-button");

  const sessionId = localStorage.getItem("chat_session_id") || crypto.randomUUID();
  localStorage.setItem("chat_session_id", sessionId);

  // Writes the text as it is generated

  function typeWriterEffect(text, element, delay = 20) {
    let i = 0;
    const interval = setInterval(() => {
      element.textContent += text.charAt(i);
      i++;
      log.scrollTop = log.scrollHeight;
      if (i === text.length) clearInterval(interval);
    }, delay);
  }

  async function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    input.value = "";
    sendBtn.disabled = true; // 🔒 Disable send button

    const userMsg = document.createElement("div");
    userMsg.className = "chat-message user-message";
    userMsg.textContent = msg;
    log.appendChild(userMsg);
    // spinner.style.display = "block";
    
    const aiMsg = document.createElement("div");
    aiMsg.className = "chat-message ai-message";
    aiMsg.textContent = ""; // clear start
    log.appendChild(aiMsg);;
    

    console.log("Sending:", msg);

    try {
      const res = await fetch("https://superior-outreach-chatbot.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg, session_id: sessionId }),
      });

      const data = await res.json();
      // spinner.style.display = "none";
      if (data.response) {
        typeWriterEffect(data.response, aiMsg, 15);
      } else {
        aiMsg.innerHTML += "Sorry, no response.";
      }
    } catch (err) {
      // spinner.style.display = "none";
      aiMsg.innerHTML += "Sorry, an error occurred.";
      console.error("Chat error:", err);
    } finally {
      sendBtn.disabled = false; // ✅ Re-enable send button
  }

  }

  // Sends the prompt through with the key 'enter'
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  // Sends the prompt through with a click on the send button
  sendBtn.addEventListener("click", sendMessage);

  // This makes the button open and close the chat widget
  openBtn.addEventListener("click", function() {

    if (chatWidget.style.visibility === 'hidden') {
      chatWidget.style.visibility = 'visible';
    } else {
      chatWidget.style.visibility = 'hidden';
    }
  })

});
function injectChatStyles() {
  const css = `
#test-button {
  position: fixed;
  visibility: visible;
  right: 10px;
  bottom: 20px;
  padding: 0;
  border: none;
  background: none;       /* remove grey background */
  cursor: pointer;
  display: block;
  width: 70px;
  height: 70px;
  z-index: 99999;         /* keep it on top */
}

#test-button img {
  width: 100%;
  height: 100%;
  object-fit: contain;    /* keeps proportions */
}

#chat-widget {
  visibility: hidden;
  color: white;
  position: fixed;
  bottom: 100px;
  right: 20px;
  width: 300px;
  font-family: sans-serif;
  border-radius: 15px;
  z-index: 9999;
}

#chat-log {
  background-color: #0F0F0F;
  font-size: 15px;
  height: 300px;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px; /* space between messages */
}

#chat-input-container {
  position: relative;
  display: flex;
  align-items: center;
  background-color: #323232;
  border-radius: 0 0 15px 15px;
}

#chat-input {
  flex: 1;
  color: white;
  background-color: transparent; /* Let container show through */
  border: none;
  padding: 10px;
  border-radius: 0 0 0 15px;
  resize: none;
  height: 40px;
}

.chat-message {
  max-width: 80%;
  padding: 7px 12px;
  border-radius: 15px;
  word-wrap: break-word;
}

/* AI message — align left */
.ai-message {
  background-color: #323232;
  align-self: flex-start;
}

/* User message — align right */
.user-message {
  background-color: #767676;
  align-self: flex-end;
}

#chat-send-btn {
  width: 36px;
  height: 36px;
  background-color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  margin-right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

#chat-send-btn::before {
  content: "";
  display: inline-block;
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 10px solid black;
  transform: rotate(90deg); /* change to 45deg for paper plane style */
}

#chat-send-btn:disabled {
  background-color: #a0a0a0; /* greyed out */
  cursor: not-allowed;
  opacity: 0.6;
}

  `;

  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);
}


function injectChatWidget() {
  const container = document.createElement("div");
  container.id = "chat-widget";
  container.innerHTML = `
    <div id="chat-log"></div>
    <div id="chat-input-container">
      <textarea id="chat-input" wrap="soft" placeholder="Ask something..."></textarea>
      <button id="chat-send-btn"></button>
    </div>
    <button id="test-button">
      <img src="https://superior-outreach-chatbot.onrender.com/frontend/chat-icon.png" alt="Chat">
    
    </button>
  `;
  document.body.appendChild(container);
}

function injectChatButton() {
  console.log("injectChatButton() called");
  const container = document.createElement("div");
  container.id = "chat-button";
  container.innerHTML = `
    <button id="test-button">click me</button>
  `;
  document.body.appendChild(container);
  console.log("Chat button injected:", document.getElementById("test-button"));
}

