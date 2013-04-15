
$(document).ready(function(){

    $('#meta-upload').hide();
    $('#input_group_url').hide();


    $('#radio-meta').click(function() {
        $('#meta-upload').slideDown();
    });
    $('#radio-basic, #radio-none').click(function() {
        $('#meta-upload').slideUp();
    });

    $('#toggle_input_file').click(function(e) {
        $('#input_group_file').hide();
        $('#input_group_url').show();
        e.preventDefault();
    })

    $('#toggle_input_url').click(function(e) {
        $('#input_group_file').show();
        $('#input_group_url').hide();
        e.preventDefault();
    })


    $('abbr').tooltip();

    // generic toggler
    $('a.toggler').each(function() {
        // hide all elements with ids given in hrefs
        $($(this).attr('href')).hide();
    })
    $('a.toggler').each(function() {
        $(this).click(function(e) {
            e.preventDefault();
            var elem = $($(this).attr('href'));
            var link = $(this);
            elem.slideToggle('fast', function() {

            if ($(this).is(':visible')) {
                link.text(link.attr('data-toggle-on'))
            } else {
                link.text(link.attr('data-toggle-off'))
            }

            });
        });
    });




});

// http://zanstra.home.xs4all.nl/picks/progress.html
function AnimatedDiv(id,frames,wait,dir) {
  this.id=id;
  this.element=document.getElementById(id);
  this.frames=frames;
  this.index=0;
  this.dir=dir||'round-robin';
  this.wait=wait;
}
AnimatedDiv.prototype={
  animate: function() {
    var self=this;
    self.element.innerHTML=self.frames[self.index];
    self.advanceFrame();
    return window.setTimeout(function(){self.animate();},self.wait);
  },
  advanceFrame: function() {
    switch(this.dir) {
    case 'round-robin':
      if(++this.index>=this.frames.length) this.index=0;
      break;
    case 'right':
      if(++this.index>=this.frames.length) {
        this.index-=2;
        this.dir='left';
      }
      break;
    case 'left':
      if(--this.index<0) {
        this.index+=2;
        this.dir='right';
      }
      break;
    default:
      throw new Error('Unknown direction ('+this.id+' '+this.dir+')');
    }
  }
}



