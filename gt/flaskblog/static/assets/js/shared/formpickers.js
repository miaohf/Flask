(function($) {
    'use strict';
    if ($("#timepicker-example").length) {
        $('#timepicker-example').datetimepicker({
            format: 'LT'
        });
    }
    if ($(".color-picker").length) {
        $('.color-picker').asColorPicker();
    }
    if ($("#start-datepicker").length) {
        $('#start-datepicker').datepicker({
            enableOnReadonly: true,
            todayHighlight: true,
        });
    }
    if ($("#end-datepicker").length) {
        $('#end-datepicker').datepicker({
            enableOnReadonly: true,
            todayHighlight: true,
        });
    }
    if ($("#renewalstart-datepicker").length) {
        $('#renewalstart-datepicker').datepicker({
            enableOnReadonly: true,
            todayHighlight: true,
        });
    }
    if ($("#renewalend-datepicker").length) {
        $('#renewalend-datepicker').datepicker({
            enableOnReadonly: true,
            todayHighlight: true,
        });
    }
    if ($("#auction-datepicker").length) {
        $('#auction-datepicker').datepicker({
            enableOnReadonly: true,
            todayHighlight: true,
        });
    }
    if ($(".datepicker-autoclose").length) {
        $('.datepicker-autoclose').datepicker({
            autoclose: true
        });
    }
    if ($('input[name="date-range"]').length) {
        $('input[name="date-range"]').daterangepicker();
    }
    if ($('input[name="date-time-range"]').length) {
        $('input[name="date-time-range"]').daterangepicker({
            timePicker: true,
            timePickerIncrement: 30,
            locale: {
                format: 'MM/DD/YYYY h:mm A'
            }
        });
    }
})(jQuery);