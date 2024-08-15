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
    const activityPanel = document.querySelector('.activity-panel')

    profileAvatar.addEventListener('click', () => {
        navigation.classList.toggle('active');
        activityPanel.addEventListener('click', closeMenu)
    })

    closeButtonDesktop.addEventListener('click', () => {
        navigation.classList.remove('active');
        activityPanel.addEventListener('click', closeMenu)
    })

    const closeMenu = () => {
        navigation.classList.remove('active');
        activityPanel.removeEventListener('click', () => {
        })
    }
}

