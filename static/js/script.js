/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 5,
        showClearBtn: true,
        i18n: {
            done: "select"
        }
    });

    $(document).ready(function(){
        $('.collapsible').collapsible();
        $('.modal').modal();
        
        $('.confirm-btn').click(function(event) {
            event.preventDefault();
            var actionUrl = $(this).attr('href');
            $('#confirm-action').attr('href', actionUrl);
            $('#confirm-modal').modal('open');
        });
    });
 

    $(document).ready(function(){
        $('.collapsible').collapsible();
    });

    $(document).ready(function(){
        $('.collapsible').collapsible();
        $('.modal').modal();

        $('#update-report-btn').click(function(event) {
            event.preventDefault();
            $('#confirm-action').attr('href', '#');
            $('#confirm-modal').modal('open');
        });

        $('#confirm-action').click(function() {
            $('#update-report-form').submit();
        });
    });
  
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });

        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
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



