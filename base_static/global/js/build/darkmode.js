'use strict';
class DarkMode {
  constructor() {
    this.toggleDarkbtn = document.querySelector('#toggle-dark-mode');
    this.body = document.querySelector('body');
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
    this.addClassList(this.body, 'dark-mode-style');
  }
  removeDarkMode() {
    this.removeClassList(this.body, 'dark-mode-style');
  }
  addClassList(element, class_to_add) {
    if (element) element.classList.add(class_to_add);
  }
  removeClassList(element, remove_class) {
    if (element) element.classList.remove(remove_class);
  }
}
new DarkMode().init();
