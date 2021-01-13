/*!
    * Start Bootstrap - Resume v6.0.1 (https://startbootstrap.com/template-overviews/resume)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
    */
// $(document).ready(function() {
//   $(function() {
//     $('#datetimepicker1').datetimepicker();
//     $('#datetimepicker2').datetimepicker({
//       useCurrent: false //Important! See issue #1075
//     });
//     $("#datetimepicker1").on("dp.change", function(e) {
//       $('#datetimepicker2').data("DateTimePicker").minDate(e.date);
//     });
//     $("#datetimepicker2").on("dp.change", function(e) {
//       $('#datetimepicker1').data("DateTimePicker").maxDate(e.date);
//     });
//   });
// });
(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#sideNav",
    });

    $('#datetimepickerfrom').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        defaultDate: new Date()
    });
    $('#datetimepickerto').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        defaultDate: new Date(),
    	useCurrent: false
    });

    $("#datetimepickerfrom").on("dp.change", function (e) {
        $('#datetimepickerto').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepickerto").on("dp.change", function (e) {
        $('#datetimepickerfrom').data("DateTimePicker").maxDate(e.date);
    });

    $('#confirm-delete').on('show.bs.modal', function(e) {
        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    });

    $('#sidebarCollapse').click(function () {
        if ( $('#sidebar-wrapper').css('margin-left') == '0px' ) {
            $('#sidebar-wrapper').css('margin-left', '-15rem');
        }else {
            $('#sidebar-wrapper').css('margin-left', '0px');
        }
    });
})(jQuery); // End of use strict