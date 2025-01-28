// main menu

const icon = document.querySelector('.icon-menu')
const menu = document.querySelector('.main-menu')
const cross = document.querySelector('.cross')

icon.addEventListener('click', openMenu)
cross.addEventListener('click', closeMenu)

function openMenu(event) {
  menu.style.display = "block";
}

function closeMenu(event) {
  menu.style.display = "none";
}

// CONTACTS

const contactsIcon = document.querySelector('.contacts-icon')
const contacts = document.querySelector('.contacts')
const cross2 = document.querySelector('.cross2')

contactsIcon.addEventListener('click', openContacts)
cross2.addEventListener('click', closeContacts)

function openContacts(event) {
  contacts.style.display = "block";
}

function closeContacts(event) {
  contacts.style.display = "none";
}

// BOOKING

const booking = document.querySelectorAll('.booking')
const bookingForm = document.querySelector('.booking-form')
const cross1 = document.querySelector('.cross1')

for (let book of booking) {book.addEventListener('click', openBookingForm)}
cross1.addEventListener('click', closeBookingForm)

function openBookingForm(event) {
  bookingForm.style.display = "block";
}

function closeBookingForm(event) {
  bookingForm.style.display = "none";
}



