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
  $('#js-sblog form').submit(function(){
    var $this = $(this);
    var $block = $this.closest('#js-sblog');
    var action = $this.data('action');
    var data_form = $this.serialize();
    // $.ajax({
    //   url: action,
    //   type: "POST",
    //   data: data_form,
    //   success: function(data){
    //     $block.html(data.content);
    //     $('#js-tr .disabled, #js-br .disabled').removeClass('disabled');
    //     $('#js-github').attr('href', data.githab);
    //     $('#js-github').attr({'data-content': 'Sign in via OAuth2 protocol'});
    //   }
    // });
    $('#js-tr .disabled, #js-br .disabled').removeClass('disabled');
    $('#js-github').attr({'href': 'data.githab'});
    $('#js-github').attr({'data-content': 'Sign in via OAuth2 protocol'});
    return false;
  });

  $('#js-repo form').submit(function(){
    var $this = $(this);
    var $block = $this.closest('#js-repo');
    var action = $this.data('action');
    var data_form = $this.serialize();
    // $.ajax({
    //   url: action,
    //   type: "POST",
    //   data: data_form,
    //   success: function(data){
    //     $block.html(data.content);
    //     $('#js-tr .disabled, #js-br .disabled').removeClass('disabled');
    //     $('#js-github').attr('href', data.githab);
    //     $('#js-github').attr({'data-content': 'Sign in via OAuth2 protocol'});
    //   }
    // });
    alert(3);
    return false;
  });

});