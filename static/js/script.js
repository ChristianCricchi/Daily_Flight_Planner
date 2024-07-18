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
});