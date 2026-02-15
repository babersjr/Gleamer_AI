document.addEventListener('DOMContentLoaded', function() {
    const signInForm = document.getElementById('signInForm');
    const submitBtn = document.querySelector('.submit-btn');

    // Form validation and submission
    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();

        // Get all form inputs
        const fullName = document.getElementById('FullName').value;
        const email = document.getElementById('EmailAddress').value;
        const password = document.getElementById('password').value;
        const phone = document.getElementById('PhoneNumber').value;
        const birthDate = document.getElementById('BirthDate').value;
        const address = document.getElementById('Address').value;
        const country = document.getElementById('Country').value;
        const city = document.getElementById('City').value;
        const gender = document.querySelector('input[name="gender"]:checked')?.value;

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showAlert('Please enter a valid email address', 'error');
            return;
        }

        // Validate phone number (basic validation)
        const phoneRegex = /^\d{11}$/;
        if (!phoneRegex.test(phone)) {
            showAlert('Please enter a valid phone number (11 digits)', 'error');
            return;
        }

        // Check if all required fields are filled
        if (!fullName || !email || !password || !phone || !birthDate || 
            !address || !country || !city || !gender) {
            showAlert('Please fill in all required fields', 'error');
            return;
        }

        // Create user data object
        const userData = {
            fullName,
            email,
            password,
            phone,
            birthDate,
            address,
            country,
            city,
            gender
        };

        // Send registration data to server
        registerUser(userData);
    });

    // Function to show alerts
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        // Style the alert
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.padding = '15px 30px';
        alertDiv.style.borderRadius = '5px';
        alertDiv.style.zIndex = '1000';
        
        if (type === 'error') {
            alertDiv.style.backgroundColor = '#ff4444';
        } else {
            alertDiv.style.backgroundColor = '#00C851';
        }
        alertDiv.style.color = 'white';

        document.body.appendChild(alertDiv);

        // Remove alert after 3 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    // Function to handle user registration
    // Add this after your DOMContentLoaded event listener starts
    const userPhoto = document.getElementById('userPhoto');
    const photoPreview = document.getElementById('photoPreview');

    userPhoto.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                photoPreview.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });

    // Update your registerUser function to include the photo
    async function registerUser(userData) {
        const formData = new FormData();
        
        // Add all user data to FormData
        Object.keys(userData).forEach(key => {
            formData.append(key, userData[key]);
        });
        
        // Add the photo file
        const photoFile = document.getElementById('userPhoto').files[0];
        if (photoFile) {
            formData.append('photo', photoFile);
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                body: formData // Send as FormData instead of JSON
            });

            const data = await response.json();

            if (response.ok) {
                showAlert('Registration successful!', 'success');
                // Redirect to login page after successful registration
                setTimeout(() => {
                    window.location.href = '/sign_in';
                }, 2000);
            } else {
                showAlert(data.message || 'Registration failed', 'error');
            }
        } catch (error) {
            showAlert('An error occurred. Please try again later.', 'error');
            console.error('Registration error:', error);
        }
    }

    // Add input validation on blur
    document.getElementById('EmailAddress').addEventListener('blur', function() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(this.value) && this.value !== '') {
            this.style.borderColor = '#ff4444';
        } else {
            this.style.borderColor = '#eaeaea';
        }
    });

    document.getElementById('PhoneNumber').addEventListener('blur', function() {
        const phoneRegex = /^\d{11}$/;
        if (!phoneRegex.test(this.value) && this.value !== '') {
            this.style.borderColor = '#ff4444';
        } else {
            this.style.borderColor = '#eaeaea';
        }
    });
});