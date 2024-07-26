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
}
