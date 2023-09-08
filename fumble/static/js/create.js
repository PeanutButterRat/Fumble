const openPopupButton = document.getElementById('openPopup');
const closePopupButton = document.getElementById('closePopup');
const popup = document.getElementById('popup');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');

openPopupButton.addEventListener('click', () => {
    popup.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
    popup.style.display = 'none';
});

searchInput.addEventListener('input', () => {
    const searchTerm = searchInput.value.toLowerCase();
    const usernames = ['user1', 'user2', 'user3', 'user4'];
    const filteredUsernames = usernames.filter(username => username.toLowerCase().includes(searchTerm));
    displaySearchResults(filteredUsernames);
});


function displaySearchResults(results) {
    searchResults.innerHTML = '';
    results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.textContent = result;
        searchResults.appendChild(listItem);
    });
}