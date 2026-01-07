const API_URL = "http://127.0.0.1:8000/query";

const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const typingEl = document.getElementById("typing");

function addMessage(role, text, sources=[]) {
  const row = document.createElement("div");
  row.className = `msg ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  if (sources && sources.length > 0) {
    const meta = document.createElement("div");
    meta.className = "meta";
    sources.forEach(s => {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = s;
      meta.appendChild(chip);
    });
    bubble.appendChild(meta);
  }

  row.appendChild(bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setTyping(on){
  typingEl.classList.toggle("hidden", !on);
  if(on) messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage(){
  const q = inputEl.value.trim();
  if(!q) return;

  addMessage("user", q);
  inputEl.value = "";
  inputEl.focus();

  sendBtn.disabled = true;
  setTyping(true);

  try{
    const res = await fetch(API_URL, {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ query: q })
    });

    const data = await res.json();
    addMessage("bot", data.answer || "No response.", data.sources || []);
  }catch(e){
    addMessage("bot", "Server error. Make sure the backend is running.", []);
  }finally{
    setTyping(false);
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e)=>{
  if(e.key === "Enter") sendMessage();
});

// Nice welcome message
addMessage("bot", "Hi! Ask me anything about ASU offices, contacts, policies, and services. I only answer from verified ASU documents.", []);
