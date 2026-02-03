const pdfInput = document.getElementById('pdfInput');
const chatbox = document.getElementById('chatbox');
const sendBtn = document.getElementById('sendBtn');
const loader = document.getElementById('loader');
const outputSection = document.getElementById('outputSection');
const output = document.getElementById('output');
const fileName = document.getElementById('fileName');

// const API_URL = 'http://127.0.0.1:8000';

pdfInput.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        fileName.textContent = `✓ Selected: ${e.target.files[0].name}`;
        fileName.classList.add('active');
    } else {
        fileName.classList.remove('active');
    }
});

sendBtn.addEventListener('click', async function(e) {
    // Prevent any default behavior
    e.preventDefault();
    e.stopPropagation();
    
    const file = pdfInput.files[0];
    const question = chatbox.value.trim();

    if (!file) {
        alert('Please upload a PDF file first!');
        return;
    }

    if (!question) {
        alert('Please enter a question or prompt!');
        return;
    }

    loader.classList.add('active');
    outputSection.classList.remove('active');
    sendBtn.disabled = true;

    // Send the user's uploaded PDF dynamically
    const formData = new FormData();
    formData.append('file', file);
    formData.append('text', question);

    try {
        const response = await fetch(`/answer`, {
            method: 'POST',
            body: formData
        });
        
        // Parse as JSON (your backend returns JSON)
        const data = await response.json();
        console.log(data);
        
        // Display the text from the response
        output.textContent = data.text;
        outputSection.classList.add('active');

    } catch (error) {
        console.error('Error:', error);
        output.textContent = `Error: ${error.message}`;
        outputSection.classList.add('active');
    } finally {
        loader.classList.remove('active');
        sendBtn.disabled = false;
    }
});