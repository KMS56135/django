document.addEventListener("DOMContentLoaded", function () {
  const slider = document.querySelector("#slider");
  const sliderWrapper = document.querySelector("#sliderWrapper");

  if (!slider || !sliderWrapper) return;

  let isDown = false;
  let startX;
  let scrollLeft;

  // Обработчики для мыши
  slider.addEventListener("mousedown", (e) => {
    isDown = true;
    slider.classList.add("active");
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
  });

  slider.addEventListener("mouseleave", () => {
    isDown = false;
    slider.classList.remove("active");
  });

  slider.addEventListener("mouseup", () => {
    isDown = false;
    slider.classList.remove("active");
  });

  slider.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 2;
    slider.scrollLeft = scrollLeft - walk;
  });

  // Обработчики для тач-устройств
  slider.addEventListener("touchstart", (e) => {
    isDown = true;
    slider.classList.add("active");
    startX = e.touches[0].pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
  });

  slider.addEventListener("touchend", () => {
    isDown = false;
    slider.classList.remove("active");
  });

  slider.addEventListener("touchmove", (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.touches[0].pageX - slider.offsetLeft;
    const walk = (x - startX) * 2;
    slider.scrollLeft = scrollLeft - walk;
  });
});
