const ENTER_KEYCODE = 13;
const openPopupButton = document.getElementById('openPopup');
const closePopupButton = document.getElementById('closePopup');
const popup = document.getElementById('popup');
const searchBar = document.getElementById('searchBar');
const searchResults = document.getElementById('searchResults');
const chats = document.getElementById('');
let usernames = [];

openPopupButton.addEventListener('click', () => {
    popup.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
    popup.style.display = 'none';
});

searchBar.addEventListener('keydown', () => {
    if (event.keyCode == ENTER_KEYCODE) {
        getSearchResults(usernames);
    }
});

searchBar.addEventListener('input', () => {
    updateDisplayedSearchResults();
});


function updateDisplayedSearchResults() {
    searchResults.innerHTML = '';
    const filteredUsernames = usernames.filter(username => username.startsWith(searchBar.value));
    filteredUsernames.forEach(username => {
        const listItem = document.createElement('li');
        listItem.textContent = username;
        listItem.addEventListener('click', () => {
            joinChat(username);
        });
        searchResults.appendChild(listItem);
    });
}


async function getSearchResults(prefix) {
    const response = await fetch(`/usernames?prefix=${prefix}`);
    if (response.ok) {
        const results = await response.json();
        usernames = results['usernames'];
        updateDisplayedSearchResults();
    } else {
        console.log('Unable to fetch usernames.')
    }
}


async function joinChat(username) {
    const response = await fetch(`/new?username=${username}`);
    if (response.ok) {
        const results = await response.json();
        console.log(results)
    } else {
        console.log(`Unable to create chat with ${username}`)
    }
}
