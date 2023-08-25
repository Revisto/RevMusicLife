  // Function to fetch API and update HTML
function convertMsToMMSS(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  const formattedMinutes = String(minutes).padStart(2, '0');
  const formattedSeconds = String(seconds).padStart(2, '0');

  return `${formattedMinutes}:${formattedSeconds}`;
}
function togglePauseResume(pauseState) {
  const pauseButton = document.getElementById('pauseButton'); // Replace with the ID of your pause button element
  const resumeButton = document.getElementById('resumeButton'); // Replace with the ID of your resume button element

  if (pauseState) {
    pauseButton.style.display = 'inline';
    resumeButton.style.display = 'none';
  } else {
    pauseButton.style.display = 'none';
    resumeButton.style.display = 'inline';
  }
}
function fetchDataAndUpdate() {
  fetch('/api/currently-playing') // Replace with your API endpoint
    .then(response => response.json())
    .then(data => {
      // Update HTML content
      document.getElementsByClassName('progress__duration')[0].innerText = convertMsToMMSS(data.duration_ms - data.progress_ms);
      document.getElementsByClassName('progress__time')[0].innerText = convertMsToMMSS(data.progress_ms);
      document.getElementsByClassName('progress__current')[0].style.width = ((data.progress_ms / data.duration_ms) * 100) + "%";
      document.getElementsByClassName('album-info__track')[0].innerText = data.track_name;
      document.getElementsByClassName('album-info__name')[0].innerText = data.artists;
      document.getElementById('songLink').href = data.link;
      togglePauseResume(data.is_playing)
      document.getElementsByClassName('player-cover__item')[0].style.backgroundImage = `url(${data.cover_url})`;
    })
    .catch(error => {
      console.log('Error:', error);
    });
}

// Fetch data every second
setInterval(fetchDataAndUpdate, 1000);