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

// settar display para none ao final de uma animação
function ChangeDisplayAnimationEnd(element) {
  element.addEventListener(
    'animationend',
    () => {
      element.style.display = 'none';
    },
    { once: true },
  );
}

// fechar telas que 'flutuam' na página
function CloseScreen(screen_to_close, background) {
  if (screen_to_close && background) {
    AdjustElementDisplay(screen_to_close, 'none');
    AdjustElementOpacity(background, 1);
    background.removeEventListener('click', PreventUserClicksOnBody);
  }
}

(() => {
  // notifications vars
  const notificationScreen = document.querySelector('.notifications-page');
  const notificationBtn = document.querySelector('#toggle-notification-menu');
  const closeNotificationsBtn = document.querySelector(
    '#close-notifications-page',
  );

  // pages
  const exerciseGrid = document.querySelector('.exercise-container-grid');
  const pageContent = document.querySelector('.main-content-container');

  /* menu de notificações */
  if (notificationBtn)
    notificationBtn.addEventListener('click', () => {
      AdjustElementDisplay(notificationScreen, 'inline');

      // se exerciseGrid existir na tela
      if (exerciseGrid) {
        exerciseGrid.addEventListener('click', PreventUserClicksOnBody);
        AdjustElementOpacity(exerciseGrid, 0.4);
        return;
      }

      // caso contrário usar pagecontent
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

// função para mostrar / esconder o menu

(() => {
  // menu
  const buttonShowMenu = document.querySelector('.button-show-menu');
  const buttonCloseMenu = document.querySelector('.button-close-menu');
  const menuContainer = document.querySelector('.menu-container');
  const buttonShowMenuVisibleClass = 'button-show-menu-is-visible';
  const menuHiddenClass = 'menu-hidden';

  // notification screen
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
    link.addEventListener('click', (e) => {
      e.preventDefault();
      formLogout.submit();
    });
  }
})();

// função para mostrar / esconder a senha no form de login

(() => {
  // campo de input para password
  const passwordField = document.querySelector('#id_password');

  if (!passwordField) return;

  // criando icone fa-eye no html
  const icon = document.createElement('i');
  icon.className = 'show-password-icon fa-regular fa-eye';
  icon.id = 'show-password-icon';

  // inserindo icone na tela se tiver a classe certa (evitar com que apareça em outros forms)
  if (passwordField.classList.contains('login-password-field')) {
    passwordField.parentNode.insertBefore(icon, passwordField.nextSibling);
  }

  const showPasswordIcon = document.querySelector('.show-password-icon');

  if (!showPasswordIcon) return;

  let is_password_visible = false;

  showPasswordIcon.addEventListener('click', () => {
    if (is_password_visible) {
      passwordField.type = 'password';
      showPasswordIcon.classList.remove('fa-eye-slash');
      showPasswordIcon.classList.add('fa-eye');
    } else {
      passwordField.type = 'text';
      showPasswordIcon.classList.remove('fa-eye');
      showPasswordIcon.classList.add('fa-eye-slash');
    }
    is_password_visible = !is_password_visible;
  });
})();

// remover flash messages da tela
(() => {
  const dismissMessageBtns = document.querySelectorAll(
    '.dismiss-flash-message',
  );

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

// adicionar icone de check ao selecionar uma opção nos formulários que possuem a tag <select>
(() => {
  const selectField = document.querySelector('.form-group.multiple-select');

  if (!selectField) return;

  const selectLabel = selectField.querySelector('label');
  let labelText = selectLabel.innerText;

  // adicionar ícones quando o selected mudar - change
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
