"use strict";
function PreventUserClicksOnBody(e) {
    e.preventDefault();
    e.stopPropagation();
}
function AdjustElementOpacity(element, value) {
    if (element)
        element.style.opacity = value;
}
function AdjustElementDisplay(element, value) {
    if (element)
        element.style.display = value;
}
function ChangeDisplayAnimationEnd(element) {
    element.addEventListener('animationend', () => {
        element.style.display = 'none';
    }, { once: true });
}
function CloseScreen(screen_to_close, background) {
    if (screen_to_close && background) {
        AdjustElementDisplay(screen_to_close, 'none');
        AdjustElementOpacity(background, 1);
        background.removeEventListener('click', PreventUserClicksOnBody);
    }
}
(() => {
    const notificationScreen = document.querySelector('.notifications-page');
    const notificationBtn = document.querySelector('#toggle-notification-menu');
    const closeNotificationsBtn = document.querySelector('#close-notifications-page');
    const exerciseGrid = document.querySelector('.exercise-container-grid');
    const pageContent = document.querySelector('.main-content-container');
    if (notificationBtn)
        notificationBtn.addEventListener('click', () => {
            AdjustElementDisplay(notificationScreen, 'inline');
            if (exerciseGrid) {
                exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
                AdjustElementOpacity(exerciseGrid, 0.4);
                return;
            }
            pageContent.addEventListener('click', PreventUserClicksOnBody);
            AdjustElementOpacity(pageContent, 0.4);
        });
    if (closeNotificationsBtn)
        closeNotificationsBtn.addEventListener('click', () => {
            if (exerciseGrid) {
                CloseScreen(notificationScreen, exerciseGrid);
                return;
            }
            CloseScreen(notificationScreen, pageContent);
        });
})();
(() => {
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const buttonCloseMenu = document.querySelector('.button-close-menu');
    const menuContainer = document.querySelector('.menu-container');
    const buttonShowMenuVisibleClass = 'button-show-menu-is-visible';
    const menuHiddenClass = 'menu-hidden';
    const notificationScreen = document.querySelector('.notifications-page');
    const exerciseGrid = document.querySelector('.exercise-container-grid');
    const pageContent = document.querySelector('.main-content-container');
    const showMenu = () => {
        buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
        menuContainer.classList.remove(menuHiddenClass);
        if (exerciseGrid) {
            CloseScreen(notificationScreen, exerciseGrid);
            return;
        }
        CloseScreen(notificationScreen, pageContent);
    };
    const closeMenu = () => {
        buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
        menuContainer.classList.add(menuHiddenClass);
    };
    if (buttonShowMenu) {
        buttonShowMenu.removeEventListener('click', showMenu);
        buttonShowMenu.addEventListener('click', showMenu);
    }
    if (buttonCloseMenu) {
        buttonCloseMenu.removeEventListener('click', closeMenu);
        buttonCloseMenu.addEventListener('click', closeMenu);
    }
    pageContent.addEventListener('click', closeMenu);
    const footer = document.querySelector('.main-footer');
    if (footer)
        footer.addEventListener('click', closeMenu);
    const notificationMenu = document.querySelector('#toggle-notification-menu');
    if (notificationMenu)
        notificationMenu.addEventListener('click', closeMenu);
})();
(() => {
    const linksLogout = document.querySelectorAll('.user-logout-link');
    const formLogout = document.querySelector('.form-logout');
    for (const link of linksLogout) {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            formLogout.submit();
        });
    }
})();
(() => {
    const passwordField = document.querySelector('#id_password');
    if (!passwordField)
        return;
    const icon = document.createElement('i');
    icon.className = 'show-password-icon fa-regular fa-eye';
    icon.id = 'show-password-icon';
    if (passwordField.classList.contains('login-password-field')) {
        passwordField.parentNode.insertBefore(icon, passwordField.nextSibling);
    }
    const showPasswordIcon = document.querySelector('.show-password-icon');
    if (!showPasswordIcon)
        return;
    let is_password_visible = false;
    showPasswordIcon.addEventListener('click', () => {
        if (is_password_visible) {
            passwordField.type = 'password';
            showPasswordIcon.classList.remove('fa-eye-slash');
            showPasswordIcon.classList.add('fa-eye');
        }
        else {
            passwordField.type = 'text';
            showPasswordIcon.classList.remove('fa-eye');
            showPasswordIcon.classList.add('fa-eye-slash');
        }
        is_password_visible = !is_password_visible;
    });
})();
(() => {
    const dismissMessageBtns = document.querySelectorAll('.dismiss-flash-message');
    if (dismissMessageBtns) {
        for (const btn of dismissMessageBtns) {
            btn.addEventListener('click', () => {
                const parentElement = btn.parentElement;
                if (parentElement.classList.contains('message')) {
                    parentElement.classList.add('hide-message');
                    ChangeDisplayAnimationEnd(parentElement);
                }
            });
        }
    }
})();
(() => {
    const selectField = document.querySelector('.form-group.multiple-select');
    if (!selectField)
        return;
    const selectLabel = selectField.querySelector('label');
    let labelText = selectLabel.innerText;
    selectField.addEventListener('change', () => {
        const icon = '<i class="fa-solid fa-circle-check"></i>';
        let selectCount = 0;
        selectField.querySelectorAll('option').forEach((option) => {
            if (!option.selected) {
                option.innerHTML = option.text;
                return;
            }
            option.innerHTML = `${icon} ${option.text}`;
            selectCount++;
        });
        selectLabel.innerHTML = `${labelText} &#8594; ${selectCount} ${icon}`;
    });
})();
