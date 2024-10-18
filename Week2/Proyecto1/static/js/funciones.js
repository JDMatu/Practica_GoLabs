document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatBox = document.getElementById('chatBox');
    const chatInput = document.getElementById('chatInput');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = chatInput.value;
        chatInput.value = '';

        const userMessage = document.createElement('div');
        userMessage.classList.add('d-flex', 'flex-row-reverse', 'align-items-center', 'text-end', 'user');
        userMessage.innerHTML = `<p ><span><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 50 50"><path fill="currentColor" d="M25.1 42c-9.4 0-17-7.6-17-17s7.6-17 17-17s17 7.6 17 17s-7.7 17-17 17m0-32c-8.3 0-15 6.7-15 15s6.7 15 15 15s15-6.7 15-15s-6.8-15-15-15"/><path fill="currentColor" d="m15.3 37.3l-1.8-.8c.5-1.2 2.1-1.9 3.8-2.7s3.8-1.7 3.8-2.8v-1.5c-.6-.5-1.6-1.6-1.8-3.2c-.5-.5-1.3-1.4-1.3-2.6c0-.7.3-1.3.5-1.7c-.2-.8-.4-2.3-.4-3.5c0-3.9 2.7-6.5 7-6.5c1.2 0 2.7.3 3.5 1.2c1.9.4 3.5 2.6 3.5 5.3c0 1.7-.3 3.1-.5 3.8c.2.3.4.8.4 1.4c0 1.3-.7 2.2-1.3 2.6c-.2 1.6-1.1 2.6-1.7 3.1V31c0 .9 1.8 1.6 3.4 2.2c1.9.7 3.9 1.5 4.6 3.1l-1.9.7c-.3-.8-1.9-1.4-3.4-1.9c-2.2-.8-4.7-1.7-4.7-4v-2.6l.5-.3s1.2-.8 1.2-2.4v-.7l.6-.3c.1 0 .6-.3.6-1.1c0-.2-.2-.5-.3-.6l-.4-.4l.2-.5s.5-1.6.5-3.6c0-1.9-1.1-3.3-2-3.3h-.6l-.3-.5c0-.4-.7-.8-1.9-.8c-3.1 0-5 1.7-5 4.5c0 1.3.5 3.5.5 3.5l.1.5l-.4.5c-.1 0-.3.3-.3.7c0 .5.6 1.1.9 1.3l.4.3v.5c0 1.5 1.3 2.3 1.3 2.4l.5.3v2.6c0 2.4-2.6 3.6-5 4.6c-1.1.4-2.6 1.1-2.8 1.6"/></svg>${message}</span></p>`;
        chatBox.appendChild(userMessage);

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        const botMessage = document.createElement('div');
        botMessage.classList.add('d-flex', 'flex-row', 'align-items-center');
        botMessage.innerHTML = `<p><span><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 48 48"><ellipse cx="24" cy="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" rx="9.636" ry="20.5"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M28.818 15.655c9.805 5.66 15.597 13.986 12.936 18.595s-12.767 3.756-22.572-1.905S3.586 18.36 6.247 13.75c1.064-1.843 3.318-2.812 6.267-2.95c4.427-.208 10.42 1.457 16.304 4.855"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M28.818 32.345c-9.805 5.661-19.91 6.514-22.571 1.905s3.13-12.934 12.935-18.595c5.662-3.27 11.424-4.935 15.795-4.871c3.198.046 5.652 1.018 6.777 2.966c2.66 4.609-3.13 12.934-12.936 18.595M20.43 21.251h7.14M19.314 24h9.372m-6.745 2.749h4.118"/></svg>${data.response}</span></p>`;
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;
    });
});