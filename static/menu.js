const bars = document.querySelector('#bars')
        const menu = document.querySelector('#menu')
        bars.addEventListener('click',(e)=>{
            menu.classList.toggle('hidden')
        })