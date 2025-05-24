const isMobile = () => window.innerWidth <= 768;
// Update sidebar behavior for mobile
if (isMobile()) {
    sidebar.classList.add('collapsed');
    mainContent.classList.add('expanded');
    toggleBtn.classList.add('collapsed');
}

// Handle window resize
window.addEventListener('resize', () => {
    if (isMobile()) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        toggleBtn.classList.add('collapsed');
    }
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (isMobile() && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        toggleBtn.classList.add('collapsed');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const mainContent = document.getElementById('mainContent');

    // Toggle sidebar
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
        toggleBtn.classList.toggle('collapsed');
        toggleBtn.querySelector('i').classList.toggle('bi-chevron-right');
        toggleBtn.querySelector('i').classList.toggle('bi-chevron-left');
    });
});
