const container = document.querySelector('body');

const closeMenu = () => {
    const navigation = window.innerWidth < 768
        ? document.querySelector('.menu')
        : document.querySelector('.navbar-desktop-menu');
    navigation.classList.remove('active');
    container.removeEventListener('click', closeMenu);
};

if (window.innerWidth < 768) {
    const openButton = document.querySelector('.btn-menu');
    const navigation = document.querySelector('.menu');
    const closeButton = document.querySelector('.btn-close');

    openButton.addEventListener('click', (event) => {
        event.stopPropagation();
        navigation.classList.add('active');
        container.addEventListener('click', closeMenu);
    });

    closeButton.addEventListener('click', (event) => {
        event.stopPropagation();
        navigation.classList.remove('active');
        container.removeEventListener('click', closeMenu);
    });
} else {
    const profileAvatar = document.querySelector('.btn-avatar-option');
    const closeButtonDesktop = document.querySelector('.btn-close');
    const navigation = document.querySelector('.navbar-desktop-menu');

    profileAvatar.addEventListener('click', (event) => {
        event.stopPropagation();
        navigation.classList.toggle('active');
        container.addEventListener('click', closeMenu);
    });

    closeButtonDesktop.addEventListener('click', (event) => {
        event.stopPropagation();
        navigation.classList.remove('active');
        container.removeEventListener('click', closeMenu);
    });
}

const openNotificationsBtn = document.querySelector('.btn-notification');
const notificationsContainer = document.querySelector('.notifications-container');

openNotificationsBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    notificationsContainer.classList.toggle('active');
    container.addEventListener('click', () => {
        notificationsContainer.classList.remove('active');
        container.removeEventListener('click', closeMenu);
    });
});

notificationsContainer.addEventListener('click', (event) => {
    event.stopPropagation();
});

if (window.innerWidth >= 768) {
    const desktopMenu = document.querySelector('.navbar-desktop-menu');
    desktopMenu.addEventListener('click', (event) => {
        event.stopPropagation();
    });
}
