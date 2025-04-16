function toggleFriends(id) {
    const friendsList = document.getElementById(id);
    friendsList.style.display = (friendsList.style.display === "block") ? "none" : "block";
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
    message.textContent = `${friendUsername} has been removed.`;
}

addFriendBtn.addEventListener('click', function() {
    const friendUsername = friendInput.value.trim();
    message.textContent = '';
    if (friendUsername === '') {
        message.textContent = 'Please enter a username.';
    }
    else if (!existingUsernames.includes(friendUsername)) {
        message.textContent = 'User not found.';
    }
    else if (currentFriends.includes(friendUsername)) {
        message.textContent = 'Already friends.';
    }
    else {
        currentFriends.push(friendUsername);
        const newFriendCard = document.createElement('div');
        newFriendCard.className = 'friend-card';
        newFriendCard.innerHTML = `
            <h3 class="friend-name">${friendUsername}</h3>
            <p class="friend-username">@${friendUsername}</p>
            <p class="puzzles-built">Puzzles Built: 0</p>
            <p class="friend-count">Friends: 0</p>
            <button class="remove-friend-btn" onclick="removeFriend(this)">Remove Friend</button>
        `;
        document.getElementById('jeffrey').appendChild(newFriendCard);
        message.textContent = 'Friend added successfully!';
    }
    friendInput.value = '';
});