function toggleFriendDetails(card) {
    const friendDetails = card.querySelector('.friend-details');
    if (details) {
        details.style.display = (details.style.display === "block") ? "none" : "block";
    }
}

// dummy data
//const existingUsernames = ['clashroyale', 'ryankoo', 'elizabethshibu', 'ethanvanbruchem', 'johnsmith', 'clashofclans'];
//const currentFriends = ['ryankoo', 'elizabethshibu', 'ethanvanbruchem'];

const friendInput = document.getElementById('friend-input');
const message = document.getElementById('message');
const addFriendBtn = document.getElementById('add-friend-btn');
let dropdown = null;

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

friendInput.addEventListener('input', function() {
    const query = friendInput.value.trim();
    if (query.length === 0) {
        if (dropdown) dropdown.remove();
        return;
    }
    fetch(`/search-users?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(usernames => {
            if (dropdown) dropdown.remove();
            dropdown = document.createElement('div');
            dropdown.className = 'dropdown';
            dropdown.style.position = 'absolute';
            dropdown.style.background = '#fff';
            dropdown.style.color = '#000';
            dropdown.style.border = '1px solid #ccc';
            dropdown.style.width = friendInput.offsetWidth + 'px';
            dropdown.style.zIndex = 1000;
            usernames.forEach(username => {
                const option = document.createElement('div');
                option.className = 'dropdown-option';
                option.textContent = username;
                option.style.padding = '5px 10px';
                option.style.cursor = 'pointer';
                option.addEventListener('mousedown', function(e) {
                    e.preventDefault();
                    friendInput.value = username;
                    dropdown.remove();
                });
                dropdown.appendChild(option);
            });
            friendInput.parentNode.appendChild(dropdown);
        });
});

// Hide dropdown when clicking outside
document.addEventListener('click', function(e) {
    if (dropdown && !friendInput.contains(e.target)) {
        dropdown.remove();
    }
});