const container = document.querySelector('body');

// Function to close a menu/modal
const closeMenu = (selector) => {
    const navigation = document.querySelector(selector);
    if (navigation) {
        navigation.classList.remove('active');
    }
    container.removeEventListener('click', () => closeMenu(selector));
};

// Function to open a menu/modal
const openMenu = (openBtnSelector, menuSelector, closeBtnSelector) => {
    const openButton = document.querySelector(openBtnSelector);
    const navigation = document.querySelector(menuSelector);
    const closeButton = document.querySelector(closeBtnSelector);

    if (openButton && navigation && closeButton) {
        openButton.addEventListener('click', (event) => {
            event.stopPropagation();
            navigation.classList.add('active');
            container.addEventListener('click', () => closeMenu(menuSelector));
        });

        closeButton.addEventListener('click', (event) => {
            event.stopPropagation();
            closeMenu(menuSelector);
        });
    }
};

// Mobile or Desktop specific menu handling
if (window.innerWidth < 768) {
    openMenu('.btn-menu', '.menu', '.btn-close');
} else {
    openMenu('.btn-avatar-option', '.navbar-desktop-menu', '.btn-close');

    const desktopMenu = document.querySelector('.navbar-desktop-menu');
    desktopMenu?.addEventListener('click', (event) => {
        event.stopPropagation();
    });
}

// Notifications handling
const openNotificationsBtn = document.querySelector('.btn-notification');
const notificationsContainer = document.querySelector('.notifications-container');

openNotificationsBtn?.addEventListener('click', (event) => {
    event.stopPropagation();
    notificationsContainer.classList.toggle('active');
    container.addEventListener('click', () => closeMenu('.notifications-container'));
});

notificationsContainer?.addEventListener('click', (event) => {
    event.stopPropagation();
});

// Search Modal handling
const openSearchBtns = document.querySelectorAll('.search-button');
const searchModal = document.querySelector('.search-layer');
const searchForm = document.querySelector('.search-layer form');

openSearchBtns.forEach((btn) => {
    btn.addEventListener('click', (event) => {
        event.stopPropagation();
        searchModal.classList.add('active');
        container.addEventListener('click', () => closeMenu('.search-layer'));
    });
});
searchForm?.addEventListener('click', (event) => {
    event.stopPropagation();
});
