/* dark mode toggle */

(() => {
  const toggleDarkbtn = document.querySelector('#toggle-dark-mode');
  const mainContent = document.querySelector('body');
  const exerciseCardsBackground = document.querySelectorAll(
    '.exercise-card-background',
  );
  const tableElement = document.querySelector('.content-table');
  const tableTr = document.querySelectorAll('.table-tr');
  const notifications = document.querySelectorAll('.notification');
  const generalIcons = document.querySelectorAll('.general-icon');

  /* chamando essa função para mostrar sempre o ícone e cor corretas, mesmo se atualizar a página */
  handlePageLoad();

  // valor padrão para darkmode em local storage, se não existir
  if (localStorage.getItem('darkmode') === null) {
    localStorage.setItem('darkmode', 'false');
  }

  // botão não existe
  if (!toggleDarkbtn) return;

  // evento do botão, altera o valor sempre que é clicado
  toggleDarkbtn.addEventListener('click', () => {
    const isDark = localStorage.getItem('darkmode');
    localStorage.setItem('darkmode', isDark === 'true' ? 'false' : 'true');
    changePageColors();
    changeMenuIcon();
  });

  function handlePageLoad() {
    document.addEventListener('DOMContentLoaded', () => {
      changePageColors();
      changeMenuIcon();
    });
  }

  // chama as funções para troca de cores
  function changePageColors() {
    const isDark = localStorage.getItem('darkmode');

    if (isDark === 'true') toggleDarkMode();
    else removeDarkMode();
  }

  // adiciona a classe de dark mode e texto branco
  function toggleDarkMode() {
    addClassList(mainContent, 'dark-mode-style');
    addClassList(tableElement, 'dark-mode-table');
    // arrays / nodelists
    nodeListAddClass(tableTr, 'tr-dark');
    nodeListAddClass(exerciseCardsBackground, 'dark-mode-cards');
    nodeListAddClass(notifications, 'dark-mode-style');
    nodeListAddClass(generalIcons, 'dark-mode-style');
  }

  // remove a classe de dark mode
  function removeDarkMode() {
    removeClassList(mainContent, 'dark-mode-style');
    removeClassList(tableElement, 'dark-mode-table');
    // arrays / nodelists
    nodeListRemoveClass(tableTr, 'tr-dark');
    nodeListRemoveClass(exerciseCardsBackground, 'dark-mode-cards');
    nodeListRemoveClass(notifications, 'dark-mode-style');
    nodeListRemoveClass(generalIcons, 'dark-mode-style');
  }

  // muda o ícone da header dinamicamente com base no valor do localstorage
  function changeMenuIcon() {
    const menuIcon = document.querySelector('#menu-icon');
    const isDark = localStorage.getItem('darkmode');

    if (isDark === 'true') {
      menuIcon.classList.remove('fa-moon');
      menuIcon.classList.add('fa-sun');
    } else {
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

  function nodeListAddClass(nodelist, class_to_add) {
    if (nodelist) {
      for (const element of nodelist) addClassList(element, class_to_add);
    }
  }

  function nodeListRemoveClass(nodelist, class_to_remove) {
    if (nodelist) {
      for (const element of nodelist) removeClassList(element, class_to_remove);
    }
  }
})();
