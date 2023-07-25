let lastMessage = null;

function fetchMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(decrypted_messages => {
            const messagesDiv = document.getElementById('messages');
            let newMessages = decrypted_messages;

            if (lastMessage) {
                const lastMessageIndex = decrypted_messages.findIndex(message => message[0] === lastMessage[0] && message[1] === lastMessage[1] && message[2] === lastMessage[2]);

                if (lastMessageIndex !== -1) {
                    newMessages = decrypted_messages.slice(lastMessageIndex + 1);
                }
            }

            for (let message of newMessages){
                const sender = message[0];
                const receiver = message[1];
                const content = message[2];

                const p = document.createElement('p');
                p.className = sender === '{{ username }}' ? 'sent' : 'received';  // Add a class to distinguish between sent and received messages

                if (content.startsWith("http") && (content.endsWith(".png") || content.endsWith(".jpg") || content.endsWith(".jpeg") || content.endsWith(".gif"))) {
                    const img = document.createElement('img');
                    img.src = content;
                    img.alt = content;
                    p.appendChild(img);
                } else if (content.startsWith("https://www.youtube.com/watch?v=")) {
                    const iframe = document.createElement('iframe');
                    const video_id = content.split("v=")[1];
                    iframe.src = "https://www.youtube.com/embed/" + video_id;
                    iframe.width = "560";
                    iframe.height = "315";
                    iframe.frameborder = "0";
                    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
                    iframe.allowFullscreen = true;
                    p.appendChild(iframe);
                } else {
                    const text = document.createTextNode(content);
                    p.appendChild(text);
                }

                const senderReceiverInfo = document.createTextNode(`From ${sender} to ${receiver}: `);
                p.prepend(senderReceiverInfo);

                messagesDiv.appendChild(p);
            }

            if (newMessages.length > 0) {
                lastMessage = newMessages[newMessages.length - 1];
            }
        });
}

document.getElementById('send-message-form').addEventListener('submit', function(event) {
    event.preventDefault(); // This line prevents the form from being submitted in the default way

    const receiver_username = document.getElementById('receiver_username').value;
    const message = document.getElementById('message').value;

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ receiver_username, message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Handle error
            console.error(data.error);
        } else {
            // Clear form
            document.getElementById('receiver_username').value = '';
            document.getElementById('message').value = '';
        }
    });
});

setInterval(fetchMessages, 1000);
