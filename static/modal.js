const toggleModal = () => {
  const body = document.querySelector('body')
  const modal = document.querySelector('.modal')
  modal.classList.toggle('opacity-0')
  modal.classList.toggle('pointer-events-none')
  body.classList.toggle('modal-active')
}


let openmodal = document.querySelectorAll('.modal-open')
for (let i = 0; i < openmodal.length; i++) {
  openmodal[i].addEventListener('click', evt => {
      evt.preventDefault()
      toggleModal()
  })
}

const overlay = document.querySelector('.modal-overlay')
overlay.addEventListener('click', toggleModal)

let closemodal = document.querySelectorAll('.modal-close')
for (let i = 0; i < closemodal.length; i++) {
  closemodal[i].addEventListener('click', toggleModal)
}

document.onkeydown = evt => {
  evt = evt || window.event
  let isEscape = false
  if ("key" in evt) {
      isEscape = (evt.key === "Escape" || evt.key === "Esc")
  } else {
      isEscape = (evt.keyCode === 27)
  }
  if (isEscape && document.body.classList.contains('modal-active')) {
      toggleModal()
  }
};