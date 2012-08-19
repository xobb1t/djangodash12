$(document).ready(function(){
  var loader = '<img src="' + __STATIC_URL__ + 'images/loader.gif" alt="loader" class="loader">'
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
    $block.html(loader);
    var action = $this.data('action');
    var github_url = $('#js-github').data('github');
    var data_form = $this.serialize();
    $.ajax({
      url: action,
      type: "POST",
      data: data_form,
      success: function(data){
        $block.html(data);
        $('#js-tr .disabled, #js-br .disabled').removeClass('disabled');
        $('#js-github').attr('href', github_url);
        $('#js-github').attr({'data-content': 'Sign in via OAuth2 protocol'});
      }
    });
    $('#js-tr .disabled, #js-br .disabled').removeClass('disabled');
    $('#js-github').attr({'href': 'data.githab'});
    $('#js-github').attr({'data-content': 'Sign in via OAuth2 protocol'});
    return false;
  });

  $('#js-repo form').submit(function(){
    var $this = $(this);
    var $block = $this.closest('#js-repo');
    $block.html(loader);
    var action = $this.data('action');
    var data_form = $this.serialize();
    var demo = '<p>Repo name: <strong>blog</strong></p><p>Domain: <strong>blog.com</strong></p>'
    var btnimport = '<div class="b-import" id="js-import"><a href="#?" class="btn btn-warning btn-large" data-action="/import/">IMPORT</a><div class="progress progress-warning hide"><div class="bar" style="width: 1%;"></div><span class="txt">In progress</span></div></div>'

            
    // $.ajax({
    //   url: action,
    //   type: "POST",
    //   data: data_form,
    //   success: function(data){
    //     if (!bata.key) {
    //       $('#js-bm').html(btnimport);
    //     }
    //     $block.html(demo);
    //   }
    // });
    $('#js-bm').html(btnimport);
    $block.html(demo);
    fun_import();
    return false;
  });
  function fun_import() {
    $('#js-import .btn').one('click' ,function() {
      var $this = $(this);
      var $iblock = $this.closest('#js-import');
      $this.hide();
      $('#js-import .progress').removeClass('hide');
      $('#js-tm img').toggleClass('hide');
      progress_interval = setInterval(fun_progress, 3000);
      return false;
    });
  }
  function fun_progress() {
    // var action = '/progress/';
    // $.ajax({
    //   url: action,
    //   type: "POST",
    //   success: function(data){ 
    //   }
    // });
    var n = 20;
    $('#js-import .bar').animate({'width': n + "%"});
  }

});