'use strict';
function PreventUserClicksOnBody(e) {
  e.preventDefault();
  e.stopPropagation();
}
function AdjustElementOpacity(element, value) {
  if (element) element.style.opacity = value.toString();
}
function AdjustElementDisplay(element, value) {
  if (element) element.style.display = value;
}
function ChangeDisplayAnimationEnd(element) {
  element.addEventListener(
    'animationend',
    () => {
      element.style.display = 'none';
    },
    { once: true },
  );
}
function CloseScreen(screen_to_close, background) {
  if (screen_to_close && background) {
    AdjustElementDisplay(screen_to_close, 'none');
    AdjustElementOpacity(background, 1);
    background.removeEventListener('click', PreventUserClicksOnBody);
  }
}
function createIcon(className, id) {
  const icon = document.createElement('i');
  icon.className = className;
  if (id) icon.id = id;
  return icon;
}
class NotificationsScreen {
  constructor() {
    this.notificationScreen = document.querySelector('.notifications-page');
    this.showNotificationBtn = document.querySelector(
      '#toggle-notification-menu',
    );
    this.closeNotificationsBtn = document.querySelector(
      '#close-notifications-page',
    );
    this.exerciseGrid = document.querySelector('.exercise-container-grid');
    this.pageContent = document.querySelector('.main-content-container');
  }
  init() {
    if (this.showNotificationBtn)
      this.showNotificationBtn.addEventListener('click', () =>
        this.showNotificationsScreen(),
      );
    if (this.closeNotificationsBtn)
      this.closeNotificationsBtn.addEventListener('click', () =>
        this.closeNotificationsScreen(),
      );
  }
  showNotificationsScreen() {
    AdjustElementDisplay(this.notificationScreen, 'inline');
    if (this.exerciseGrid) {
      this.exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
      AdjustElementOpacity(this.exerciseGrid, 0.4);
      return;
    }
    this.pageContent.addEventListener('click', PreventUserClicksOnBody);
    AdjustElementOpacity(this.pageContent, 0.4);
  }
  closeNotificationsScreen() {
    if (this.exerciseGrid) {
      CloseScreen(this.notificationScreen, this.exerciseGrid);
      return;
    }
    CloseScreen(this.notificationScreen, this.pageContent);
  }
}
class LateralMenu {
  constructor() {
    this.buttonShowMenuVisibleClass = 'button-show-menu-is-visible';
    this.menuHiddenClass = 'menu-hidden';
    this.buttonShowMenu = document.querySelector('.button-show-menu');
    this.buttonCloseMenu = document.querySelector('.button-close-menu');
    this.menuContainer = document.querySelector('.menu-container');
    this.notificationScreen = document.querySelector('.notifications-page');
    this.exerciseGrid = document.querySelector('.exercise-container-grid');
    this.pageContent = document.querySelector('.main-content-container');
    this.notificationMenu = document.querySelector('#toggle-notification-menu');
    this.footer = document.querySelector('.main-footer');
  }
  init() {
    if (this.buttonShowMenu) {
      this.buttonShowMenu.removeEventListener('click', () => this.showMenu());
      this.buttonShowMenu.addEventListener('click', () => this.showMenu());
    }
    if (this.buttonCloseMenu) {
      this.buttonCloseMenu.removeEventListener('click', () => this.closeMenu());
      this.buttonCloseMenu.addEventListener('click', () => this.closeMenu());
    }
    this.pageContent.addEventListener('click', () => this.closeMenu());
    if (this.footer)
      this.footer.addEventListener('click', () => this.closeMenu());
    if (this.notificationMenu)
      this.notificationMenu.addEventListener('click', () => this.closeMenu());
  }
  showMenu() {
    this.buttonShowMenu.classList.remove(this.buttonShowMenuVisibleClass);
    this.menuContainer.classList.remove(this.menuHiddenClass);
    if (this.exerciseGrid) {
      CloseScreen(this.notificationScreen, this.exerciseGrid);
      return;
    }
    CloseScreen(this.notificationScreen, this.pageContent);
  }
  closeMenu() {
    this.buttonShowMenu.classList.add(this.buttonShowMenuVisibleClass);
    this.menuContainer.classList.add(this.menuHiddenClass);
  }
}
class LogoutLinks {
  constructor() {
    this.linksLogout = Array.from(
      document.querySelectorAll('.user-logout-link'),
    );
    this.formLogout = document.querySelector('.form-logout');
  }
  init() {
    for (const link of this.linksLogout) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        this.formLogout.submit();
      });
    }
  }
}
class ShowHidePassword {
  constructor() {
    this.passwordField = document.querySelector('#id_password');
  }
  init() {
    if (!this.passwordField) return;
    this.createEyeIcon();
    this.updateInputType();
  }
  updateInputType() {
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
  createEyeIcon() {
    const icon = createIcon(
      'show-password-icon fa-regular fa-eye',
      'show-password-icon',
    );
    const passwordFieldParent = this.passwordField.parentNode;
    if (this.passwordField.classList.contains('login-password-field')) {
      passwordFieldParent.insertBefore(icon, this.passwordField.nextSibling);
    }
  }
}
class DismissFlashMessages {
  constructor() {
    this.dismissMessageBtns = Array.from(
      document.querySelectorAll('.dismiss-flash-message'),
    );
  }
  init() {
    if (!this.dismissMessageBtns) return;
    for (const btn of this.dismissMessageBtns) {
      btn.addEventListener('click', () => {
        const parentElement = btn.parentElement;
        if (parentElement.classList.contains('message')) {
          parentElement.classList.add('hide-message');
          ChangeDisplayAnimationEnd(parentElement);
        }
      });
    }
  }
}
class SelectInputCheckIcon {
  constructor() {
    this.selectField = document.querySelector('.form-group.multiple-select');
  }
  init() {
    if (!this.selectField) return;
    this.addCheckIcon();
  }
  addCheckIcon() {
    const selectLabel = this.selectField.querySelector('label');
    const labelText = selectLabel.innerText;
    this.selectField.addEventListener('change', () => {
      const icon = '<i class="fa-solid fa-circle-check"></i>';
      let selectCount = 0;
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
