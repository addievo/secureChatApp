let lastMessage = null;
let activeConversation = null;
let currentConversation = null;
var socket = io();
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
    socket.emit('start_conversation', { 'username': newConversationUsername });

    // Clear the new conversation input
    document.getElementById('new-conversation').value = '';
});



//send message event listener
document.getElementById('send-message-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Use the active conversation as the receiver_username
    const receiver_username = activeConversation;
    const message = document.getElementById('message').value;

    // Emit a 'new_message' event to the server
    socket.emit('new_message', { receiver_username, message });

    // Clear the form
    document.getElementById('message').value = '';
});

document.getElementById('message').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) { // keyCode for Enter key
        event.preventDefault(); // Prevent newline being added to textarea
        document.getElementById('send-message-form').dispatchEvent(new Event('submit', { cancelable: true })); // Trigger form submission
    }
});

socket.on('message_sent', function(data) {
    // Fetch messages after a new message is sent
    addMessage(data);
});

let picker = document.querySelector('emoji-picker');
let pickerEventAdded = false; // New variable to track whether the event has been added

document.getElementById('emoji-button').addEventListener('click', function() {
    if (!picker) {
        console.error("Emoji picker not found");
        return;
    }

    // Only add the event listener if it hasn't been added before
    if (!pickerEventAdded) {
        picker.addEventListener('emoji-click', function(event) {
            // Insert the emoji at the cursor
            let messageInput = document.getElementById('message');
            let cursorPosition = messageInput.selectionStart;
            messageInput.value = messageInput.value.substring(0, cursorPosition)
                + event.detail.unicode
                + messageInput.value.substring(cursorPosition);

            picker.style.display = 'none'; // Hide the emoji picker
        });

        pickerEventAdded = true; // Mark that the event listener has been added
    }

    // Show or hide the emoji picker
    picker.style.display = picker.style.display === 'none' ? 'block' : 'none';
});


document.getElementById('image').addEventListener('change', function() {
    var file = this.files[0];
    var formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', 'uue6qj3l');  // Your upload preset
    uploadToCloudinary(formData);
});

function uploadToCloudinary(formData) {
    var apiUrl = 'https://api.cloudinary.com/v1_1/ddxlk4go1/image/upload';  // Your Cloudinary cloud name
    $.ajax(apiUrl, {
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
    }).done(function(response) {
        var messageInput = document.getElementById('message');
        messageInput.value += response.secure_url;  // Use `secure_url` for the HTTPS version of the image URL
    });
}


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

function addMessage(data) {
    // Assuming `data` is an object with a `message` field that holds the new message text
    const messageText = data.message;

    const messagesDiv = document.getElementById('messages');

    // Create a new paragraph element to hold the message text
    const messageElement = document.createElement('p');
    messageElement.textContent = messageText;

    // Append the new message to the chat
    messagesDiv.appendChild(messageElement);
}

function fetchMessages() {
    const receiver_username = document.getElementById('receiver_username').value;

    if (!receiver_username) {
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
                //parse datetime
                const timestamp = new Date(message[3]);
                const date = timestamp.getDate();
                const month = timestamp.getMonth() + 1;
                const year = timestamp.getFullYear();
                const hours = timestamp.getHours();
                const minutes = timestamp.getMinutes();

                messageElement.textContent = `${message[0]} to ${message[1]} ${date}/${month}/${year} at ${hours}:${minutes < 10 ? '0' : ''}${minutes}: `;

                // Check if the message content is a URL
                if (validURL(message[2])) {
                    // If the URL is an image/gif
                    if (/\.(gif|jpe?g|tiff?|png|webp|bmp)$/i.test(message[2])) {
                        const img = document.createElement('img');
                        img.src = message[2];
                        img.style.maxWidth= '852px';
                        img.style.maxHeight= '480px';
                        messageElement.appendChild(img);
                    }
                    // If the URL is a YouTube video
                    else if (/youtu\.?be/i.test(message[2])) {
                        const iframe = document.createElement('iframe');
                        iframe.src = convertYouTubeURL(message[2]);
                        iframe.style.width = '852px';
                        iframe.style.height = '480px';
                        messageElement.appendChild(iframe);
                    }
                    // Any other URL can just be linked
                    else {
                        const link = document.createElement('a');
                        link.href = message[2];
                        link.textContent = message[2];
                        messageElement.appendChild(link);
                    }
                } else {
                    // If not a URL, just add the message text
                    messageElement.textContent += message[2];
                }

                messagesDiv.appendChild(messageElement);
                lastMessage = message;
            }
        });
}

// Function to validate a URL
function validURL(str) {
    const pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
    return !!pattern.test(str);
}

// Function to convert a YouTube URL to an embed URL
function convertYouTubeURL(url) {
    return url.replace(/watch\?v=/, 'embed/');
}

socket.on('new_message', function(data) {
    // Append the new message to the message list
    appendMessage(data);
});
onload(fetchConversations)
onload(fetchMessages())
setInterval(fetchConversations, 5000);

