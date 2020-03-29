$(document).on('click', '.header-top-nav-search > a', function() {
    $('.header-top-nav-search > a').fadeOut(200);
    $('.header-top-nav-search > form').delay(240).fadeIn(200);
})

$('.header-top-nav-menu-icon').on('click', function () {
    $('body').toggleClass('noscroll');
    $('.header-top-nav-menu-icon').toggleClass('open');
    $('.header-nav').toggleClass('mobile-nav mobile-nav-open');
});


$(document).on('click', '.dropdown-toggle', function (event) {
    $(this).parent().toggleClass('open');
});