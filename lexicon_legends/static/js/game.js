document.addEventListener('DOMContentLoaded', () => {
    let players = py_players;
    const socket = io();
    const roomKey = py_roomKey;
    const current_user = py_currentUser;
    const playersElement = document.getElementById('players');
    const timerElement = document.getElementById('timer');
    const wordInput = document.getElementById('wordInput');
    const submitWord = document.getElementById('submitWord');
    const typedWordsTable = document.getElementById('typedWordsTable');
    const started = document.getElementById('started');
    const ended = document.getElementById('ended');
    const sameWord = document.getElementById('same_word');
    const randomWord = document.getElementById('random_word').textContent;

    socket.emit('join', {room_key: roomKey});

    socket.on('start_game', () => {
        startTimer();
    });

    socket.on('update_players', (data) => {
        players = data.players;
        playersElement.textContent = `Players: ${players}`;
    });

    socket.on('update_timer', (data) => {
        timerElement.textContent = `timer: ${data.time}s`;
    });

    window.addEventListener('beforeunload', () => {
        socket.emit('leave', {room_key: roomKey});
    });

    function startTimer() {
        let time = 30;
        started.style.display = 'none';
        wordInput.style.display = 'block';
        timerElement.style.display = 'block';
        submitWord.style.display = 'block';

        setInterval(() => {
            time--;

            if (time < 0){
                wordInput.style.display = 'none';
                ended.style.display = 'block';
                submitWord.style.display = 'none';

                var id = document.getElementById("winner");
                var id2 = document.getElementById("score1");
                var id3 = document.getElementById("score1");

                id.style.display = "block";
                id2.style.display = "block";
                id3.style.display = "block";

                return;

            };
            socket.emit('sync_timer', {room_key: roomKey, time: time});
        }, 1000);
    }

    submitWord.addEventListener('click', () => {
        const typedWord = wordInput.value.trim();

        if (wordInput.value.toLowerCase() == randomWord.toLowerCase()) {
            sameWord.style.display = 'block';
        }
       
        if (typedWord) {
            socket.emit('send_word', { room_key: roomKey, word: typedWord, sender: current_user, 
                winner: '', wscore: 0,
                loser: '', lscore: 0,
            });
            wordInput.value = '';
        }
    });

    socket.on('receive_word', (data) => {
        const sender = data.sender;
        const word = data.word;
        const winner = data.winner;
        const wscore = data.wscore;
        const lscore = data.lscore;
    
        let senderColumn = typedWordsTable.querySelector(`[data-sender="${sender}"]`);
    
        if (!senderColumn) {
            senderColumn = document.createElement('td');
            senderColumn.setAttribute('data-sender', sender);
            senderColumn.style.verticalAlign = 'top';
    
            const senderName = document.createElement('div');
            senderName.textContent = sender;
            senderName.style.color = sender === current_user ? '#1ec83b' : '#9e1912';
            senderColumn.appendChild(senderName);
    
            typedWordsTable.appendChild(senderColumn);
        }
    
        const wordCell = document.createElement('div');
        wordCell.textContent = word;
        wordCell.style.color = '#FFFFFF';
        senderColumn.appendChild(wordCell);
    
        document.getElementById("win").innerHTML = winner;

        if (winner == current_user){
            document.getElementById("your_score").innerHTML = wscore;
            document.getElementById("opps_score").innerHTML = lscore;
        }
        else{
            document.getElementById("your_score").innerHTML = lscore;
            document.getElementById("opps_score").innerHTML = wscore;
        }

    });

});