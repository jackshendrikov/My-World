$(window).on("load",function(){
     $('.spinner').hide();
     $('.app').css("display", "flex");
     $('.content-section-footer-title').css("display", "flex");
});

$(function () {
    $(".menu-link").click(function () {
        $(".menu-link").removeClass("is-active");
        $(this).addClass("is-active");
    });
});

$(function () {
    $(".main-header-link").click(function () {
        $(".main-header-link").removeClass("is-active");
        $(this).addClass("is-active");
    });
});

$(".search-bar input")
    .focus(function () {
        $(".header").addClass("wide");
    })
    .blur(function () {
        $(".header").removeClass("wide");
    });

const toggleButton = document.querySelector('.dark-light');

toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
});


$(document).mousemove(function(event) {
    let windowWidth = $(window).width();
    let windowHeight = $(window).height();

    let mouseXpercentage = Math.round(event.pageX / windowWidth * 100);
    let mouseYpercentage = Math.round(event.pageY / windowHeight * 100);

    $('html, body').css('background', 'radial-gradient(at ' + mouseXpercentage + '% ' + mouseYpercentage + '%, #614385, #516395)');
});