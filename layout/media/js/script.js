$(document).ready(function(){
  $('.js-popover').popover({
    placement: 'top'
  });
  $('.js-select select').sselect({
    create: function(selected, block){
      block.addClass('dssds');
      $('li:first', block).hide();
    }
  });
});