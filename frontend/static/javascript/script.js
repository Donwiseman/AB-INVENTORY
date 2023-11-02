$(document).ready(function(){
    $(".sub-btn").click(function(){
        $(this).next('.sub-menu').slideToggle()
        $(this).find('.dropdown').toggleClass('rotate')
    })

    $('.menu-btn').click(function(){
        $('.side-bar').addClass('active')
    })

    $('.clo-btn').click(function(){
        $('.side-bar').removeClass('active')
    })
})