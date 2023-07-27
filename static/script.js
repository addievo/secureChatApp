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

document.getElementById('message').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) { // keyCode for Enter key
        event.preventDefault(); // Prevent newline being added to textarea
        document.getElementById('send-message-form').dispatchEvent(new Event('submit', { cancelable: true })); // Trigger form submission
    }
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
    var reader = new FileReader();
    reader.onloadend = function() {
        var base64data = reader.result;
        uploadToImgur(base64data);
    }
    reader.readAsDataURL(file);
});

function uploadToImgur(base64data) {
    var apiUrl = 'https://api.imgur.com/3/image';
    var imageData = base64data.split(',')[1];
    console.log(imageData); // Add this line to debug
    var settings = {
        async: false,
        crossDomain: true,
        processData: false,
        method: 'POST',
        headers: {
            Authorization: '5b588327c957f90',
            Accept: 'application/json'
        },
        data: {
            image: imageData
        }
    };

    $.ajax(apiUrl, settings).done(function(response) {
        var messageInput = document.getElementById('message');
        messageInput.value += response.data.link;
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



setInterval(fetchConversations, 5000);
setInterval(fetchMessages, 2000); // Fetch messages every second

