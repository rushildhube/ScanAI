// Modern Dental AI Application JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname;
    
    // Initialize the application
    initializeApp();
    
    // Route to appropriate page handler
    if (currentPage.includes('/login')) {
        handleAuthPage();
    } else if (currentPage.includes('/dashboard')) {
        handleDashboardPage();
    } else {
        handleLandingPage();
    }
});

// Global application initialization
function initializeApp() {
    // Initialize global error handling
    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    
    // Initialize loading states
    initializeLoadingStates();
    
    // Initialize notification system
    initializeNotificationSystem();
    
    // Initialize smooth scrolling for anchor links
    initializeSmoothScrolling();
    
    // Initialize navbar scroll effects
    initializeNavbarEffects();
    
    console.log('ScanAI Application initialized successfully');
}

// Global error handlers
function handleGlobalError(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred. Please refresh and try again.', 'error');
}

function handleUnhandledRejection(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('A network error occurred. Please check your connection.', 'error');
}

// Landing page handler
function handleLandingPage() {
    // Add scroll-based animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe step cards for animation
    document.querySelectorAll('.step-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });
    
    // Add parallax effect to hero background
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero-section::before');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
}

// Navbar scroll effects
function initializeNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        // Add/remove scrolled class
        if (currentScrollY > 50) {
            navbar.classList.add('scrolled');
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
        } else {
            navbar.classList.remove('scrolled');
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
        
        // Hide/show navbar on scroll
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Enhanced notification system
function initializeNotificationSystem() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notification-container')) {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 100px;
            right: 1rem;
            z-index: 10000;
            pointer-events: none;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        background: ${getNotificationColor(type).bg};
        color: ${getNotificationColor(type).text};
        border: 2px solid ${getNotificationColor(type).border};
        padding: 1rem 1.5rem;
        margin-bottom: 0.75rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        pointer-events: auto;
        transform: translateX(100%);
        transition: all 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 500;
        font-size: 0.9rem;
        animation: slideInRight 0.3s ease-out forwards;
    `;
    
    notification.innerHTML = `
        <span style="font-size: 1.2rem;">${getNotificationIcon(type)}</span>
        <span style="flex: 1;">${message}</span>
        <button onclick="this.parentElement.remove()" style="
            background: none;
            border: none;
            color: inherit;
            font-size: 1.2rem;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
            padding: 0.25rem;
            border-radius: 0.25rem;
        " onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'">×</button>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }
}

function getNotificationColor(type) {
    const colors = {
        success: {
            bg: 'linear-gradient(135deg, rgba(5, 150, 105, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%)',
            text: '#059669',
            border: '#10B981'
        },
        error: {
            bg: 'linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%)',
            text: '#DC2626',
            border: '#EF4444'
        },
        warning: {
            bg: 'linear-gradient(135deg, rgba(217, 119, 6, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%)',
            text: '#D97706',
            border: '#F59E0B'
        },
        info: {
            bg: 'linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%)',
            text: '#2563EB',
            border: '#3B82F6'
        }
    };
    return colors[type] || colors.info;
}

function getNotificationIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || icons.info;
}

// Loading states initialization
function initializeLoadingStates() {
    // Add CSS for loading states
    if (!document.getElementById('loading-styles')) {
        const style = document.createElement('style');
        style.id = 'loading-styles';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
            
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .button-loading {
                position: relative;
                color: transparent !important;
            }
            
            .button-loading::after {
                content: '';
                position: absolute;
                width: 20px;
                height: 20px;
                top: 50%;
                left: 50%;
                margin-left: -10px;
                margin-top: -10px;
                border: 2px solid transparent;
                border-top-color: #ffffff;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
        `;
        document.head.appendChild(style);
    }
}

// Utility function for button loading states
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.classList.add('button-loading');
        button.dataset.originalText = button.textContent;
        // Keep the text but make it transparent via CSS
    } else {
        button.disabled = false;
        button.classList.remove('button-loading');
        // Text will become visible again via CSS
    }
}

// Authentication page handler
async function handleAuthPage() {
    const authForm = document.getElementById('auth-form');
    const authButton = document.getElementById('auth-button');
    const authSwitch = document.getElementById('switch-to-signup');
    const authMessage = document.getElementById('auth-message');
    const nameGroup = document.getElementById('name-group');
    const extraDetailsGroup = document.getElementById('extra-details-group');

    if (!authForm || !authButton || !authSwitch) {
        console.error('Auth form elements not found');
        return;
    }

    let isLogin = true;
    
    // Initialize form validation
    addFormValidation(authForm);

    // Toggle between login and signup
    authSwitch.addEventListener('click', (e) => {
        e.preventDefault();
        isLogin = !isLogin;
        
        authButton.textContent = isLogin ? 'Sign In' : 'Create Account';
        authSwitch.textContent = isLogin ? 'Create Account' : 'Sign In';
        authSwitch.closest('p').innerHTML = isLogin 
            ? 'Don\'t have an account? <a href="#" id="switch-to-signup">Create Account</a>'
            : 'Already have an account? <a href="#" id="switch-to-signup">Sign In</a>';
        
        nameGroup.style.display = isLogin ? 'none' : 'block';
        extraDetailsGroup.style.display = isLogin ? 'none' : 'block';
        
        // Clear messages and validation
        if (authMessage) {
            authMessage.style.display = 'none';
            authMessage.textContent = '';
        }
        clearAllValidationErrors();
        
        // Re-attach event listener to new switch button
        document.getElementById('switch-to-signup').addEventListener('click', arguments.callee);
    });

    // Handle form submission
    authForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear previous errors
        clearAllValidationErrors();
        if (authMessage) authMessage.style.display = 'none';
        
        // Validate form
        if (!validateForm(isLogin)) {
            showNotification('Please fix the errors in the form before submitting.', 'warning');
            return;
        }
        
        // Set loading state
        setButtonLoading(authButton, true);
        
        // Prepare form data
        const formData = {
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value
        };
        
        if (!isLogin) {
            formData.name = document.getElementById('name').value.trim();
            formData.age = document.getElementById('age').value ? parseInt(document.getElementById('age').value) : null;
            formData.city = document.getElementById('city').value.trim() || null;
            formData.state = document.getElementById('state').value.trim() || null;
            formData.mobile = document.getElementById('mobile').value.trim() || null;
            formData.sex = document.getElementById('sex').value || null;
        }

        try {
            const url = isLogin ? '/auth/login' : '/auth/register';
            const response = await fetch(url, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                const message = result.message || (isLogin ? 'Login successful!' : 'Account created successfully!');
                showNotification(message, 'success');
                
                if (authMessage) {
                    authMessage.textContent = message;
                    authMessage.className = 'auth-message success';
                    authMessage.style.display = 'block';
                }
                
                if (result.access_token) {
                    localStorage.setItem('access_token', result.access_token);
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                }
            } else {
                const errorMessage = getErrorMessage(result.detail || result.message || 'Authentication failed');
                showNotification(errorMessage, 'error');
                
                if (authMessage) {
                    authMessage.textContent = errorMessage;
                    authMessage.className = 'auth-message error';
                    authMessage.style.display = 'block';
                }
            }
        } catch (error) {
            console.error('Auth error:', error);
            const errorMessage = 'Unable to connect to server. Please check your internet connection.';
            showNotification(errorMessage, 'error');
            
            if (authMessage) {
                authMessage.textContent = errorMessage;
                authMessage.className = 'auth-message error';
                authMessage.style.display = 'block';
            }
        } finally {
            setButtonLoading(authButton, false);
        }
    });
}

// Form validation functions
function addFormValidation(form) {
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    clearFieldError(event);
    
    let isValid = true;
    let errorMessage = '';
    
    if (field.required && !value) {
        isValid = false;
        errorMessage = `${getFieldName(field)} is required`;
    } else if (field.type === 'email' && value) {
        if (!isValidEmail(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    } else if (field.type === 'password' && value) {
        const isLoginForm = !document.getElementById('name-group') || document.getElementById('name-group').style.display === 'none';
        if (!isLoginForm && value.length < 8) {
            isValid = false;
            errorMessage = 'Password must be at least 8 characters long';
        } else if (!isLoginForm && !/(?=.*[a-zA-Z])(?=.*\d)/.test(value)) {
            isValid = false;
            errorMessage = 'Password must contain at least one letter and one number';
        }
    } else if (field.type === 'tel' && value) {
        if (!/^[\+]?[1-9][\d\s\-]{7,15}$/.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        }
    }
    
    if (!isValid) {
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

function clearFieldError(event) {
    const field = event.target;
    field.classList.remove('error');
    const existingError = field.parentElement.parentElement.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

function showFieldError(field, message) {
    field.classList.add('error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    
    field.parentElement.parentElement.appendChild(errorDiv);
}

function clearAllValidationErrors() {
    document.querySelectorAll('.field-error').forEach(error => error.remove());
    document.querySelectorAll('.error').forEach(field => field.classList.remove('error'));
}

function validateForm(isLogin) {
    let isValid = true;
    const form = document.getElementById('auth-form');
    
    if (isLogin) {
        // Only validate email and password for login
        const email = document.getElementById('email');
        const password = document.getElementById('password');
        
        if (!validateField({ target: email })) isValid = false;
        if (!validateField({ target: password })) isValid = false;
    } else {
        // Validate all required fields for signup
        const requiredFields = form.querySelectorAll('input[required]');
        requiredFields.forEach(field => {
            if (!validateField({ target: field })) isValid = false;
        });
    }
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function getFieldName(field) {
    return field.placeholder || field.name || 'Field';
}

function getErrorMessage(error) {
    const errorMappings = {
        'already exists': 'An account with this email already exists. Please sign in instead.',
        'not found': 'No account found with this email. Please create an account first.',
        'invalid email': 'Please enter a valid email address.',
        'incorrect password': 'Incorrect password. Please try again.',
        'validation error': 'Please check your input and try again.',
        'server error': 'Server error. Please try again later.',
        'network error': 'Network error. Please check your connection.'
    };
    
    const lowerError = error.toLowerCase();
    for (const [key, message] of Object.entries(errorMappings)) {
        if (lowerError.includes(key)) {
            return message;
        }
    }
    
    return error;
}

// Dashboard page handler
async function handleDashboardPage() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // Validate session
    try {
        const response = await fetch('/auth/check-session', {
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                showNotification('Session expired. Please sign in again.', 'warning');
                localStorage.removeItem('access_token');
                setTimeout(() => window.location.href = '/login', 2000);
                return;
            }
        }
    } catch (error) {
        console.error('Session validation failed:', error);
    }

    // Initialize dashboard components
    initializeFileUpload();
    initializeLogout();
    loadAnalysisHistory();
}

function initializeFileUpload() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const analyzeButton = document.getElementById('analyze-button');
    const uploadMessage = document.getElementById('upload-message');
    
    if (!dropZone || !fileInput || !fileList || !analyzeButton) {
        console.error('File upload elements not found');
        return;
    }

    let uploadedFiles = [];

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        if (!dropZone.contains(e.relatedTarget)) {
            dropZone.classList.remove('dragover');
        }
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files).filter(file => file.type.startsWith('image/'));
        handleFileSelection(files.slice(0, 5));
    });

    dropZone.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        handleFileSelection(files.slice(0, 5));
    });

    function handleFileSelection(files) {
        uploadedFiles = files;
        updateFileList();
    }

    function updateFileList() {
        fileList.innerHTML = '';
        
        uploadedFiles.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span style="display: flex; align-items: center; gap: 0.5rem;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <circle cx="9" cy="9" r="2"/>
                        <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                    </svg>
                    ${file.name}
                    <span style="font-size: 0.8rem; color: var(--text-muted);">(${(file.size / 1024 / 1024).toFixed(1)}MB)</span>
                </span>
                <button class="remove-btn" data-index="${index}">×</button>
            `;
            fileList.appendChild(fileItem);
        });

        analyzeButton.disabled = uploadedFiles.length === 0 || uploadedFiles.length > 5;
        
        if (uploadedFiles.length > 5) {
            showNotification('Maximum 5 files allowed. Please remove some files.', 'warning');
        }
    }

    // Remove file handler
    fileList.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-btn')) {
            const index = parseInt(e.target.dataset.index);
            uploadedFiles.splice(index, 1);
            updateFileList();
        }
    });

    // Analyze button handler
    analyzeButton.addEventListener('click', async () => {
        if (uploadedFiles.length === 0) {
            showNotification('Please select at least one image to analyze.', 'warning');
            return;
        }
        
        setButtonLoading(analyzeButton, true);
        
        try {
            await performAnalysis(uploadedFiles);
        } catch (error) {
            console.error('Analysis failed:', error);
            showNotification('Analysis failed. Please try again.', 'error');
        } finally {
            setButtonLoading(analyzeButton, false);
        }
    });
}

async function performAnalysis(files) {
    const token = localStorage.getItem('access_token');
    const uploadMessage = document.getElementById('upload-message');
    
    // Show upload progress
    if (uploadMessage) {
        uploadMessage.textContent = 'Uploading images...';
        uploadMessage.className = 'auth-message info';
        uploadMessage.style.display = 'block';
    }
    
    showNotification('Uploading images...', 'info');

    // Upload files
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    const uploadResponse = await fetch('/api/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });

    if (!uploadResponse.ok) {
        const error = await uploadResponse.json();
        throw new Error(error.detail || 'Upload failed');
    }
    
    const uploadResult = await uploadResponse.json();
    const analysisId = uploadResult.analysis_id;

    // Start analysis
    if (uploadMessage) {
        uploadMessage.textContent = 'Running AI analysis...';
    }
    
    showNotification('Images uploaded. Running AI analysis...', 'info');
    
    const analyzeResponse = await fetch(`/api/analyze?analysis_id=${analysisId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (!analyzeResponse.ok) {
        const error = await analyzeResponse.json();
        throw new Error(error.detail || 'Analysis failed');
    }
    
    const analyzeResult = await analyzeResponse.json();

    // Show success message
    if (uploadMessage) {
        uploadMessage.textContent = 'Analysis completed successfully!';
        uploadMessage.className = 'auth-message success';
    }
    
    showNotification('Analysis completed successfully!', 'success');
    
    // Display results
    await displayResults(analysisId);
    
    // Refresh history
    loadAnalysisHistory();
}

async function displayResults(analysisId) {
    const token = localStorage.getItem('access_token');
    const resultsSection = document.getElementById('results-section');
    const resultsDisplay = document.getElementById('results-display');
    
    try {
        const response = await fetch(`/api/results/${analysisId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const results = await response.json();
            
            resultsDisplay.innerHTML = `
                <div style="background: var(--gradient-card); border: 2px solid var(--medical-green); border-radius: 1rem; padding: 2rem; text-align: center;">
                    <h3 style="margin-bottom: 1rem; color: var(--text-primary);">
                        Primary Finding: <span style="color: var(--medical-green); font-weight: 800;">${results.results.primary_finding.class}</span>
                    </h3>
                    <p style="margin-bottom: 1rem;">
                        Confidence: <span style="background: var(--medical-green); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 700;">${results.results.primary_finding.confidence}</span>
                    </p>
                    ${results.results.additional_findings && results.results.additional_findings.length > 0 ? `
                        <div style="margin-top: 1.5rem; text-align: left;">
                            <h4 style="margin-bottom: 1rem;">Additional Findings:</h4>
                            <ul style="list-style: none; padding: 0;">
                                ${results.results.additional_findings.map(f => `
                                    <li style="background: var(--gray-50); margin-bottom: 0.5rem; padding: 0.75rem; border-radius: 0.5rem; display: flex; justify-content: space-between;">
                                        <span>${f.class}</span>
                                        <span style="font-weight: 600; color: var(--primary-blue);">${f.confidence}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
            
            resultsSection.style.display = 'block';
            
            // Setup download handlers
            document.getElementById('download-report-button').onclick = () => downloadReport(analysisId);
            document.getElementById('email-report-button').onclick = () => emailReportAgain(analysisId);
        }
    } catch (error) {
        console.error('Failed to load results:', error);
        showNotification('Failed to load results. Please try again.', 'error');
    }
}

function initializeLogout() {
    const logoutButton = document.getElementById('logout-button');
    if (!logoutButton) return;
    
    logoutButton.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to sign out?')) return;
        
        setButtonLoading(logoutButton, true);
        
        try {
            const token = localStorage.getItem('access_token');
            await fetch('/auth/logout', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('access_token');
            showNotification('You have been signed out successfully.', 'success');
            setTimeout(() => window.location.href = '/login', 1500);
        }
    });
}

async function loadAnalysisHistory() {
    const token = localStorage.getItem('access_token');
    const historyBody = document.getElementById('history-body');
    
    if (!historyBody) return;
    
    try {
        const response = await fetch('/api/history', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const history = await response.json();
            historyBody.innerHTML = '';
            
            if (history.length === 0) {
                historyBody.innerHTML = `
                    <tr>
                        <td colspan="4" style="text-align: center; padding: 3rem; color: var(--text-muted);">
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
                                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="opacity: 0.5;">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                    <polyline points="14,2 14,8 20,8"/>
                                    <line x1="16" y1="13" x2="8" y2="13"/>
                                    <line x1="16" y1="17" x2="8" y2="17"/>
                                </svg>
                                <div>
                                    <p style="font-weight: 600; margin-bottom: 0.5rem;">No analysis history yet</p>
                                    <p style="font-size: 0.9rem;">Upload some dental images to get started!</p>
                                </div>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            history.forEach(analysis => {
                const row = document.createElement('tr');
                const date = new Date(analysis.timestamp).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                });
                const status = analysis.status.charAt(0).toUpperCase() + analysis.status.slice(1);
                const finding = analysis.results?.primary_finding?.class || 'Processing...';
                
                let actionsHtml = '';
                if (status === 'Completed') {
                    actionsHtml = `
                        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="#" onclick="downloadReport('${analysis._id}')" class="action-link">
                                Download
                            </a>
                            <a href="#" onclick="viewReport('${analysis._id}')" class="action-link">
                                View
                            </a>
                        </div>
                    `;
                } else {
                    actionsHtml = '<span style="color: var(--text-muted); font-style: italic;">Processing...</span>';
                }

                row.innerHTML = `
                    <td>${date}</td>
                    <td><span class="status-badge status-${analysis.status.toLowerCase()}">${status}</span></td>
                    <td>${finding}</td>
                    <td>${actionsHtml}</td>
                `;
                
                historyBody.appendChild(row);
            });
        } else if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Failed to load history:', error);
        showNotification('Failed to load analysis history.', 'error');
    }
}

// Global functions for report actions
window.downloadReport = async function(analysisId) {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`/api/reports/${analysisId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `dental_analysis_report_${analysisId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showNotification('Report downloaded successfully!', 'success');
        } else {
            showNotification('Failed to download report. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Download error:', error);
        showNotification('Download failed. Please check your connection.', 'error');
    }
};

window.viewReport = async function(analysisId) {
    await displayResults(analysisId);
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
};

window.emailReportAgain = async function(analysisId) {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`/api/analyze?analysis_id=${analysisId}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            showNotification('Report sent to your email successfully!', 'success');
        } else {
            showNotification('Failed to send email. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Email error:', error);
        showNotification('Failed to send email. Please try again.', 'error');
    }
};