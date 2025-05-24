const isMobile = () => window.innerWidth <= 768;

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const mainContent = document.getElementById('mainContent');

    // Initialize sidebar state for mobile
    if (isMobile()) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        toggleBtn.classList.add('collapsed');
        toggleBtn.querySelector('i').classList.add('bi-chevron-right');
        toggleBtn.querySelector('i').classList.remove('bi-chevron-left');
    } else {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');
        toggleBtn.classList.remove('collapsed');
        toggleBtn.querySelector('i').classList.add('bi-chevron-left');
        toggleBtn.querySelector('i').classList.remove('bi-chevron-right');
    }

    // Toggle sidebar
    toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation(); // Prevent click from triggering document click event
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
        toggleBtn.classList.toggle('collapsed');
        toggleBtn.querySelector('i').classList.toggle('bi-chevron-right');
        toggleBtn.querySelector('i').classList.toggle('bi-chevron-left');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (isMobile() && !sidebar.contains(e.target) && !toggleBtn.contains(e.target) && !sidebar.classList.contains('collapsed')) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
            toggleBtn.classList.add('collapsed');
            toggleBtn.querySelector('i').classList.add('bi-chevron-right');
            toggleBtn.querySelector('i').classList.remove('bi-chevron-left');
        }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        if (isMobile()) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
            toggleBtn.classList.add('collapsed');
            toggleBtn.querySelector('i').classList.add('bi-chevron-right');
            toggleBtn.querySelector('i').classList.remove('bi-chevron-left');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
            toggleBtn.classList.remove('collapsed');
            toggleBtn.querySelector('i').classList.add('bi-chevron-left');
            toggleBtn.querySelector('i').classList.remove('bi-chevron-right');
        }
    });
});
