let timerInterval;
let isTimerRunning = false;
let timeRemaining = 240;

function incrementScore(element) {
    let score = parseInt(element.innerText);
    element.innerText = score + 1;
}



function updateTimer() {
    if (timeRemaining > 0) {
        timeRemaining--;
        updateTimerDisplay();
    } else {
        clearInterval(timerInterval);
        isTimerRunning = false;
        stopTimerAndHighlight();
    }
}
function stopTimerAndHighlight() {
    clearInterval(timerInterval);  // 停止计时器
    // isTimerRunning = false;
    document.querySelector('.timer').style.backgroundColor = 'red';  // 设置计时器背景为红色
}


function updateTimerDisplay() {
    let minutes = Math.floor(timeRemaining / 60);
    let seconds = timeRemaining % 60;
    document.querySelector('.timer').innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function toggleTimer() {
    if (isTimerRunning) {
        clearInterval(timerInterval);
    } else {
        timerInterval = setInterval(updateTimer, 1000);
    }
    isTimerRunning = !isTimerRunning;
}

function setTimer(minutes, seconds) {
    timeRemaining = minutes * 60 + seconds;
    updateTimerDisplay();
}

function openSettings() {
    let timeInput = prompt("請輸入倒數時間 (格式: MM:SS)", "5:00");
    if (timeInput) {
        let timerParts = timeInput.split(':');
        let minutes = parseInt(timerParts[0]);
        let seconds = parseInt(timerParts[1]);
        if (!isNaN(minutes) && !isNaN(seconds)) {
            setTimer(minutes, seconds);
        } else {
            alert("請輸入有效的時間格式");
        }
    }
}

document.querySelector('.timer').addEventListener('dblclick', function() {
    openSettings();
});

