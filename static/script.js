function fetchMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(decrypted_messages => {
            //clear old messages
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '';

            for (let message of decrypted_messages){
                const p = document.createElement('p');
                // Assuming the decrypted_messages array has the format (sender_username, receiver_username, decrypted_content)
                p.textContent = `From ${message[0]}: ${message[2]}`; // Display the sender's name and the decrypted content
                messagesDiv.appendChild(p);
            }
        });
}

setInterval(fetchMessages, 1000);
