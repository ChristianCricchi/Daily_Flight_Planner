/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    // Initialize Materialize CSS components
    $(".sidenav").sidenav({ edge: "right" });
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $('select').formSelect();

    // Initialize datepicker with custom options
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 5,
        showClearBtn: true,
        i18n: {
            done: "select"
        }
    });

    // Initialize collapsible and modal components
    $('.collapsible').collapsible();
    $('.modal').modal();
    
    // Handle confirm button click
    $('.confirm-btn').click(function (event) {
        event.preventDefault();
        var actionUrl = $(this).attr('href');
        $('#confirm-action').attr('href', actionUrl);
        $('#confirm-modal').modal('open');
    });

    // Handle update report button click
    $('#update-report-btn').click(function (event) {
        event.preventDefault();
        $('#confirm-action').attr('href', '#');
        $('#confirm-modal').modal('open');
    });

    // Handle confirm action click for report update
    $('#confirm-action').click(function () {
        $('#update-report-form').submit();
    });

 
    // Call function to validate Materialize select fields
    validateMaterializeSelect();

    // Function to validate Materialize select fields
    function validateMaterializeSelect() {
        // Define CSS classes for valid and invalid states
        let classValid = {
            "border-bottom": "1px solid #4caf50",
            "box-shadow": "0 1px 0 0 #4caf50"
        };
        let classInvalid = {
            "border-bottom": "1px solid #f44336",
            "box-shadow": "0 1px 0 0 #f44336"
        };

        // Set CSS for required select fields
        if ($("select.validate").prop("required")) {
            $("select.validate").css({
                "display": "block",
                "height": "0",
                "padding": "0",
                "width": "0",
                "position": "absolute"
            });
        }

        // Handle focus and click events on select dropdown
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            // Apply valid class on change if an option is selected
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            // Apply valid class if an option is already selected
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                // Apply invalid class on focusout if required and no option selected
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});



