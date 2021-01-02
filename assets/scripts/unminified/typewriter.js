$('.typewriter').css('display', 'none');

setTimeout(function() {
  $('.typewriter').css('display', 'flex');

  var str = $('.typewriter').html(),
  i = 0,
  isTag,
  text,
  cursor = "_",
  timer;

  (function type() {
    text = str.slice(0, ++i);
    if (text === str){ 
        i = 0;
      blink();
      return;
    }
    $('.typewriter').html(text + " " + cursor);
    timer = setTimeout(type, 20);
  }());
  
  function blink() {
    i++;
    const foo = str + " " + (i%2 ? cursor : '');
    $('.typewriter').html(foo);
    timer = setTimeout(blink, 600);
  }
  
  function fade() {
      $('.typewriter').html(str);
  }
  
}, 300);