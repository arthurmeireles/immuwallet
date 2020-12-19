// jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    try{
      if ($(".navbar").offset().top > 150) {
          $(".navbar-fixed-top").addClass("top-nav-collapse");
      } else {
          $(".navbar-fixed-top").removeClass("top-nav-collapse");
      }
    }catch(err){
      $(".navbar-fixed-top").addClass("top-nav-collapse");
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

$(document).ready(function(){
  $("#toggle_container").hide();
  $(".box-search").hide();

  $('.reveal').click(function() {
    $("#toggle_container").fadeIn( "slow" );
  });
  $('.reveal-box-search').click(function() {
    $(".box-search").fadeIn( "slow" );
  });
});
