// script.js

function toggleFiles() {
    var filesContent = document.getElementById("files-content");
    filesContent.classList.toggle("hide");
}

function openEditor(filename) {
    var url = '/edit?filename=' + encodeURIComponent(filename);
    window.open(url, 'editor.html', 'width=800,height=600');
}