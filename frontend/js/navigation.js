const container = document.querySelector('.my-grid-container')


if (window.innerWidth < 768) {

    const openButton = document.querySelector('.btn-menu');
    const navigation = document.querySelector('.menu');
    const closeButton = document.querySelector('.btn-close');


    openButton.addEventListener('click', () => {
        navigation.classList.add('active');
    })

    closeButton.addEventListener('click', () => {
        navigation.classList.remove('active');
    })
} else {
    const profileAvatar = document.querySelector('.btn-avatar-option')
    const closeButtonDesktop = document.querySelector('.btn-close');
    const navigation = document.querySelector('.navbar-desktop-menu');

    profileAvatar.addEventListener('click', () => {
        navigation.classList.toggle('active');
        container.addEventListener('click', closeMenu)
    })

    closeButtonDesktop.addEventListener('click', () => {
        navigation.classList.remove('active');
        container.addEventListener('click', closeMenu)
    })

    const closeMenu = () => {
        navigation.classList.remove('active');
        container.removeEventListener('click', () => {
        })
    }
}

const openNotificationsBtn = document.querySelector('.btn-notification');
const notificationsContainer = document.querySelector('.notifications-container');
openNotificationsBtn.addEventListener('click', () => {
    notificationsContainer.classList.toggle('active');
    container.addEventListener('click', () => {
        notificationsContainer.classList.remove('active');
        container.removeEventListener('click', () => {
        })
    })

})