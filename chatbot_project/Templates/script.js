
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const chatBox = document.getElementById("chat-box");
const sendButton = form.querySelector(".send-button");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) return;

    const userMessage = document.createElement("p");
    userMessage.textContent = "You: " + message;
    chatBox.appendChild(userMessage);

    const botMessage = document.createElement("p");
    botMessage.textContent = "Bot: Chatterly is thinking...";
    chatBox.appendChild(botMessage);

    const formData = new FormData(form);
    messageInput.value = "";
    messageInput.disabled = true;
    sendButton.disabled = true;

    try {
        const response = await fetch("/chat/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.response || "The request failed.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let answer = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            answer += decoder.decode(value, { stream: true });
            botMessage.textContent = "Bot: " + answer;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        answer += decoder.decode();
        botMessage.textContent = "Bot: " + (answer || "No response received.");
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        botMessage.textContent = "Bot: " + (error.message || "Something went wrong. Try again.");
    } finally {
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
});