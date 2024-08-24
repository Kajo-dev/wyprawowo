document.addEventListener('DOMContentLoaded', function () {
    const carousels = document.querySelectorAll('.carousel');

    carousels.forEach(function (carousel) {
        const carouselId = carousel.id.split('-')[1];
        const carouselImages = carousel.querySelector('.carousel-images');
        const carouselItems = carousel.querySelectorAll('.carousel-item');
        const nextButton = carousel.querySelector('.next');
        const prevButton = carousel.querySelector('.prev');
        let currentIndex = 0;
        let startX, endX;

        function updateBackgroundColor(imageElement) {
            if (imageElement.complete) {
            } else {
                imageElement.addEventListener('load', function () {
                });
            }
        }

        function updateCarousel() {
            const translateXValue = -currentIndex * 100;
            carouselImages.style.transform = `translateX(${translateXValue}%)`;
            const activeImage = carouselItems[currentIndex].querySelector('img');
            updateBackgroundColor(activeImage);
        }

        nextButton.addEventListener('click', function () {
            if (currentIndex < carouselItems.length - 1) {
                currentIndex++;
            } else {
                currentIndex = 0;
            }
            updateCarousel();
        });

        prevButton.addEventListener('click', function () {
            if (currentIndex > 0) {
                currentIndex--;
            } else {
                currentIndex = carouselItems.length - 1;
            }
            updateCarousel();
        });

        carousel.addEventListener('touchstart', function (e) {
            startX = e.touches[0].clientX;
        });

        carousel.addEventListener('touchmove', function (e) {
            endX = e.touches[0].clientX;
        });

        carousel.addEventListener('touchend', function () {
            if (startX > endX + 50) {
                if (currentIndex < carouselItems.length - 1) {
                    currentIndex++;
                } else {
                    currentIndex = 0;
                }
            } else if (startX < endX - 50) {
                if (currentIndex > 0) {
                    currentIndex--;
                } else {
                    currentIndex = carouselItems.length - 1;
                }
            }
            updateCarousel();
        });

        updateCarousel();
    });
});
