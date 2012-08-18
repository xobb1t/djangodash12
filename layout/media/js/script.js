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
  $('#js-save form').submit(function() {
    var $this = $(this);
    var $block = $this.closest('#js-save');
    var action = $this.data('action');
    var data_form = $this.serialize();
    // $.ajax({
    //   url: action,
    //   type: "POST",
    //   data: data_form,
    //   success: function(data){
    //     $block.html(data.content);
    //     $('.col-r disabled').removeClass('disabled');
    //     $('#js-github').attr('href', data.githab);
    //   }
    // });
    $('.col-r .disabled').removeClass('disabled');
    $('#js-github').attr({'href': 'data.githab'});
    return false;
  });
});