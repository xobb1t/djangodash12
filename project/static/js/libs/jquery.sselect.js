/*!
Sselect.
Version: 1.1 (05.07.2012)
https://github.com/trolev/sslect/

$(document).ready(function(){
  $('select').sselect({
    create:     function(selected){},
    select:     function(selected){}
  });
});
*/

jQuery.fn.sselect = function(options){
  var settings = jQuery.extend({
    create:     function(selected){},
    select:     function(selected){}
  },options);
  this.each(function() {
    var $input = $(this);
    if (!$input.is('select')) {
      var $input = $('select', this);
      if (!$input.length) {
        alert('error sselect');
        return;
      }
    }
    var reset = $input.next(".sselect").length;
    if (!reset) {
      create($input);
    }
    var $sselect = $input.next(".sselect");
    var $stxt = $('.sselect-text', $sselect);
    var $txt = $('.txt', $sselect);
    var $list = $('.sselect-list', $sselect);
    var ul = "";
    if ($('optgroup', $input).length) {
      $('optgroup', $input).each(function() {
        var $this = $(this);
        var label = $this.attr('label') ? $this.attr('label') : '';
        ul += '<span class="sselect-label">' + label + '</span>';
        ul += createUl($this);
      });
    } else {
      ul += createUl($input)
    }
    $list.html(ul);
    settings.create($(':selected', $input), $list);
    $stxt.unbind('click.sselect').bind('click.sselect',function() {
      $sselect.toggleClass('sselect-open');
      $('.sselect-open').not($sselect).removeClass('sselect-open');
      return false; 
    });
    fun_selected($input, $txt, $list);
    $input.unbind('change.sselect').bind('change.sselect', function () {
      fun_selected($input, $txt, $list);
      settings.select($(':selected', $input));
    });
    $('a', $list).unbind('click.sselect').bind('click.sselect', function(e){
      var index = $('a', $list).index($(e.target));
      $('option', $input).eq(index).attr("selected", "selected");
      $input.change();
      return false;
    });
    $input.hide();
  });
};
function create($input) {
  $input.after('<div class="sselect"><div class="sselect-text"><span class="txt"></span><i class="icon"></i></div><div class="sselect-list"></div></div>');
}
function createUl($input){
  var l = "<ul class='sselect-ul'>";
  $('option', $input).each(function(){
    var $this = $(this);
    var option = $this.text();
    l += "<li><a href='#'>" + option + "</a></li>"
  });
  l += "</ul>";
  return l;
}
function fun_selected($input, $txt, $list) {
  var selected = $(':selected', $input);
  var index = $('option', $input).index(selected);
  $txt.html(selected.text());
  $('.selected', $list).removeClass('selected');
  $('li', $list).eq(index).addClass('selected');
  $('.sselect-open').removeClass('sselect-open');
}
$(document).unbind().bind('click', function(e){
  if ($(e.target).closest('.sselect').length) {
    return;
  } else {
    $('.sselect-open').removeClass('sselect-open');
  }
});