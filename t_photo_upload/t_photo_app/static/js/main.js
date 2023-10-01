(function ($) {
    "use strict";

    var active_page="#nav_"+$(".container-xxl").attr("id");
    $(active_page).css("color","var(--secondary)").css("text-decoration","underline");

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();


    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-150px');
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    $('#info-btn button').click (function() {
        var idx=$(this).attr("id");
        var item="#"+idx.replace("btn","items")
        $("#info-items span").removeClass("info-items-check");
        $("#info-items span").addClass("info-items");
        $(item).removeClass("info-items");
        $(item).addClass("info-items-check");
        return false;
        });

    $('#intro-btn button').click (function() {
        var idx=$(this).attr("id");
        var item="#"+idx.replace("btn","items")
        $("#intro-items span").removeClass("intro-items-check");
        $("#intro-items span").addClass("intro-items");
        $(item).removeClass("intro-items");
        $(item).addClass("intro-items-check");
        return false;
        });

    $('#manage-item button').click (function() {
        var idx=$(this).attr("id");
        var item="#"+idx.replace("btn","items")
        $(item).toggleClass("manage-edit");
        return false;
        });

    // Modal Video
    /*
    var $videoSrc;
    $('.btn-play').click(function () {
        $videoSrc = $(this).data("src");
    });
    console.log($videoSrc);
    $('#videoModal').on('shown.bs.modal', function (e) {
        $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
    })
    $('#videoModal').on('hide.bs.modal', function (e) {
        $("#video").attr('src', $videoSrc);
    })
    */

    // Product carousel
    $(".product-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        loop: true,
        center: true,
        dots: false,
        nav: true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
			0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });

})(jQuery);