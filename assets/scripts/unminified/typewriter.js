$('.typewriter').css('display', 'none');

setTimeout(function() {
  $('.typewriter').css('display', 'flex');

  var str = $('.typewriter').html(),
  i = 0,
  isTag,
  text,
  cursor = "█",
  timer;

  (function type() {
    text = str.slice(0, ++i);
    if (text === str){ 
        i = 0;
      blink();
      return;
    }
    $('.typewriter').html(text + " " + cursor);
    timer = setTimeout(type, 40);
  }());
  
  function blink() {
    i++;
    const foo = str + " " + (i%2 ? cursor : '');
    $('.typewriter').html(foo);
    if (i < 10) timer = setTimeout(blink, 600);
    else fade();
  }
  
  function fade() {
      $('.typewriter').html(str);
  }
  
}, 300);