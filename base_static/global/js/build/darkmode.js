'use strict';
class DarkMode {
  constructor() {
    this.toggleDarkbtn = document.querySelector('#toggle-dark-mode');
    this.mainContent = document.querySelector('body');
    this.tableElement = document.querySelector('.content-table');
    this.exerciseCardsBackground = Array.from(
      document.querySelectorAll('.exercise-card-background'),
    );
    this.tableTr = Array.from(document.querySelectorAll('.table-tr'));
    this.notifications = Array.from(document.querySelectorAll('.notification'));
    this.generalIcons = Array.from(document.querySelectorAll('.general-icon'));
  }
  init() {
    if (!this.toggleDarkbtn) return;
    this.handlePageLoad();
    this.toggleDarkbtn.addEventListener('click', () => {
      const isDark = localStorage.getItem('darkmode');
      localStorage.setItem('darkmode', isDark === 'true' ? 'false' : 'true');
      this.changePageColors();
      this.changeMenuIcon();
    });
  }
  handlePageLoad() {
    if (localStorage.getItem('darkmode') === null) {
      localStorage.setItem('darkmode', 'false');
    }
    document.addEventListener('DOMContentLoaded', () => {
      this.changePageColors();
      this.changeMenuIcon();
    });
  }
  changePageColors() {
    const isDark = localStorage.getItem('darkmode');
    if (isDark === 'true') this.toggleDarkMode();
    else this.removeDarkMode();
  }
  changeMenuIcon() {
    const menuIcon = document.querySelector('#theme-icon');
    const isDark = localStorage.getItem('darkmode');
    if (!menuIcon) return;
    if (isDark === 'true') {
      menuIcon.classList.remove('fa-moon');
      menuIcon.classList.add('fa-sun');
    } else {
      menuIcon.classList.remove('fa-sun');
      menuIcon.classList.add('fa-moon');
    }
  }
  toggleDarkMode() {
    this.addClassList(this.mainContent, 'dark-mode-style');
    this.addClassList(this.tableElement, 'dark-mode-table');
    this.nodeListAddClass(this.tableTr, 'tr-dark');
    this.nodeListAddClass(this.exerciseCardsBackground, 'dark-mode-cards');
    this.nodeListAddClass(this.notifications, 'dark-mode-style');
    this.nodeListAddClass(this.generalIcons, 'dark-mode-style');
  }
  removeDarkMode() {
    this.removeClassList(this.mainContent, 'dark-mode-style');
    this.removeClassList(this.tableElement, 'dark-mode-table');
    this.nodeListRemoveClass(this.tableTr, 'tr-dark');
    this.nodeListRemoveClass(this.exerciseCardsBackground, 'dark-mode-cards');
    this.nodeListRemoveClass(this.notifications, 'dark-mode-style');
    this.nodeListRemoveClass(this.generalIcons, 'dark-mode-style');
  }
  addClassList(element, class_to_add) {
    if (element) element.classList.add(class_to_add);
  }
  removeClassList(element, remove_class) {
    if (element) element.classList.remove(remove_class);
  }
  nodeListAddClass(nodelist, class_to_add) {
    if (nodelist) {
      for (const element of nodelist) this.addClassList(element, class_to_add);
    }
  }
  nodeListRemoveClass(nodelist, remove_class) {
    if (nodelist) {
      for (const element of nodelist)
        this.removeClassList(element, remove_class);
    }
  }
}
new DarkMode().init();
