'use strict';
var _a, _b;
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
class NavBar {
  constructor() {
    this.dropdownBtn = Array.from(
      document.querySelectorAll('.nav-dropdown-btn'),
    );
    this.navDropdown = Array.from(document.querySelectorAll('.nav-dropdown'));
    this.hamburgerBtn = document.getElementById('hamburger');
    this.navMenu = document.querySelector('.menu');
    this.links = Array.from(document.querySelectorAll('.nav-dropdown a'));
  }
  init() {
    if (!this.dropdownBtn) return;
    this.dropdownBtn.forEach((btn) => {
      btn.addEventListener('click', (e) => this.handleDropdown(btn, e));
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
  handleDropdown(btn, e) {
    var _a;
    if (!e.currentTarget) return;
    const dropdownIndex =
      (_a = e.currentTarget.dataset.dropdown) !== null && _a !== void 0
        ? _a
        : '';
    const dropdownElement = document.getElementById(dropdownIndex);
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
  setAriaExpandedFalse() {
    this.dropdownBtn.forEach((btn) =>
      btn.setAttribute('aria-expanded', 'false'),
    );
  }
  closeDropdownMenu() {
    this.navDropdown.forEach((drop) => {
      drop.classList.remove('active');
      drop.addEventListener('click', (e) => e.stopPropagation());
    });
  }
  toggleHamburger() {
    this.navMenu.classList.toggle('show');
    this.hamburgerBtn.setAttribute(
      'aria-expanded',
      this.hamburgerBtn.getAttribute('aria-expanded') === 'false'
        ? 'true'
        : 'false',
    );
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
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function handleForgotPasswordPages(pageAttr) {
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
(_a = document.getElementById('resend-email-btn')) === null || _a === void 0
  ? void 0
  : _a.addEventListener('click', () => {
      window.location.reload();
    });
(_b = document.getElementById('go-back-link')) === null || _b === void 0
  ? void 0
  : _b.addEventListener('click', () => {
      history.back();
    });

class HandlePasswordTipsStyles {
  constructor() {
    this.passwordField = document.querySelector('#id_password');
    this.helpTexts = Array.from(
      document.querySelectorAll('.helptext-p.password'),
    );
  }
  init() {
    if (!this.passwordField || !this.helpTexts) return;
    this.passwordField.addEventListener('keyup', () => this.handleStyle());
  }
  handleStyle() {
    const conditions = [
      !(this.passwordField.value.length < 8),
      /^(?=.*[A-Z])/.test(this.passwordField.value),
      /^(?=.*[a-z])/.test(this.passwordField.value),
      /^(?=.*\d)/.test(this.passwordField.value),
    ];
    const errorColor = '#dc3545';
    const successColor = '#28a745';

    conditions.forEach((condition, index) => {
      const color = condition ? successColor : errorColor;
      this.changeHelpTextColor(index, color);

      if (!condition) {
        this.addIcon(index, 'fa-circle-exclamation', errorColor);
        this.removeIcon(index, 'fa-check');
      } else {
        this.addIcon(index, 'fa-check', successColor);
        this.removeIcon(index, 'fa-circle-exclamation');
      }
    });
  }
  changeHelpTextColor(index, color) {
    if (!this.helpTexts[index]) return;
    this.helpTexts[index].style.color = color;
  }
  addIcon(index, iconClass, color) {
    if (!this.helpTexts[index]) return;

    let icon = this.helpTexts[index].querySelector(`.${iconClass}`);
    if (!icon) {
      icon = document.createElement('i');
      icon.className = `fa-solid ${iconClass}`;
      icon.style.marginLeft = '8px';
      icon.style.color = color;
      this.helpTexts[index].appendChild(icon);
    }
  }
  removeIcon(index, iconClass) {
    if (!this.helpTexts[index]) return;
    const icon = this.helpTexts[index].querySelector(`.${iconClass}`);
    if (icon) {
      this.helpTexts[index].removeChild(icon);
    }
  }
}

new NavBar().init();
new NotificationsScreen().init();
new LogoutLinks().init();
new ShowHidePassword().init();
new DismissFlashMessages().init();
new SelectInputCheckIcon().init();
new HandlePasswordTipsStyles().init();
