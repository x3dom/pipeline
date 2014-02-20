function init3dhop() {
	$('#toolbar img')
		.hover(function(){
			$(this).animate({opacity:'0.8'}, {queue:false,duration:100});
			}, function(){
			$(this).animate({opacity:'0.5'}, {queue:true,duration:100});
			})
		.click(function() {
			actionsToolbar($(this).attr('id'));
			$(this).animate({opacity:'1.0'}, {queue:true,duration:100});
			$(this).animate({opacity:'0.8'}, {queue:true,duration:100});
			return false;
		});

	$('#3dhop')
		.on('contextmenu', function(e){ //don't allow to open contextual menu (right click)
			return false; 
		});	
				
    resizeCanvas($('#3dhop').width(),$('#3dhop').height());
	
	set3dhlg();	
} 

function lightSwitch() {
  var on = presenter.isLightTrackballEnabled();

  var pat = new RegExp(".*/","g");
  var base = pat.exec(String($('#light').attr("src")));
  if(on)
    $('#light').attr("src", base + "light_on.png");
  else 
    $('#light').attr("src", base + "light.png");
} 

function moveToolbar(l,t) {
  $('#toolbar').css('margin-left', l);
  $('#toolbar').css('margin-top', t);	
} 

function resizeCanvas(w,h) {
  $('#draw-canvas').attr('width', w);
  $('#draw-canvas').attr('height',h);
  $('#3dhop').css('width', w);
  $('#3dhop').css('height', h);  
  $('#tdhlg').css('margin-left', w-115);
  $('#tdhlg').css('margin-top', h-15);
}

function set3dhlg() {	
  $('#tdhlg').text("Powered by 3D HOP");	
  $('#tdhlg').click(function() { window.open('http://vcg.isti.cnr.it/~potenziani/test/sites/3dhop', '_blank') }); 	  
} 
