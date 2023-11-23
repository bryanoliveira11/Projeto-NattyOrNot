/* dark mode toggle */

(() => {
    const toggleDarkbtn = document.querySelector('#toggle-dark-mode');
    const mainContent = document.querySelector('body');
    const exerciseCardsBackground = document.querySelectorAll('.exercise-card-background');
    const tableElement = document.querySelector('.content-table');
    const tableTr = document.querySelectorAll('.table-tr');

    // botão não existe
    if (!toggleDarkbtn) return;

    /* chamando essa função para mostrar sempre o ícone e cor corretas, mesmo se atualizar a página */
    changePageColors();
    changeMenuIcon();

    // valor padrão para darkmode em local storage, se não existir
    if (localStorage.getItem('darkmode') === null) {
        localStorage.setItem('darkmode', 'false');
    }

    // evento do botão, altera o valor sempre que é clicado
    toggleDarkbtn.addEventListener('click', () => {
        let isDark = localStorage.getItem('darkmode');
        localStorage.setItem('darkmode', isDark === 'true' ? 'false' : 'true');
        changeMenuIcon();
        changePageColors();
    })

    // chama as funções para troca de cores
    function changePageColors() {
        let isDark = localStorage.getItem('darkmode');

        if (isDark === 'true') toggleDarkMode();
        else removeDarkMode();
    }

    // adiciona a classe de dark mode e texto branco
    function toggleDarkMode() {
        addClassList(mainContent, 'dark-mode-style');
        addClassList(tableElement, 'dark-mode-table');
        if (tableTr) {
            for (const tr of tableTr) addClassList(tr, 'tr-dark');
        }
        if (exerciseCardsBackground) {
            for (const card of exerciseCardsBackground) addClassList(card, 'dark-mode-cards');
        }
    }

    // remove a classe de dark mode
    function removeDarkMode() {
        removeClassList(mainContent, 'dark-mode-style');
        removeClassList(tableElement, 'dark-mode-table');
        if (tableTr) {
            for (const tr of tableTr) removeClassList(tr, 'tr-dark');
        }
        if (exerciseCardsBackground) {
            for (const card of exerciseCardsBackground) removeClassList(card, 'dark-mode-cards');
        }
    }

    // muda o ícone da header dinamicamente com base no valor do localstorage
    function changeMenuIcon() {
        const menuIcon = document.querySelector('#menu-icon');
        let isDark = localStorage.getItem('darkmode');

        if (isDark === 'true') {
            menuIcon.classList.remove('fa-moon');
            menuIcon.classList.add('fa-sun');
        }
        else {
            menuIcon.classList.remove('fa-sun');
            menuIcon.classList.add('fa-moon');
        }
    }

    // adiciona uma classe ao elemento
    function addClassList(element, class_to_add) {
        if (element) element.classList.add(class_to_add);
    }

    // remove uma classe do elemento
    function removeClassList(element, class_to_remove) {
        if (element) element.classList.remove(class_to_remove);
    }

})();