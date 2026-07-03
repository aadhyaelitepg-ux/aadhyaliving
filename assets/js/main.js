(function($){
	"use strict";

	// Mean Menu
	$('.mean-menu').meanmenu({
		meanScreenWidth: "991"
	});

	// Header Sticky
	$(window).on('scroll',function() {
		if ($(this).scrollTop() > 120){  
			$('.navbar-area').addClass("is-sticky");
		}
		else{
			$('.navbar-area').removeClass("is-sticky");
		}
	});



	// locations-slides
	$('.locations-slides').owlCarousel({
		nav: true,
		loop: false,
		margin: 25,
		dots: true,
		autoplay: true,
		autoplayHoverPause: true,
		navText: [
			"<i class='ri-arrow-left-line'></i>",
			"<i class='ri-arrow-right-line'></i>",
		],
		responsive: {
			0: {
				items: 1
			},
			576: {
				items: 2
			},
			768: {
				items: 3
			},
			992: {
				items: 3
			},
			1200: {
				items: 3
			}
		}
	});

	// Feedback Slides
	$('.feedback-slides').owlCarousel({
		nav: true,
		loop: false,
		margin: 25,
		dots: false,
		autoplay: true,
		autoplayHoverPause: true,
		// nav: false,
		// loop: false,
		// margin: 25,
		// dots: true,
		// center: true,
		// autoplay: true,
		// autoplayHoverPause: true,
		navText: [
			// "<i class='ri-arrow-left-s-line'></i>",
			// "<i class='ri-arrow-right-s-line'></i>",
			"<i class='ri-arrow-left-line'></i>",
			"<i class='ri-arrow-right-line'></i>",
		],
		responsive: {
			0: {
				items: 1
			},
			576: {
				items: 1
			},
			768: {
				items: 2
			},
			992: {
				items: 3
			},
			1200: {
				items: 3
			}
		}
	});


	// AOS
	AOS.init();

	// Go to Top
	$(function(){
		// Scroll Event
		$(window).on('scroll', function(){
			var scrolled = $(window).scrollTop();
			if (scrolled > 600) $('.go-top').addClass('active');
			if (scrolled < 600) $('.go-top').removeClass('active');
		});  
		// Click Event
		$('.go-top').on('click', function() {
			$("html, body").animate({ scrollTop: "0" },  500);
		});
	});

	

}(jQuery));