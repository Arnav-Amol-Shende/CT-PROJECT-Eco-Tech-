document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("sendBtn");
  const userInput = document.getElementById("userInput");
  const chatWindow = document.getElementById("chatWindow");

  sendBtn.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (message !== "") {
      appendMessage("user", message);
      userInput.value = "";
      sendMessageToBackend(message);
    }
  });

  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendBtn.click();
  });

  function appendMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.innerHTML = `<i class="fas ${sender === "bot" ? "fa-robot" : "fa-user"}"></i> ${text}`;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  async function sendMessageToBackend(message) {
    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message }) 
      });

      const data = await response.json();
      appendMessage("bot", data.response);

    } catch (error) {
      console.error("Error:", error);
      appendMessage("bot", "⚠️ Sorry, something went wrong!");
    }
  }
});
