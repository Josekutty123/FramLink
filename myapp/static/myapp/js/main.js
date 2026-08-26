// FarmLink ERP Custom Script

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle for Mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.erp-sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Bulletproof Navbar Login Dropdown Handler
    const loginBtn = document.getElementById('loginDropdown');
    const loginMenu = document.getElementById('loginDropdownMenu');

    if (loginBtn && loginMenu) {
        // Toggle on click
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const isOpen = loginMenu.classList.contains('show');
            
            if (isOpen) {
                loginMenu.classList.remove('show');
                loginBtn.setAttribute('aria-expanded', 'false');
            } else {
                loginMenu.classList.add('show');
                loginBtn.setAttribute('aria-expanded', 'true');
            }
        });

        // Close dropdown when clicking anywhere outside
        document.addEventListener('click', function(e) {
            if (!loginBtn.contains(e.target) && !loginMenu.contains(e.target)) {
                loginMenu.classList.remove('show');
                loginBtn.setAttribute('aria-expanded', 'false');
            }
        });

        // Close dropdown on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && loginMenu.classList.contains('show')) {
                loginMenu.classList.remove('show');
                loginBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Auto-dismiss Django flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            try {
                if (window.bootstrap && bootstrap.Alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } else {
                    alert.remove();
                }
            } catch (err) {
                alert.remove();
            }
        }, 5000);
    });
});
