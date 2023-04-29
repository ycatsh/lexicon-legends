var duration_seconds = 30

var stored_duration = localStorage.getItem("remaining_time");
if (stored_duration !== null) {
  duration_seconds = parseInt(stored_duration);
}

var timer = document.getElementById("timer");
timer.innerHTML = 'Timer: '+ duration_seconds;

function updateTimer() {
    timer.innerHTML = 'Timer: '+ duration_seconds;
    duration_seconds--;

    localStorage.setItem("remaining_time", duration_seconds.toString());

    if (duration_seconds <= 0) {
        clearInterval(timer_interval);
        timer.innerHTML = "Game Over";
        document.getElementById("word_form").disabled = true;
    }
}

var timer_interval = setInterval(updateTimer, 1000);