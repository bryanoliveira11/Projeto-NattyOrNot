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

    if(buttonShowMenu){
        buttonShowMenu.removeEventListener('click', showMenu);
        buttonShowMenu.addEventListener('click', showMenu);
    };

    if(buttonCloseMenu){
        buttonCloseMenu.removeEventListener('click', closeMenu);
        buttonCloseMenu.addEventListener('click', closeMenu);
    };
})();

// função para enviar formulários de logout
(() => {
    const linksLogout = document.querySelectorAll('.user-logout-link')
    const formLogout = document.querySelector('.form-logout')

    for(const link of linksLogout){
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

    if(!showPasswordBtnShow){
        return
    }

    const showPasswordIcon = document.querySelector('#show-password-icon');
    const showPasswordText = document.querySelector('#show-password-text');
    let is_password_visible = false;

    showPasswordBtnShow.addEventListener('click', () => {
        if(is_password_visible){
            passwordField.type = 'password';
            showPasswordIcon.classList.remove('fa-eye-slash');
            showPasswordIcon.classList.add('fa-eye');
            showPasswordText.innerHTML = 'Mostrar';
        }
        else{
            passwordField.type = 'text';
            showPasswordIcon.classList.remove('fa-eye');
            showPasswordIcon.classList.add('fa-eye-slash'); 
            showPasswordText.innerHTML = 'Esconder';
        }
        is_password_visible = !is_password_visible;
    });
})();


// função para confirmar a deleção de um exercício na página do dashboard

(() => {
    const forms = document.querySelectorAll('.form-delete');
 
    for(const form of forms){
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const confirmed = confirm('Isso ira Deletar o Exercício, Confirmar ?');

            if(confirmed){
                form.submit();
            }

        });
    }

})();