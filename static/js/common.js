function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

class ApiError extends Error {
    constructor(message, fieldErrors = {}) {
        super(message);
        this.fieldErrors = fieldErrors;
    }
}

function clearFieldErrors(form) {
    form.querySelectorAll('.js-field-error').forEach(el => el.remove());
}

function showFieldErrors(form, errors = {}) {
    for (const [name, messages] of Object.entries(errors)) {
        const input = form.elements[name];
        if (!input || !Array.isArray(messages)) continue;
        const note = document.createElement('p');
        note.className = 'form-error js-field-error';
        note.textContent = messages.join(' ');
        input.closest('.form-group')?.appendChild(note);
    }
}