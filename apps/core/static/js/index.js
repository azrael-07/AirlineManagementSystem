document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.slider-dot');
    const prevBtn = document.querySelector('.slider-arrow.prev');
    const nextBtn = document.querySelector('.slider-arrow.next');
    let currentSlide = 0;
    let slideInterval;

    // 初始化轮播图
    function initSlider() {
        slides[0].classList.add('active');
        dots[0].classList.add('active');
        startSlideInterval();
    }

    // 切换到指定幻灯片
    function goToSlide(index) {
        slides[currentSlide].classList.remove('active');
        dots[currentSlide].classList.remove('active');
        currentSlide = (index + slides.length) % slides.length;
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }

    // 下一张幻灯片
    function nextSlide() {
        goToSlide(currentSlide + 1);
    }

    // 上一张幻灯片
    function prevSlide() {
        goToSlide(currentSlide - 1);
    }

    // 开始自动轮播
    function startSlideInterval() {
        slideInterval = setInterval(nextSlide, 5000);
    }

    // 停止自动轮播
    function stopSlideInterval() {
        clearInterval(slideInterval);
    }

    // 事件监听器
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopSlideInterval();
            goToSlide(index);
            startSlideInterval();
        });
    });

    prevBtn.addEventListener('click', () => {
        stopSlideInterval();
        prevSlide();
        startSlideInterval();
    });

    nextBtn.addEventListener('click', () => {
        stopSlideInterval();
        nextSlide();
        startSlideInterval();
    });

    // 鼠标悬停时暂停轮播
    const slider = document.querySelector('.slider');
    slider.addEventListener('mouseenter', stopSlideInterval);
    slider.addEventListener('mouseleave', startSlideInterval);

    // 初始化轮播图
    initSlider();
}); 