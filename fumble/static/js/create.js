const ENTER_KEYCODE = 13;
const openPopupButton = document.getElementById('openPopup');
const closePopupButton = document.getElementById('closePopup');
const popup = document.getElementById('popup');
const searchInput = document.getElementById('searchBar');
const searchResults = document.getElementById('searchResults');
let usernames = [];

openPopupButton.addEventListener('click', () => {
    popup.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
    popup.style.display = 'none';
});

searchInput.addEventListener('keydown', () => {
    if (event.keyCode == ENTER_KEYCODE) {
        updateSearchResults(usernames);
    } else {
        const filteredUsernames = usernames.filter(username => username.includes(searchTerm));
        displaySearchResults(filteredUsernames);
    }
});


function displaySearchResults() {
    searchResults.innerHTML = '';
    usernames.forEach(result => {
        const listItem = document.createElement('li');
        listItem.textContent = result;
        searchResults.appendChild(listItem);
    });
}


async function updateSearchResults(prefix) {
    const response = await fetch(`/usernames?prefix=${prefix}`);
    if (response.ok) {
        const results = await response.json();
        console.log(results)
        usernames = results['usernames'];
        displaySearchResults();
    } else {
        console.log('Unable to fetch usernames.')
    }
}