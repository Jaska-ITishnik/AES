// root Encryption Visualizer - UI Interactions Only
document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navLinks = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('data-section');

            // Update active link
            navLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');

            // Show target section
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });
        });
    });

    // Tab navigation
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) return;

            const targetTab = this.getAttribute('data-tab');

            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Show target tab content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${targetTab}-tab`) {
                    content.classList.add('active');
                }
            });
        });
    });

    // Round navigation
    const prevRoundBtn = document.getElementById('prev-round');
    const nextRoundBtn = document.getElementById('next-round');

    if (prevRoundBtn && nextRoundBtn) {
        prevRoundBtn.addEventListener('click', function() {
            if (!this.disabled) {
                // Submit form with previous round
                navigateToRound('prev');
            }
        });

        nextRoundBtn.addEventListener('click', function() {
            if (!this.disabled) {
                // Submit form with next round
                navigateToRound('next');
            }
        });
    }

    function navigateToRound(direction) {
        // Create a hidden form to navigate to a different round
        const form = document.createElement('form');
        form.method = 'post';
        form.action = window.location.href;

        // Add CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        // Add current values
        const plaintext = document.getElementById('plaintext').value;
        const plaintextInput = document.createElement('input');
        plaintextInput.type = 'hidden';
        plaintextInput.name = 'plaintext';
        plaintextInput.value = plaintext;
        form.appendChild(plaintextInput);

        const key = document.getElementById('key').value;
        const keyInput = document.createElement('input');
        keyInput.type = 'hidden';
        keyInput.name = 'key';
        keyInput.value = key;
        form.appendChild(keyInput);

        // Add direction
        const directionInput = document.createElement('input');
        directionInput.type = 'hidden';
        directionInput.name = 'round_direction';
        directionInput.value = direction;
        form.appendChild(directionInput);

        // Add current round
        const currentRound = document.getElementById('current-round').textContent;
        const roundInput = document.createElement('input');
        roundInput.type = 'hidden';
        roundInput.name = 'current_round';
        roundInput.value = currentRound;
        form.appendChild(roundInput);

        // Submit the form
        document.body.appendChild(form);
        form.submit();
    }

    // Hex input toggle
    const hexInputCheckbox = document.getElementById('hex-input');
    if (hexInputCheckbox) {
        hexInputCheckbox.addEventListener('change', function() {
            const helpText = document.querySelector('.help-text');
            if (this.checked) {
                helpText.textContent = 'Enter values in hexadecimal format (e.g., 3243f6a8885a308d313198a2e0370734)';
            } else {
                helpText.textContent = 'Enter text values (will be converted to hex)';
            }
        });
    }

    // Input validation
    const plaintextInput = document.getElementById('plaintext');
    const keyInput = document.getElementById('key');

    if (plaintextInput && keyInput && hexInputCheckbox) {
        function validateHexInput(input) {
            if (hexInputCheckbox.checked && input.value) {
                if (!/^[0-9a-fA-F]*$/.test(input.value)) {
                    input.classList.add('error');
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.textContent = 'Please enter valid hexadecimal characters (0-9, a-f)';

                    // Remove any existing error message
                    const existingError = input.parentNode.querySelector('.error-message');
                    if (existingError) {
                        input.parentNode.removeChild(existingError);
                    }

                    input.parentNode.appendChild(errorDiv);
                    return false;
                } else {
                    input.classList.remove('error');
                    const existingError = input.parentNode.querySelector('.error-message');
                    if (existingError) {
                        input.parentNode.removeChild(existingError);
                    }
                    return true;
                }
            }
            return true;
        }

        plaintextInput.addEventListener('input', function() {
            validateHexInput(this);
        });

        keyInput.addEventListener('input', function() {
            validateHexInput(this);
        });

        // Form validation
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                let isValid = true;

                if (!validateHexInput(plaintextInput)) {
                    isValid = false;
                }

                if (!validateHexInput(keyInput)) {
                    isValid = false;
                }

                if (!isValid) {
                    e.preventDefault();
                }
            });
        }
    }
});