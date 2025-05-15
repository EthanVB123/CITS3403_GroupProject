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

function removeFriend(button, username) {
    fetch('/remove-friend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json().then(data => ({status: response.status, body: data})))
    .then(({status, body}) => {
        if (status === 200) {
            const friendCard = button.parentElement;
            friendCard.remove();
            message.style.color = 'green';
            message.style.fontWeight = 'bold';
            message.textContent = `${username} has been removed.`;
        } else {
            message.style.color = '#d00';
            message.style.fontWeight = 'normal';
            message.textContent = body.error || 'Error removing friend.';
        }
    });
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
                <p class="puzzle-score">Puzzle Score: ${body.userScore}</p>
                <button class="remove-friend-btn absolute right-2 top-2 bg-red-400 border border-red-900 hover:bg-red-900 hover:text-white p-0.5 rounded duration-200"
                    onclick="removeFriend(this, '${body.username}'); event.stopPropagation();">Remove
                    Friend</button>
            `;
            newFriendCard.classList.add("friend-card" ,"bg-zinc-100", "border", "border-black", "rounded", "hover:bg-zinc-200", "relative", "p-2", "mb-0.5")
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
            dropdown.style.top = friendInput.offsetTop + friendInput.offsetHeight + 'px';
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