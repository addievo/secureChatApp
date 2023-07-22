function fetchMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(messages=> {
            //clear old messages
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '';

            for (let message of messages){
                const p = document.createElement('p');
                p.textContent = message.content;
                messagesDiv.appendChild(p);
            }
        }
    );
}

setInterval(fetchMessages, 1000);