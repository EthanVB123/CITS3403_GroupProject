function toggleFriendDetails(card) {
    const friendDetails = card.querySelector('.friend-details');
    if (details) {
        details.style.display = (details.style.display === "block") ? "none" : "block";
    }
}

// dummy data
const existingUsernames = ['clashroyale', 'ryankoo', 'elizabethshibu', 'ethanvanbruchem', 'johnsmith', 'clashofclans'];
const currentFriends = ['ryankoo', 'elizabethshibu', 'ethanvanbruchem'];

const friendInput = document.getElementById('friend-input');
const message = document.getElementById('message');
const addFriendBtn = document.getElementById('add-friend-btn');

function removeFriend(button) {
    const friendCard = button.parentElement;
    const friendUsername = friendCard.querySelector('.friend-username').textContent.trim().slice(1);
    friendCard.remove();
    const index = currentFriends.indexOf(friendUsername);
    if (index !== -1) {
        currentFriends.splice(index, 1);
    }
    message.style.color = '#d00';
    message.style.fontWeight = 'normal';
    message.textContent = `${friendUsername} has been removed.`;
}

addFriendBtn.addEventListener('click', function() {
    const friendUsername = friendInput.value.trim();
    message.style.color = '#d00';
    message.style.fontWeight = 'normal';
    message.textContent = '';
    if (friendUsername === '') {
        message.textContent = 'Please enter a username.';
        return;
    }
    fetch('/add-friend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: friendUsername })
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(({status, body}) => {
        if (status === 200) {
            // Add friend card to the list
            const newFriendCard = document.createElement('div');
            newFriendCard.className = 'friend-card';
            newFriendCard.innerHTML = `
                <h3 class="friend-name">${body.username}</h3>
                <p class="friend-username">@${body.username}</p>
                <p class="puzzles-built">Puzzles Built: 0</p>
                <p class="friend-count">Friends: 0</p>
                <button class="remove-friend-btn" onclick="removeFriend(this, '${body.username}')">Remove Friend</button>
            `;
            document.getElementById('friends-section').appendChild(newFriendCard);
            message.textContent = 'Friend added successfully!';
            message.style.color = 'green';
            message.style.fontWeight = 'bold';
        } else {
            message.textContent = body.error || 'Error adding friend.';
        }
    });
    friendInput.value = '';
});