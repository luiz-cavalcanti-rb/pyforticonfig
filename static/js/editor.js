// editor.js

var editor = CodeMirror.fromTextArea(document.getElementById('editor-content'), {
    lineNumbers: true,
    mode: 'javascript' // You can change the mode as per your file type
});

var initialContent = editor.getValue();

// Function to handle close button click
function handleCloseButtonClick() {
    if (hasContentChanged()) {
        var confirmSave = confirm("There are unsaved changes. Do you want to save before closing?");
        if (confirmSave) {
            // Save the content and close the editor window if saving is successful
            saveContent(closeEditorWindow);
        } else {
            // If the user chooses not to save, close the editor window directly
            closeEditorWindow();
        }
    } else {
        // If there are no unsaved changes, close the editor window directly
        closeEditorWindow();
    }
}

// Function to save content
function saveContent(callback) {
    var content = editor.getValue();
    var filename = "{{ filename }}"; // Get the filename from the template

    // Send an AJAX request to the server to save the content
    fetch('/save_file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            filename: filename,
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If saving is successful, execute the callback function (closeEditorWindow)
            if (typeof callback === 'function') {
                callback();
            }
            alert('Content saved successfully!');
        } else {
            alert('Failed to save content: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving content.');
    });
}

// Function to close the editor window
function closeEditorWindow() {
    // Redirect to another page or close the current window
    // window.location.href = "/"; // Redirect to the homepage or any other desired page
    window.close();
}

// Function to undo changes
function undoChanges() {
    editor.undo();
}

// Function to check if content has changed
function hasContentChanged() {
    return editor.getValue() !== initialContent;
}

// Event listener for save button
document.getElementById('save-button').addEventListener('click', saveContent);

// Event listener for undo button
document.getElementById('undo-button').addEventListener('click', undoChanges);

// Event listener for close button
document.getElementById('close-button').addEventListener('click', handleCloseButtonClick);
