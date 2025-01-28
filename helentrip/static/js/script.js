new Swiper('.card-wrapper', {
    loop: true,
    spaceBetween: 30,

    // Pagination bullets
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
        dynamicBullets: true
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    // Responsive breakpoints
    breakpoints: {
        0: {
            slidesPerView: 1.2
        },
        600: {
            slidesPerView: 1.5
        },
        700: {
            slidesPerView: 1.8
        },
        800: {
            slidesPerView: 2
        },
        900: {
            slidesPerView: 2.4
        },
        1024: {
            slidesPerView: 3
        },
        1400: {
            slidesPerView: 4
        }
    }
});


// TIMER



// ACCORDION

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
	acc[i].addEventListener("click", function() {
		this.classList.toggle("active");
		var panel = this.nextElementSibling;
		if (panel.style.maxHeight){
			panel.style.maxHeight = null;
		} else {
			panel.style.maxHeight = panel.scrollHeight + "px";
		} 
	});
}

// slider for description

/* let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("shedule__myslide");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
} */

//------
let slideIndex = 1;
showSlides(slideIndex);

// Свайп - начальная и конечная позиции
let touchStartX = 0;
let touchEndX = 0;

// Функция перелистывания
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Функция выбора текущего слайда
function currentSlide(n) {
  showSlides(slideIndex = n);
}

// Функция показа слайдов
function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("shedule__myslide");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) { slideIndex = 1 }
  if (n < 1) { slideIndex = slides.length }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

// Функции для обработки свайпа
function handleTouchStart(event) {
  touchStartX = event.touches[0].clientX; // Запоминаем начальную позицию
}

function handleTouchEnd(event) {
  touchEndX = event.changedTouches[0].clientX; // Запоминаем конечную позицию
  handleSwipe();
}

function handleSwipe() {
  if (touchStartX - touchEndX > 50) {
    // Свайп влево
    plusSlides(1);
  } else if (touchEndX - touchStartX > 50) {
    // Свайп вправо
    plusSlides(-1);
  }
}

// Привязка событий к слайдеру
const slider = document.querySelector(".shedule__photo");
slider.addEventListener("touchstart", handleTouchStart, false);
slider.addEventListener("touchend", handleTouchEnd, false);