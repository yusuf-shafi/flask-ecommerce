document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResult = document.getElementById('searchResult');

    searchInput.addEventListener('input', function() {
        const searchText = searchInput.value.toLowerCase();
        let message = '';

        if (searchText.includes('shoes')) {
            message = 'Found shoes!';
        } else if (searchText.includes('tops')) {
            message = 'Found tops!';
        } else if (searchText.includes('bottoms')) {
            message = 'Found bottoms!';
        } else {
            message = 'No matching item found.';
        }

        searchResult.textContent = message;
    });
});
