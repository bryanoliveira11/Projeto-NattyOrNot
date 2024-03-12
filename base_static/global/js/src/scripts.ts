// funções para as telas de filtros e notificações do usuário

// evita que o usuário clique em algum elemento da tela
function PreventUserClicksOnBody(e: Event): void {
  e.preventDefault();
  e.stopPropagation();
}

// ajusta opacidade de um elemento
function AdjustElementOpacity(element: HTMLElement, value: number): void {
  if (element) element.style.opacity = value.toString();
}

// define o style de display do elemento
function AdjustElementDisplay(element: HTMLElement, value: string): void {
  if (element) element.style.display = value;
}

// settar display para none ao final de uma animação
function ChangeDisplayAnimationEnd(element: HTMLElement): void {
  element.addEventListener(
    'animationend',
    () => {
      element.style.display = 'none';
    },
    { once: true },
  );
}

// fechar telas que 'flutuam' na página
function CloseScreen(
  screen_to_close: HTMLElement,
  background: HTMLElement,
): void {
  if (screen_to_close && background) {
    AdjustElementDisplay(screen_to_close, 'none');
    AdjustElementOpacity(background, 1);
    background.removeEventListener('click', PreventUserClicksOnBody);
  }
}

function createIcon(className: string, id?: string): HTMLElement {
  const icon = document.createElement('i');
  icon.className = className;
  if (id) icon.id = id;
  return icon;
}

class NotificationsScreen {
  // notifications vars
  notificationScreen: HTMLDivElement;
  showNotificationBtn: HTMLAnchorElement;
  closeNotificationsBtn: HTMLDivElement;

  // pages
  exerciseGrid: HTMLDivElement;
  pageContent: HTMLElement;

  constructor() {
    this.notificationScreen = document.querySelector(
      '.notifications-page',
    ) as HTMLDivElement;
    this.showNotificationBtn = document.querySelector(
      '#toggle-notification-menu',
    ) as HTMLAnchorElement;
    this.closeNotificationsBtn = document.querySelector(
      '#close-notifications-page',
    ) as HTMLDivElement;
    this.exerciseGrid = document.querySelector(
      '.exercise-container-grid',
    ) as HTMLDivElement;
    this.pageContent = document.querySelector(
      '.main-content-container',
    ) as HTMLElement;
  }

  init(): void {
    if (this.showNotificationBtn)
      this.showNotificationBtn.addEventListener('click', () =>
        this.showNotificationsScreen(),
      );

    if (this.closeNotificationsBtn)
      this.closeNotificationsBtn.addEventListener('click', () =>
        this.closeNotificationsScreen(),
      );
  }

  showNotificationsScreen(): void {
    /* menu de notificações */
    AdjustElementDisplay(this.notificationScreen, 'inline');

    // se exerciseGrid existir na tela
    if (this.exerciseGrid) {
      this.exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
      AdjustElementOpacity(this.exerciseGrid, 0.4);
      return;
    }

    // caso contrário usar pagecontent
    this.pageContent.addEventListener('click', PreventUserClicksOnBody);
    AdjustElementOpacity(this.pageContent, 0.4);
  }

  closeNotificationsScreen(): void {
    if (this.exerciseGrid) {
      CloseScreen(this.notificationScreen, this.exerciseGrid);
      return;
    }
    CloseScreen(this.notificationScreen, this.pageContent);
  }
}

class LateralMenu {
  // menu
  buttonShowMenu: HTMLButtonElement;
  buttonCloseMenu: HTMLButtonElement;
  menuContainer: HTMLDivElement;
  buttonShowMenuVisibleClass: string = 'button-show-menu-is-visible';
  menuHiddenClass: string = 'menu-hidden';

  // notification screen
  notificationScreen: HTMLDivElement;
  exerciseGrid: HTMLDivElement;
  pageContent: HTMLElement;
  notificationMenu: HTMLAnchorElement;

  // footer
  footer: HTMLElement;

  constructor() {
    this.buttonShowMenu = document.querySelector(
      '.button-show-menu',
    ) as HTMLButtonElement;
    this.buttonCloseMenu = document.querySelector(
      '.button-close-menu',
    ) as HTMLButtonElement;
    this.menuContainer = document.querySelector(
      '.menu-container',
    ) as HTMLDivElement;
    this.notificationScreen = document.querySelector(
      '.notifications-page',
    ) as HTMLDivElement;
    this.exerciseGrid = document.querySelector(
      '.exercise-container-grid',
    ) as HTMLDivElement;
    this.pageContent = document.querySelector(
      '.main-content-container',
    ) as HTMLElement;
    this.notificationMenu = document.querySelector(
      '#toggle-notification-menu',
    ) as HTMLAnchorElement;
    this.footer = document.querySelector('.main-footer') as HTMLElement;
  }

  init(): void {
    if (this.buttonShowMenu) {
      this.buttonShowMenu.removeEventListener('click', () => this.showMenu());
      this.buttonShowMenu.addEventListener('click', () => this.showMenu());
    }

    if (this.buttonCloseMenu) {
      this.buttonCloseMenu.removeEventListener('click', () => this.closeMenu());
      this.buttonCloseMenu.addEventListener('click', () => this.closeMenu());
    }

    // fechar menu ao clicar na tela
    this.pageContent.addEventListener('click', () => this.closeMenu());

    // fechar menu ao clicar no footer
    if (this.footer)
      this.footer.addEventListener('click', () => this.closeMenu());

    // fechar menu ao abrir notifications
    if (this.notificationMenu)
      this.notificationMenu.addEventListener('click', () => this.closeMenu());
  }

  showMenu(): void {
    this.buttonShowMenu.classList.remove(this.buttonShowMenuVisibleClass);
    this.menuContainer.classList.remove(this.menuHiddenClass);

    if (this.exerciseGrid) {
      CloseScreen(this.notificationScreen, this.exerciseGrid);
      return;
    }
    CloseScreen(this.notificationScreen, this.pageContent);
  }

  closeMenu(): void {
    this.buttonShowMenu.classList.add(this.buttonShowMenuVisibleClass);
    this.menuContainer.classList.add(this.menuHiddenClass);
  }
}

// classe para enviar formulários de logout
class LogoutLinks {
  linksLogout: HTMLAnchorElement[];
  formLogout: HTMLFormElement;

  constructor() {
    this.linksLogout = Array.from(
      document.querySelectorAll('.user-logout-link'),
    ) as HTMLAnchorElement[];
    this.formLogout = document.querySelector('.form-logout') as HTMLFormElement;
  }

  init(): void {
    for (const link of this.linksLogout) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        this.formLogout.submit();
      });
    }
  }
}

// classe para mostrar / esconder a senha no form de login
class ShowHidePassword {
  passwordField: HTMLInputElement;

  constructor() {
    this.passwordField = document.querySelector(
      '#id_password',
    ) as HTMLInputElement;
  }

  init(): void {
    if (!this.passwordField) return;
    this.createEyeIcon();
    this.updateInputType();
  }

  updateInputType(): void {
    const showPasswordIcon = document.querySelector('.show-password-icon');
    if (!showPasswordIcon) return;
    let is_password_visible = false;

    showPasswordIcon.addEventListener('click', () => {
      if (is_password_visible) {
        this.passwordField.type = 'password';
        showPasswordIcon.classList.remove('fa-eye-slash');
        showPasswordIcon.classList.add('fa-eye');
      } else {
        this.passwordField.type = 'text';
        showPasswordIcon.classList.remove('fa-eye');
        showPasswordIcon.classList.add('fa-eye-slash');
      }
      is_password_visible = !is_password_visible;
    });
  }

  createEyeIcon(): void {
    // criando icone fa-eye no html
    const icon = createIcon(
      'show-password-icon fa-regular fa-eye',
      'show-password-icon',
    );
    const passwordFieldParent = this.passwordField.parentNode as HTMLElement;

    // inserindo icone na tela se tiver a classe certa (evitar com que apareça em outros forms)
    if (this.passwordField.classList.contains('login-password-field')) {
      passwordFieldParent.insertBefore(icon, this.passwordField.nextSibling);
    }
  }
}

// classe para remover flash messages da tela
class DismissFlashMessages {
  dismissMessageBtns: HTMLElement[];

  constructor() {
    this.dismissMessageBtns = Array.from(
      document.querySelectorAll('.dismiss-flash-message'),
    ) as HTMLElement[];
  }

  init(): void {
    if (!this.dismissMessageBtns) return;
    for (const btn of this.dismissMessageBtns) {
      btn.addEventListener('click', () => {
        const parentElement = btn.parentElement as HTMLElement;

        if (parentElement.classList.contains('message')) {
          parentElement.classList.add('hide-message');
          ChangeDisplayAnimationEnd(parentElement);
        }
      });
    }
  }
}

class SelectInputCheckIcon {
  selectField: HTMLSelectElement;

  constructor() {
    this.selectField = document.querySelector(
      '.form-group.multiple-select',
    ) as HTMLSelectElement;
  }

  init(): void {
    if (!this.selectField) return;
    this.addCheckIcon();
  }

  addCheckIcon(): void {
    const selectLabel = this.selectField.querySelector(
      'label',
    ) as HTMLLabelElement;
    const labelText: string = selectLabel.innerText;

    // adicionar ícones quando o selected mudar - change
    this.selectField.addEventListener('change', () => {
      const icon: string = '<i class="fa-solid fa-circle-check"></i>';
      let selectCount: number = 0;

      this.selectField.querySelectorAll('option').forEach((option) => {
        if (!option.selected) {
          option.innerHTML = option.text;
          return;
        }
        option.innerHTML = `${icon} ${option.text}`;
        selectCount++;
      });
      selectLabel.innerHTML = `${labelText} &#8594; ${selectCount} ${icon}`;
    });
  }
}

new LateralMenu().init();
new NotificationsScreen().init();
new LogoutLinks().init();
new ShowHidePassword().init();
new DismissFlashMessages().init();
new SelectInputCheckIcon().init();
