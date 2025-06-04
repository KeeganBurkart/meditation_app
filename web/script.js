let timer;
let remainingSeconds = 0;

const durationInput = document.getElementById('duration');
const moodBeforeInput = document.getElementById('moodBefore');
const moodAfterInput = document.getElementById('moodAfter');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const display = document.getElementById('display');

function updateDisplay() {
    const minutes = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
    const seconds = String(remainingSeconds % 60).padStart(2, '0');
    display.textContent = `${minutes}:${seconds}`;
}

function tick() {
    if (remainingSeconds > 0) {
        remainingSeconds -= 1;
        updateDisplay();
    } else {
        finishSession();
    }
}

function startTimer() {
    remainingSeconds = parseInt(durationInput.value, 10) * 60;
    updateDisplay();
    timer = setInterval(tick, 1000);
    startBtn.disabled = true;
    stopBtn.disabled = false;
}

function stopTimer() {
    clearInterval(timer);
    startBtn.disabled = false;
    stopBtn.disabled = true;
}

function finishSession() {
    stopTimer();
    const session = {
        duration: parseInt(durationInput.value, 10) * 60,
        start: Date.now() - (parseInt(durationInput.value, 10) * 60 - remainingSeconds) * 1000,
        end: Date.now(),
        moodBefore: parseInt(moodBeforeInput.value, 10) || null,
        moodAfter: parseInt(moodAfterInput.value, 10) || null
    };
    const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
    sessions.push(session);
    localStorage.setItem('sessions', JSON.stringify(sessions));
    alert('Session complete!');
}

startBtn.addEventListener('click', startTimer);
stopBtn.addEventListener('click', stopTimer);
