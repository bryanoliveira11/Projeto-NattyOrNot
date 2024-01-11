// funções para as telas de filtros e notificações do usuário

// evita que o usuário clique em algum elemento da tela
function PreventUserClicksOnBody(e) {
    e.preventDefault();
    e.stopPropagation();
}

// ajusta opacidade de um elemento
function AdjustElementOpacity(element, value) {
    if (element) element.style.opacity = value;
}

// define o style de display do elemento
function AdjustElementDisplay(element, value) {
    if (element) element.style.display = value;
}

// adicionar animação de fadeIn nas telas
function ToggleFadeInAnimation(screen) {
    screen.classList.add('fadeIn-screen');
    AdjustElementDisplay(screen, 'inline');
}

// settar display para none ao final de uma animação
function ChangeDisplayAnimationEnd(element) {
    element.addEventListener('animationend', () => {
        element.style.display = 'none';
    }, { once: true });
}

// fechar telas que 'flutuam' na página
function CloseScreen(screen_to_close, background) {
    if (screen_to_close && background) {
        screen_to_close.classList.remove('fadeIn-screen');
        screen_to_close.style.display = 'none';
        AdjustElementOpacity(background, 1);
        background.removeEventListener('click', PreventUserClicksOnBody);
    }
}

(() => {
    const filtersButton = document.querySelector('.filters-button');
    const filtersScreen = document.querySelector('.filters-page');
    const closeFiltersButton = document.querySelector('#close-filters-page');
    const exerciseGrid = document.querySelector('.exercise-container-grid');
    const notificationScreen = document.querySelector('.notifications-page');
    const notificationBtn = document.querySelector('#toggle-notification-menu');
    const closeNotificationsBtn = document.querySelector('#close-notifications-page');
    const pageContent = document.querySelector('.main-content-container');

    /* menu de filtros */

    if (filtersButton) filtersButton.addEventListener('click', () => {
        // fechar tela de notificações se estiver aberta
        if (notificationScreen) CloseScreen(notificationScreen, exerciseGrid);

        // animação de fadeIn
        ToggleFadeInAnimation(filtersScreen);
        AdjustElementDisplay(filtersScreen, 'inline');
        AdjustElementOpacity(exerciseGrid, 0.4);
        exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
    });

    // fecha a tela de filtros
    if (closeFiltersButton) closeFiltersButton.addEventListener('click', () => {
        CloseScreen(filtersScreen, exerciseGrid);
    });


    /* menu de notificações */

    if (notificationBtn) notificationBtn.addEventListener('click', () => {
        // fechar tela de filtros se estiver aberta
        if (filtersScreen) CloseScreen(filtersScreen, pageContent);

        // animação de fadeIn
        ToggleFadeInAnimation(notificationScreen);

        // se exerciseGrid existir na tela
        if (exerciseGrid) {
            exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
            AdjustElementOpacity(exerciseGrid, 0.4);
            return;
        };

        // caso contrário usar pagecontent
        pageContent.addEventListener('click', PreventUserClicksOnBody);
        AdjustElementOpacity(pageContent, 0.4);
    });

    if (closeNotificationsBtn) closeNotificationsBtn.addEventListener('click', () => {
        if (exerciseGrid) {
            CloseScreen(notificationScreen, exerciseGrid);
            return;
        };

        CloseScreen(notificationScreen, pageContent);
    });

})();

// função para mostrar / esconder o menu

(() => {
    // menu
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const buttonCloseMenu = document.querySelector('.button-close-menu');
    const menuContainer = document.querySelector('.menu-container');
    const buttonShowMenuVisibleClass = 'button-show-menu-is-visible';
    const menuHiddenClass = 'menu-hidden';

    // filters & notification screen 
    const filtersScreen = document.querySelector('.filters-page');
    const notificationScreen = document.querySelector('.notifications-page');
    const exerciseGrid = document.querySelector('.exercise-container-grid');
    const pageContent = document.querySelector('.main-content-container');

    const showMenu = () => {
        buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
        menuContainer.classList.remove(menuHiddenClass);

        if (exerciseGrid) {
            CloseScreen(filtersScreen, exerciseGrid);
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
    };

    if (buttonCloseMenu) {
        buttonCloseMenu.removeEventListener('click', closeMenu);
        buttonCloseMenu.addEventListener('click', closeMenu);
    };

    // fechar menu ao clicar na tela
    pageContent.addEventListener('click', closeMenu);

    // fechar menu ao clicar no footer
    const footer = document.querySelector('.main-footer');
    if (footer) footer.addEventListener('click', closeMenu);

    // fechar menu ao abrir notifications
    const notificationMenu = document.querySelector('#toggle-notification-menu');
    if (notificationMenu) notificationMenu.addEventListener('click', closeMenu);
})();


// função para enviar formulários de logout
(() => {
    const linksLogout = document.querySelectorAll('.user-logout-link');
    const formLogout = document.querySelector('.form-logout');

    for (const link of linksLogout) {
        link.addEventListener('click', e => {
            e.preventDefault();
            formLogout.submit();
        })
    }
})();


// função para mostrar / esconder a senha no form de login

(() => {
    const passwordField = document.querySelector('#id_password');
    const showPasswordBtnShow = document.querySelector('#show-password');

    if (!showPasswordBtnShow) return;

    const showPasswordIcon = document.querySelector('#show-password-icon');
    const showPasswordText = document.querySelector('#show-password-text');
    let is_password_visible = false;

    showPasswordBtnShow.addEventListener('click', () => {
        if (is_password_visible) {
            passwordField.type = 'password';
            showPasswordIcon.classList.remove('fa-eye-slash');
            showPasswordIcon.classList.add('fa-eye');
            showPasswordText.innerHTML = 'Mostrar';
        }
        else {
            passwordField.type = 'text';
            showPasswordIcon.classList.remove('fa-eye');
            showPasswordIcon.classList.add('fa-eye-slash');
            showPasswordText.innerHTML = 'Esconder';
        }
        is_password_visible = !is_password_visible;
    });
})();


// remover flash messages da tela
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
            })
        }
    }
})();


// função para confirmar a deleção de um exercício na página do dashboard

/* (() => {
    const forms = document.querySelectorAll('.form-delete');

    for (const form of forms) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const confirmed = confirm('Confirmar Deleção ?');

            if (confirmed) {
                form.submit();
            }

        });
    }

})();
*/