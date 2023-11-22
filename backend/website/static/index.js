function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/notes"
    });
}

function addNewChatBox(id) {

    var html = `
        <input type="text" id='chatUser' name='chatUser' required>
        <button class="btn btn-primary" onClick="newChat()">Chat</button>
    `;
    
    document.getElementById(id).innerHTML = html;
}
/*
function newChat() {
    username = document.getElementById('chatUser').value;
    fetch('/new-chat', {
        method: 'POST',
        body: JSON.stringify({username: username}),
    }).then((_res) => {
        window.location.href = "/chat"
    });
}
*/

function addNote() {
    noteText = document.getElementById('note').value;
    fetch('/new-note', {
        method: 'POST',
        body: JSON.stringify({noteText: noteText}),
    }).then((_res) => {
        window.location.href = "/notes"
    });
}
