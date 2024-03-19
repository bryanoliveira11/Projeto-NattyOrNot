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

// classe para a navbar
class NavBar {
  dropdownBtn: HTMLButtonElement[];
  navDropdown: HTMLDivElement[];
  hamburgerBtn: HTMLElement;
  navMenu: HTMLElement;
  links: HTMLAnchorElement[];

  constructor() {
    this.dropdownBtn = Array.from(
      document.querySelectorAll('.nav-dropdown-btn'),
    ) as HTMLButtonElement[];
    this.navDropdown = Array.from(
      document.querySelectorAll('.nav-dropdown'),
    ) as HTMLDivElement[];
    this.hamburgerBtn = document.getElementById('hamburger') as HTMLElement;
    this.navMenu = document.querySelector('.menu') as HTMLElement;
    this.links = Array.from(
      document.querySelectorAll('.nav-dropdown a'),
    ) as HTMLAnchorElement[];
  }

  init(): void {
    if (!this.dropdownBtn) return;

    this.dropdownBtn.forEach((btn) => {
      btn.addEventListener('click', (e: Event) => this.handleDropdown(btn, e));
    });

    this.links.forEach((link) =>
      link.addEventListener('click', () => {
        this.closeDropdownMenu();
        this.setAriaExpandedFalse();
        this.toggleHamburger();
      }),
    );

    document.documentElement.addEventListener('click', () => {
      this.closeDropdownMenu();
      this.setAriaExpandedFalse();
    });

    this.hamburgerBtn.addEventListener('click', () => this.toggleHamburger());
  }

  /*
   função para ativar a classe de active para o btn de dropdown clicado
   e desativar os outros
   */
  handleDropdown(btn: HTMLButtonElement, e: Event): void {
    if (!e.currentTarget) return;

    const dropdownIndex: string =
      (e.currentTarget as HTMLElement).dataset.dropdown ?? '';
    const dropdownElement = document.getElementById(
      dropdownIndex,
    ) as HTMLElement;

    dropdownElement.classList.toggle('active');

    this.navDropdown.forEach((drop) => {
      if (drop.id !== btn.dataset['dropdown']) {
        drop.classList.remove('active');
      }
    });

    e.stopPropagation();

    btn.setAttribute(
      'aria-expanded',
      btn.getAttribute('aria-expanded') === 'false' ? 'true' : 'false',
    );
  }

  setAriaExpandedFalse(): void {
    this.dropdownBtn.forEach((btn) =>
      btn.setAttribute('aria-expanded', 'false'),
    );
  }

  closeDropdownMenu(): void {
    this.navDropdown.forEach((drop) => {
      drop.classList.remove('active');
      drop.addEventListener('click', (e) => e.stopPropagation());
    });
  }

  toggleHamburger(): void {
    this.navMenu.classList.toggle('show');
    this.hamburgerBtn.setAttribute(
      'aria-expanded',
      this.hamburgerBtn.getAttribute('aria-expanded') === 'false'
        ? 'true'
        : 'false',
    );
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

// função para lidar com o css dos passos no form de forgot password
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function handleForgotPasswordPages(pageAttr: string): void {
  const verifyEmail = document.querySelector('#verify-email');
  const verifyCode = document.querySelector('#verify-code');
  const resetPassword = document.querySelector('#reset-password');

  if (!verifyEmail || !verifyCode || !resetPassword || !pageAttr) return;

  if (pageAttr === 'code-page') {
    verifyCode.classList.add('active');
    return;
  }
  if (pageAttr === 'reset-page') {
    verifyCode.classList.add('active');
    resetPassword.classList.add('active');
    return;
  }
}

// função para reenviar e-mail (somente recarrega a página)
document.querySelector('#resend-email-btn')?.addEventListener('click', () => {
  window.location.reload();
});

new NavBar().init();
new NotificationsScreen().init();
new LogoutLinks().init();
new ShowHidePassword().init();
new DismissFlashMessages().init();
new SelectInputCheckIcon().init();
