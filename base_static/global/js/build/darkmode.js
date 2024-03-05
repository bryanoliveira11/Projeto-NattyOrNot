"use strict";
(() => {
    const toggleDarkbtn = document.querySelector('#toggle-dark-mode');
    const mainContent = document.querySelector('body');
    const exerciseCardsBackground = document.querySelectorAll('.exercise-card-background');
    const tableElement = document.querySelector('.content-table');
    const tableTr = document.querySelectorAll('.table-tr');
    const notifications = document.querySelectorAll('.notification');
    const generalIcons = document.querySelectorAll('.general-icon');
    handlePageLoad();
    if (localStorage.getItem('darkmode') === null) {
        localStorage.setItem('darkmode', 'false');
    }
    if (!toggleDarkbtn)
        return;
    toggleDarkbtn.addEventListener('click', () => {
        const isDark = localStorage.getItem('darkmode');
        localStorage.setItem('darkmode', isDark === 'true' ? 'false' : 'true');
        changePageColors();
        changeMenuIcon();
    });
    function handlePageLoad() {
        document.addEventListener('DOMContentLoaded', () => {
            changePageColors();
            changeMenuIcon();
        });
    }
    function changePageColors() {
        const isDark = localStorage.getItem('darkmode');
        if (isDark === 'true')
            toggleDarkMode();
        else
            removeDarkMode();
    }
    function toggleDarkMode() {
        addClassList(mainContent, 'dark-mode-style');
        addClassList(tableElement, 'dark-mode-table');
        nodeListAddClass(tableTr, 'tr-dark');
        nodeListAddClass(exerciseCardsBackground, 'dark-mode-cards');
        nodeListAddClass(notifications, 'dark-mode-style');
        nodeListAddClass(generalIcons, 'dark-mode-style');
    }
    function removeDarkMode() {
        removeClassList(mainContent, 'dark-mode-style');
        removeClassList(tableElement, 'dark-mode-table');
        nodeListRemoveClass(tableTr, 'tr-dark');
        nodeListRemoveClass(exerciseCardsBackground, 'dark-mode-cards');
        nodeListRemoveClass(notifications, 'dark-mode-style');
        nodeListRemoveClass(generalIcons, 'dark-mode-style');
    }
    function changeMenuIcon() {
        const menuIcon = document.querySelector('#menu-icon');
        const isDark = localStorage.getItem('darkmode');
        if (isDark === 'true') {
            menuIcon.classList.remove('fa-moon');
            menuIcon.classList.add('fa-sun');
        }
        else {
            menuIcon.classList.remove('fa-sun');
            menuIcon.classList.add('fa-moon');
        }
    }
    function addClassList(element, class_to_add) {
        if (element)
            element.classList.add(class_to_add);
    }
    function removeClassList(element, class_to_remove) {
        if (element)
            element.classList.remove(class_to_remove);
    }
    function nodeListAddClass(nodelist, class_to_add) {
        if (nodelist) {
            for (const element of nodelist)
                addClassList(element, class_to_add);
        }
    }
    function nodeListRemoveClass(nodelist, class_to_remove) {
        if (nodelist) {
            for (const element of nodelist)
                removeClassList(element, class_to_remove);
        }
    }
})();
