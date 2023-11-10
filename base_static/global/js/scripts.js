// função para mostrar / esconder o menu
(() => {
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const buttonCloseMenu = document.querySelector('.button-close-menu');
    const menuContainer = document.querySelector('.menu-container');
    const buttonShowMenuVisibleClass = 'button-show-menu-is-visible';
    const menuHiddenClass = 'menu-hidden';

    const showMenu = () => {
        buttonShowMenu.classList.remove(buttonShowMenuVisibleClass)
        menuContainer.classList.remove(menuHiddenClass)
    };

    const closeMenu = () => {
        buttonShowMenu.classList.add(buttonShowMenuVisibleClass)
        menuContainer.classList.add(menuHiddenClass)
    };

    if (buttonShowMenu) {
        buttonShowMenu.removeEventListener('click', showMenu);
        buttonShowMenu.addEventListener('click', showMenu);
    };

    if (buttonCloseMenu) {
        buttonCloseMenu.removeEventListener('click', closeMenu);
        buttonCloseMenu.addEventListener('click', closeMenu);
    };
})();

// função para enviar formulários de logout
(() => {
    const linksLogout = document.querySelectorAll('.user-logout-link')
    const formLogout = document.querySelector('.form-logout')

    for (const link of linksLogout) {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            formLogout.submit();
        })
    }
})();


// função para mostrar / esconder a senha no form de login

(() => {
    const passwordField = document.querySelector('#id_password');
    const showPasswordBtnShow = document.querySelector('#show-password');

    if (!showPasswordBtnShow) {
        return
    }

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

// funções para tela de filtros

function PreventUserClicksOnBody(e) {
    e.preventDefault();
    e.stopPropagation();
}

function AdjustElementOpacity(element, value) {
    element.style.opacity = value;
}

function AdjustElementDisplay(element, value) {
    element.style.display = value;
}

(() => {
    const filtersButton = document.querySelector('.filters-button');
    const filtersScreen = document.querySelector('.filters-page');
    const closeFiltersButton = document.querySelector('#close-filters-page');
    const exerciseGrid = document.querySelector('.exercise-container-grid');

    // abre a tela de filtros
    if (filtersButton) {
        filtersButton.addEventListener('click', () => {
            AdjustElementDisplay(filtersScreen, 'inline');
            AdjustElementOpacity(exerciseGrid, 0.4),
                exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
        })
    }

    if (closeFiltersButton) {
        // fecha a tela de filtros
        closeFiltersButton.addEventListener('click', () => {
            AdjustElementDisplay(filtersScreen, 'none');
            AdjustElementOpacity(exerciseGrid, 1);
            exerciseGrid.removeEventListener('click', PreventUserClicksOnBody);
        })
    }
})();