const multiSelectWithoutCtrl = ( elemSelector ) => {

  let options = document.querySelectorAll(`${elemSelector} option`);

  options.forEach(function (element) {
      element.addEventListener("mousedown",
          function (e) {
              e.preventDefault();
              element.parentElement.focus();
              this.selected = !this.selected;
              return false;
          }, false );
  });


}




multiSelectWithoutCtrl('#mySelectInput') /* Can use ID or Class */

document.addEventListener('DOMContentLoaded', function () {
    const genresSelect = document.getElementById('mySelectInput'); // Updated ID
    const getRecommendationsButton = document.getElementById('get-recommendations-button');

    getRecommendationsButton.addEventListener('click', function () {
        const selectedOptions = Array.from(genresSelect.selectedOptions);

        selectedOptions.forEach((option) => {
            option.selected = !option.selected;
        });
    });

    // Find the form element
    const genreForm = document.querySelector('form');
    const artistInput = document.getElementById('searchName');
    const trackInput = document.getElementById('searchTrack');

    genreForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get the selected genres from the select element
        const selectedGenres = Array.from(genresSelect.selectedOptions).map(option => option.value);
        const artistName = artistInput.value;
        const trackName = trackInput.value;

        // Create an object to send as JSON
        const formData = {
            selected_genres: selectedGenres,
            artist_name: artistName,
            track_name: trackName
        };

        // Send the data to Flask using fetch
        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                // Handle success, e.g., redirect to a new page
                const jsonResponse = await response.json();
                window.location.href = '/recommend/result/' + jsonResponse.genre + '/' + jsonResponse.artist + '/' + jsonResponse.track // Change to the desired URL
            } else {
                console.error('Error:', response.status, response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});