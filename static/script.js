let activeConversation = null;

function fetchConversations() {
    fetch('/get_conversations')
        .then(response => response.json())
        .then(conversations => {
            const conversationsDiv = document.getElementById('conversations');
            conversationsDiv.innerHTML = '';  // Clear the conversations list

            for (let username of conversations) {
                const div = document.createElement('div');
                div.textContent = username;
                div.onclick = function() {  // Set the active conversation when clicked
                    activeConversation = username;
                    fetchMessages();
                };
                conversationsDiv.appendChild(div);
            }
        });
}

function fetchMessages() {
    if (!activeConversation) {
        return;  // Don't fetch messages if no conversation is active
    }

    fetch(`/get_messages?username=${activeConversation}`)
        .then(response => response.json())
        .then(messages => {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '';  // Clear the messages

            for (let message of messages) {
                const p = document.createElement('p');
                p.textContent = message.content;
                messagesDiv.appendChild(p);
            }
        });
}

document.getElementById('send-message-form').addEventListener('submit', function(event) {
    event.preventDefault();

    if (!activeConversation) {
        return;  // Don't send a message if no conversation is active
    }

    const message = document.getElementById('message').value;

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ receiver_username: activeConversation, message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
        } else {
            document.getElementById('message').value = '';
        }
    });
});

setInterval(fetchConversations, 5000);  // Fetch conversations every 5 seconds
