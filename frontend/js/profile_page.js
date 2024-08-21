const showCharacteristicsModalTriggers = document.querySelectorAll('.characteristics-container > .characteristics-box');
const closeCharacterModal = document.querySelector('.characteristics-box-modal .btn-close');
const characteristicsModal = document.querySelector('.characteristics-box-modal');
const container = document.querySelector('.my-grid-container');
const seeMoreCharacteristicsBtn = document.querySelector('.see-more-characteristics');

const closeModal = () => {
    characteristicsModal.classList.remove('active');
    container.removeEventListener('click', closeModal);
}


const triggersShowCharacteristicsModal = [...showCharacteristicsModalTriggers, seeMoreCharacteristicsBtn]

if (triggersShowCharacteristicsModal.length > 0 && triggersShowCharacteristicsModal[0] !== null) {
    [...showCharacteristicsModalTriggers, seeMoreCharacteristicsBtn]?.forEach((trigger) => {

        trigger.addEventListener('click', (event) => {
            event.stopPropagation();
            characteristicsModal.classList.toggle('active');
            setTimeout(() => {
                container.addEventListener('click', closeModal)
            }, 0)
        });

    });

    closeCharacterModal.addEventListener('click', (event) => {
        event.stopPropagation();
        characteristicsModal.classList.remove('active');
        container.removeEventListener('click', closeModal);
    });

    characteristicsModal.addEventListener('click', (event) => {
        event.stopPropagation();
    });
}
