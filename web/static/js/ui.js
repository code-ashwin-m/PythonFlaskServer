let body = document.body;
let profile = document.querySelector('.header .flex .profile');
let search_form = document.querySelector('.header .flex .search-form');
let sidebar = document.querySelector('.sidebar');

document.querySelector('#btn-profile').onclick = () => {
    search_form.classList.remove('active');
    profile.classList.toggle('active');
}

document.querySelector('#btn-search2').onclick = () => {
    profile.classList.remove('active');
    search_form.classList.toggle('active');
}

document.querySelector('#btn-sidebar').onclick = () => {
    sidebar.classList.toggle('active');
    body.classList.toggle('active');
}

document.querySelector('.sidebar-close').onclick = () => {
    sidebar.classList.remove('active');
    body.classList.remove('active');
}

window.onscroll = () => {
    profile.classList.remove('active');
    search_form.classList.remove('active');

    if (window.innerWidth < 1200){
        sidebar.classList.remove('active');
        body.classList.remove('active');
    }
} 