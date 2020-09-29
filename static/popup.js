const togglePopup = () => {
    const body = document.querySelector('body')
    const popup = document.querySelector('.popup')
    popup.classList.toggle('opacity-0')
    popup.classList.toggle('pointer-events-none')
    body.classList.toggle('popup-active')
  }
  
  
  let openpopup = document.querySelectorAll('.popup-open')
  for (let i = 0; i < openpopup.length; i++) {
    openpopup[i].addEventListener('click', evt => {
        evt.preventDefault()
        togglePopup()
    })
  }
  
  const popupoverlay = document.querySelector('.popup-overlay')
  popupoverlay.addEventListener('click', togglePopup)
  
  let closepopup = document.querySelectorAll('.popup-close')
  for (let i = 0; i < closepopup.length; i++) {
    closepopup[i].addEventListener('click', togglePopup)
  }
  
  document.onkeydown = evt => {
    evt = evt || window.event
    let isEscape = false
    if ("key" in evt) {
        isEscape = (evt.key === "Escape" || evt.key === "Esc")
    } else {
        isEscape = (evt.keyCode === 27)
    }
    if (isEscape && document.body.classList.contains('popup-active')) {
        togglePopup()
    }
  };