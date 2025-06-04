function loadUser() {
    const stored = localStorage.getItem('user');
    if (stored) {
        return JSON.parse(stored);
    }
    const user = {
        name: 'Meditator',
        bio: 'Mindful living enthusiast.',
        photoUrl: 'https://via.placeholder.com/150'
    };
    localStorage.setItem('user', JSON.stringify(user));
    return user;
}

function loadSessions() {
    return JSON.parse(localStorage.getItem('sessions') || '[]');
}

function calculateTotalMinutes(sessions) {
    return Math.round(sessions.reduce((t, s) => t + s.duration / 60, 0));
}

function calculateSessionCount(sessions) {
    return sessions.length;
}

function calculateCurrentStreak(sessions) {
    if (sessions.length === 0) return 0;
    const days = Array.from(new Set(
        sessions.map(s => new Date(s.end).toDateString())
    )).sort((a, b) => new Date(b) - new Date(a));
    let streak = 1;
    for (let i = 1; i < days.length; i++) {
        const prev = new Date(days[i - 1]);
        const curr = new Date(days[i]);
        if (prev - curr === 86400000) {
            streak += 1;
        } else {
            break;
        }
    }
    return streak;
}

function render() {
    const user = loadUser();
    const sessions = loadSessions();

    document.getElementById('profilePhoto').src = user.photoUrl;
    document.getElementById('profileName').textContent = user.name;
    document.getElementById('profileBio').textContent = user.bio;
    document.getElementById('totalMinutes').textContent = calculateTotalMinutes(sessions);
    document.getElementById('sessionCount').textContent = calculateSessionCount(sessions);
    document.getElementById('currentStreak').textContent = calculateCurrentStreak(sessions);

    const list = document.getElementById('activityList');
    list.innerHTML = '';
    sessions
        .slice()
        .sort((a, b) => new Date(b.end) - new Date(a.end))
        .forEach(s => {
            const li = document.createElement('li');
            const date = new Date(s.end).toLocaleString();
            const minutes = Math.round(s.duration / 60);
            li.textContent = `${date} - ${minutes} min`;
            list.appendChild(li);
        });
}

document.addEventListener('DOMContentLoaded', render);
