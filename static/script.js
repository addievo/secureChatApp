let lastMessage = null;
let activeConversation = null;
let currentConversation = null;

document.getElementById('start-conversation').addEventListener('click', function(event) {
    event.preventDefault();
    event.stopPropagation();

    const newConversationUsername = document.getElementById('new-conversation').value;
    const conversationList = document.getElementById('conversation-list');
    const existingListItems = conversationList.getElementsByTagName('li');

    // Check if a conversation with the same username already exists
    for (let listItem of existingListItems) {
        if (listItem.getAttribute('data-conversation') === newConversationUsername) {
            // If it exists, simply make it the active conversation and fetch messages
            document.getElementById('receiver_username').value = newConversationUsername;
            activeConversation = newConversationUsername;
            fetchMessages();
            // Clear the new conversation input
            document.getElementById('new-conversation').value = '';
            return;  // Exit the function early
        }
    }

    // If it doesn't exist, create a new conversation
    const listItem = document.createElement('li');
    listItem.setAttribute('data-conversation', newConversationUsername);

    const conversationButton = document.createElement('button');
    conversationButton.textContent = newConversationUsername;
    conversationButton.addEventListener('click', function() {
        document.getElementById('receiver_username').value = newConversationUsername;
        activeConversation = newConversationUsername;
        fetchMessages();
    });

    listItem.appendChild(conversationButton);
    conversationList.appendChild(listItem);

    // Clear the new conversation input
    document.getElementById('new-conversation').value = '';
});


//send message event listener



document.getElementById('send-message-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Use the active conversation as the receiver_username
    const receiver_username = activeConversation;
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
            document.getElementById('message').value = '';
            // Fetch messages after a new message is sent
            fetchMessages();
        }
    })
    .catch(error => {
        // This will catch any errors that aren't caught in the then() function
        console.error('Error:', error);
    });
});





function fetchConversations() {
    fetch('/get_conversations')
        .then(response => response.json())
        .then(conversations => {
            const conversationList = document.getElementById('conversation-list');

            // Create a set of existing conversations
            const existingConversations = new Set();
            const existingListItems = conversationList.getElementsByTagName('li');
            for (let listItem of existingListItems) {
                existingConversations.add(listItem.getAttribute('data-conversation'));
            }

            for (let conversation of conversations) {
                // If the conversation is not already in the list, add it
                if (!existingConversations.has(conversation)) {
                    const listItem = document.createElement('li');
                    listItem.setAttribute('data-conversation', conversation); // Add data attribute
                    const conversationButton = document.createElement('button');
                    conversationButton.textContent = conversation;
                    conversationButton.addEventListener('click', function() {
                        document.getElementById('receiver_username').value = conversation;
                        activeConversation = conversation;
                        fetchMessages(); // Fetch messages for the selected conversation
                    });

                    listItem.appendChild(conversationButton);
                    conversationList.appendChild(listItem);
                }
            }
        });
}




function fetchMessages() {
    const receiver_username = document.getElementById('receiver_username').value;

    // Handle the case when the user tries to start a conversation with an empty username
    if (!receiver_username) {
        // Clear existing messages if the active conversation has changed
        const messagesDiv = document.getElementById('messages');
        while (messagesDiv.firstChild) {
            messagesDiv.removeChild(messagesDiv.firstChild);
        }
        activeConversation = null;
        return;
    }

    fetch(`/get_messages?username=${receiver_username}`)
        .then(response => response.json())
        .then(decrypted_messages => {
            const messagesDiv = document.getElementById('messages');

            // Clear existing messages if the active conversation has changed
            if (receiver_username !== activeConversation) {
                while (messagesDiv.firstChild) {
                    messagesDiv.removeChild(messagesDiv.firstChild);
                }
                activeConversation = receiver_username;
            }

            let newMessages = decrypted_messages;

            if (lastMessage) {
                const lastMessageIndex = decrypted_messages.findIndex(message => message[0] === lastMessage[0] && message[1] === lastMessage[1] && message[2] === lastMessage[2]);

                if (lastMessageIndex !== -1) {
                    newMessages = decrypted_messages.slice(lastMessageIndex + 1);
                }
            }

            for (let message of newMessages) {
                const messageElement = document.createElement('p');
                messageElement.textContent = `${message[0]} to ${message[1]}: ${message[2]}`;
                messagesDiv.appendChild(messageElement);

                // Remember the last fetched message
                lastMessage = message;
            }
        });
}
setInterval(fetchConversations, 5000);
setInterval(fetchMessages, 1000); // Fetch messages every second

