class DarkMode {
  toggleDarkbtn: HTMLAnchorElement;
  body: HTMLBodyElement;

  constructor() {
    this.toggleDarkbtn = document.querySelector(
      '#toggle-dark-mode',
    ) as HTMLAnchorElement;
    this.body = document.querySelector('body') as HTMLBodyElement;
  }

  init(): void {
    // toggle existe
    if (!this.toggleDarkbtn) return;

    this.handlePageLoad();

    this.toggleDarkbtn.addEventListener('click', () => {
      // configurando valor de darkmode no localstorage
      const isDark = localStorage.getItem('darkmode');
      localStorage.setItem('darkmode', isDark === 'true' ? 'false' : 'true');
      this.changePageColors();
      this.changeMenuIcon();
    });
  }

  handlePageLoad(): void {
    // valor padrão para darkmode em local storage, se não existir
    if (localStorage.getItem('darkmode') === null) {
      localStorage.setItem('darkmode', 'false');
    }

    document.addEventListener('DOMContentLoaded', () => {
      this.changePageColors();
      this.changeMenuIcon();
    });
  }

  // trocando o tema do site
  changePageColors(): void {
    const isDark = localStorage.getItem('darkmode');

    if (isDark === 'true') this.toggleDarkMode();
    else this.removeDarkMode();
  }

  // muda o ícone da header dinamicamente com base no valor do localstorage
  changeMenuIcon(): void {
    const menuIcon = document.querySelector('#theme-icon') as HTMLElement;
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

  // adiciona a classe de dark mode e texto branco
  toggleDarkMode(): void {
    this.addClassList(this.body, 'dark-mode-style');
    this.body.style.transition = 'all 150ms ease';
  }

  // remove a classe de dark mode
  removeDarkMode(): void {
    this.removeClassList(this.body, 'dark-mode-style');
  }

  // adiciona uma classe ao elemento
  addClassList(element: HTMLElement, class_to_add: string): void {
    if (element) element.classList.add(class_to_add);
  }

  // remove uma classe do elemento
  removeClassList(element: HTMLElement, remove_class: string): void {
    if (element) element.classList.remove(remove_class);
  }
}

new DarkMode().init();
