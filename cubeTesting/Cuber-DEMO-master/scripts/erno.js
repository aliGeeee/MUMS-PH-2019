/*              ·~=≠≠x#≠≠=-                         ·=≈≠xxx≠≈~-·              
            ·~≠#%&$$$$&%x≈~·                        ~=≠#%$$$$$&%x≈-           
          ~x&$$$$$$$x~·  -%~                        #≈   -≈&$$$$$$$#≈·        
        =%$$$$$$$$$$-  -≠$$-                        x$%=·  x$$$$$$$$$&≠-      
      -%$$$$$$$$$$$$$%%$$$≈                         ·&$$&%&$$$$$$$$$$$$&≠     
     ·&$$$$$$$$$$$$$$$$$&=                           ·#$$$$$$$$$$$$$$$$$$≈    
     ≈$$$$$$$$$$$$$$$$$#-                              ≈&$$$$$$$$$$$$$$$$$    
     ≈$$$$$$$$$$$$$$$$$                                 ≈$$$$$$$$$$$$$$$$$    
     ·%$$$$$$$$$$$$$$$≈                                  &$$$$$$$$$$$$$$$=    
      ~#$$$$$$$$$$$$&≈                                   ·#$$$$$$$$$$$$&x     
      #%%%&&$$$$$&%≈-     =-   ·-=≈≈xxxxxx≠≠=~-·  -=       =x%$$$$$$&&%%&-    
      ≈$$&&%###≠~-       ·$&≈x%&$$$$$$$$$$$$$$$%#≠&$-        ·-≈###%&&$$%     
       #$$$$$$$x        ·≈$$$$$$$$$$$$$$$$$$$$$$$$$$%≈-        -$$$$$$$$~     
       ·x&$$&&%##≈-   ~x&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#=·  ·=x#%&&&$&%=      
         -%&$$$$$$$≠=%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&x≈%$$$$$$$&≈        
           -=≠x#%&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%#≠=~·         
             ·~≠%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%≠=-·          
≈====≈≠≠≠xx#%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&%%#xx≠≠≈=≈
%&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&%
 ··-=x%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%x=-·· 
       -≈#&$$$$$$$$$$$$$$$$$$$$&$$$$$$$$$$$$$$&$$$$$$$$$$$$$$$$$$$$&#≈-       
          ·=%$$$$$$$$$$$$$$$$$$%=x%$$$$$$$$%≠~%$$$$$$$$$$$$$$$$$$%=·          
     ·-~≈≠x#%$$$$$$$$$$$$$$$$$$$x  -x$$$$≠·  x$$$$$$$$$$$$$$$$$$$%#x≠≈~-·     
   =≠&$$$$$%%%&$&%$$$$$$$$$$$$$$$%≠≠%$$$$%≠≠&$$$$$$$$$$$$$$$%&$&%%%$$$$$&≠~   
  -$&$&#≠==x&$$%%$$~~≠#&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&#≠~~$$%%$$&x==≠#%$%$=  
  ≈$$$~  ≈%$$#x&$$~    ·-=≠#%&&$$$$$$$$$$$$$$$$&%%#≠=-·    ~$$&x#$$%≈  -$$$x  
  ≠$$≠  #$$%-~%$#~           ··-~~==========~~-··           ~#$%~·%$$#  =$$#  
  ≠$%  ·$$#·-$&≈                                              ≠&$-·#$$·  #$#  
  ≈$=  ~$%  -$&                                                &$·  %$~  -$x  
  -&   ~$~   &≠                                                #%   ~$~   #=*/




/*


	TWIST NOTATION

	UPPERCASE = Clockwise to next 90 degree peg
	lowercase = Anticlockwise to next 90 degree peg



	FACE & SLICE ROTATION COMMANDS

	F	Front
	S 	Standing (rotate according to Front Face's orientation)
	B 	Back
	
	L 	Left
	M 	Middle (rotate according to Left Face's orientation)
	R 	Right
	
	U 	Up
	E 	Equator (rotate according to Down Face's orientation)
	D 	Down



	ENTIRE CUBE ROTATION COMMANDS
	
	X   Rotate entire cube according to Right Face's orientation
	Y   Rotate entire cube according to Up Face's orientation
	Z   Rotate entire cube according to Front Face's orientation



	NOTATION REFERENCES

	http://en.wikipedia.org/wiki/Rubik's_Cube#Move_notation
	http://en.wikibooks.org/wiki/Template:Rubik's_cube_notation


*/








var erno = {


	//  Roughly when did we last update this business?
	//  Used more for a console-based reality check whilst debugging
	//  rather than actual version control. (That's what Git's for!)

	version: 20131102.1337,


	//  How much output do we want in the browser's console?
	//  0 = None. 1 = Everything.

	verbosity: 1,


	//  We're using Three.js for sure, 
	//  but shall we render in CSS or SVG?
	//  Hint: We never finished building SVG support!

	renderMode: 'css',


	//  For convenience we're running the show in terms of "states".
	//  What would Jeff Raskin say?!
	//  This makes development super modular
	//  and can work as a template for some young'un 
	//  to make their own simple games.

	state: 'setup',
	stateFrames: 0,
	stateHistory: [ 'setup' ],


	//  When we're ready to change state we can automagically:
	//  1. Update our state history.
	//  2. Run any 'Teardown' scripts from the state we're leaving.
	//  3. See how many frames we spent in that state.
	//  4. Run any 'Setup' scripts for the state we're entering.

	changeStateTo: function( stateNext ){

		if( erno.state !== stateNext ){

			if( erno.verbosity >= 0.3 ){
		
				console.log( '< Exiting  "'+ erno.state +'" state at '+ erno.stateFrames +' frames.' )
				console.log( '> Entering "'+ stateNext +'" state.' )
			}
		
			var 
			teardown = erno.states[ erno.state +'Teardown' ],
			setup    = erno.states[ stateNext +'Setup' ]

			if( teardown instanceof Function ) teardown()
			if( setup    instanceof Function ) setup()
			erno.stateHistory.push( stateNext )
			erno.state = stateNext	
			erno.stateFrames = 0
		}
		return false
	},


	//  Every 'state' is a Function that can be called by our window.loop() Function.
	//  Any 'Setup' or 'Teardown' states are automatically called by racer.changeStateTo().

	states: {




		//  This setup() is our chance to get everything in order *before*
		//  actually doing anything.
		//  We need to honor all accumulated requests in window.setupTasks[].

		setup: function(){

			console.log( '\nCuber', erno.version )
			console.log( '' )


			//  Not everyone's comfortable with exploring source code,
			//  particularly via the command-line.
			//  If they went through the trouble to open the JavaScript console
			//  let's give them a quick sampling of what's out there.

			window.help = (function(){

				var s = ''

				s += 'This Rubik\'s Cube simulator is run by the "erno" Object.'
				s += '\nType "erno" in this console and hit Enter for a summary.'
				s += '\nHere are some random commands to pique your interest:'
				s += '\n\n  cube.inspect()'
				s += '\n  cube.inspect( true )'
				s += '\n  cube.front'
				s += '\n  cube.front.northWest.inspect()'
				s += '\n  cube.front.northWest.up.color.name'
				s += '\n  cube.standing.setOpacity( 0.5 )'
				s += '\n  cube.corners.setRadius( 90 )'
				s += '\n  cube.solve()'
				s += '\n\nThis code was written by stewd.io and has been modified for the nefarious purposes of the MUMS Puzzle Hunt Commitee by Alec Barber.'
				s += '\n\nType "help" to view this message again.'
				return s + '\n'

			})()
			console.log( help )


			//  If we have any tasks to complete at setup time
			//  this is the place to do it!

			if( window.setupTasks )	setupTasks.forEach( function( task ){ task() })


			//  Set up THREE.js and Trackball Controls:
			//  Click and drag the scene to orbit around the origin.

			setupThree()
			setupControls()


			//  Visualization presets are supplied by the URL hash property.
			//  Have we been asked to use a visual preset?

			var hash = document.location.search.substr( 1 )

			if( hash.charAt( hash.length - 1 ) === '/' ) hash = hash.substr( 0, hash.length - 1 )
			hash = hash.charAt( 0 ).toUpperCase() + hash.substr( 1, hash.length )

			//  Create a Rubik's Cube. Just one. 
			//  Though we're entirely capable of spawning several!
			//  (Update: that's not entirely true...)

			window.cube = new Cube( hash )


			//  Let's enable our Cube Control keyboard commands.

			updateControls()

			//  Ok, we're done with the setup tasks
			//  so let's change our state to loop.

			erno.changeStateTo( 'loop' )
		},
		loop: function(){

			animate()
		}
	},


	//  Here's a quick way to see how much overheard Erno is using
	//  right from the JavaScript command line.

	inspect: function(){

		var 
		memAvailableMB = window.performance.memory.totalJSHeapSize
			.divide( 1024 * 1024 )
			.multiply( 10 ).roundDown().divide( 10 ),
		memUsedMB = window.performance.memory.usedJSHeapSize
			.divide( 1024 * 1024 )
			.multiply( 10 ).roundDown().divide( 10 ),
		memUsedPercent = window.performance.memory.usedJSHeapSize
			.divide( window.performance.memory.totalJSHeapSize )
			.multiply( 1000 ).roundDown().divide( 10 )		
		
		console.log( '' )
		console.log(  now().toDate() )
		console.log( 'JS heap size total  ', memAvailableMB +' MB  (100.0%)' )
		console.log( 'JS heap size used   ', memUsedMB +' MB  ('+ memUsedPercent +'%)' )
		console.log( 'cube.twistQueue     ', ( cube.twistQueue.history.length + cube.twistQueue.future.length ))
		console.log( 'cube.taskQueue      ', ( cube.taskQueue.history.length + cube.taskQueue.future.length ))
		console.log( 'THREE.Object3D index', THREE.Object3DIdCount )
		console.log( '' )

		return memUsedPercent
	}
}








    ///////////////
   //           //
  //   Three   //
 //           //
///////////////


function setupThree(){


	//  First let's create a Scene object.

	window.scene = new THREE.Scene()


	//  And now a Camera to look at that scene.
	
	var
	FIELD_OF_VIEW = 45,
	WIDTH         = document.getElementById('outer-container').offsetWidth,
	HEIGHT        = document.getElementById('outer-container').offsetHeight,
	ASPECT_RATIO  = WIDTH / HEIGHT,
	NEAR          = 1,
	FAR           = 6000

	window.camera = new THREE.PerspectiveCamera( FIELD_OF_VIEW, ASPECT_RATIO, NEAR, FAR )
	camera.position.z = 1500
	camera.tanFOV = Math.tan((( Math.PI / 180 ) * camera.fov / 2 ))//  For maintaining scale on windowResize.
	camera.oneToOne = function(){
		
		//  Return the Z position at which to place an object for exactly 100% scale.
		//  https://github.com/mrdoob/three.js/blob/dev/examples/js/renderers/CSS3DRenderer.js#L142

		return - 0.5 / Math.tan( this.fov * Math.PI / 360 ) * HEIGHT
	}
	camera.lookAt( scene.position )
	scene.add( camera )

	window.raycaster = new THREE.Raycaster()

	//  We need a projector to map 2D clicks and touches
	//  to 3D points in space!

	window.projector = new THREE.Projector()


	//  Renderer!

	if( erno.renderMode === 'css' ){

		window.renderer = new THREE.CSS3DRenderer()
		renderer.domElement.style.position = 'absolute'
		renderer.domElement.style.top = 0
	}
	else if( erno.renderMode === 'svg' ){

		window.renderer = new THREE.SVGRenderer()
		renderer.setQuality( 'low' )
	}
	else if( erno.renderMode === 'webgl' ){

		window.renderer = new THREE.WebGLRenderer({ antialias: true })
		renderer.shadowMapEnabled = true
	}
	renderer.setSize( WIDTH, HEIGHT )
	renderer.originalHeight = HEIGHT
	document.getElementById( 'cube-container' ).appendChild( renderer.domElement )


	//  Readjust on window resize.

	$(document).resize(onWindowResize)
}
function setupControls(){


	//  Mouse trackball controls.

	window.controls = new THREE.TrackballControls( camera, renderer.domElement )
	controls.noZoom = controls.noPan = true;
	//window.controls = new THREE.TrackballControls( window.cube.threeObject, document.body )
	controls.rotateSpeed = 0.5
	controls.autoRotateTheta=135;
	controls.beginAutoRotate();
	controls.mouseUpCallback = function () {
		controls.stopAutoRotate();
		controls.mouseUpCallback = false;
	}
	//controls.addEventListener( 'change', render )

	//  Change Field of View

	/*$( document ).keydown( function( event ){

		if( event.keyCode === 38 ) camera.fov ++
		if( event.keyCode === 40 ) camera.fov --
		//camera.updateProjectionMatrix()
	})*/
}
function onWindowResize(){
	
	let
	WIDTH         = document.getElementById('outer-container').offsetWidth,
	HEIGHT        = document.getElementById('outer-container').offsetHeight

	camera.aspect = WIDTH / HEIGHT
	camera.fov = ( 360 / Math.PI ) * Math.atan( camera.tanFOV * ( HEIGHT / renderer.originalHeight ))    
	camera.updateProjectionMatrix()
	renderer.setSize( WIDTH, HEIGHT )
	render()
}
function animate(){
	//console.log("Animate loop");
	TWEEN.update()
	if( window.controls && window.controls instanceof THREE.TrackballControls ){

		let 
		cameraPositionX = camera.position.x,
		cameraPositionY = camera.position.y,
		cameraPositionZ = camera.position.z,

		cameraRotationX = camera.rotation.x,
		cameraRotationY = camera.rotation.y,
		cameraRotationZ = camera.rotation.z

		controls.update()

		if( cameraPositionX !== camera.position.x ||
			cameraPositionY !== camera.position.y || 
			cameraPositionZ !== camera.position.z ||
			
			cameraRotationX !== camera.rotation.x ||
			cameraRotationY !== camera.rotation.y || 
			cameraRotationZ !== camera.rotation.z ){

			updateControls()	
		}		
	}
	render()
	//requestAnimationFrame( animate )
}
function render(){
	
	renderer.render( scene, camera )
}








    //////////////////
   //              //
  //   Controls   //
 //              //
//////////////////


function updateControls( cube ){

	if( cube === undefined ) cube = window.cube
	$( '#backgroundColorCss' ).val( $( 'body' ).css( 'background-color' ))	
	$( '#cameraFov' ).val( camera.fov )
}
function assessTrueFalseMixed( id, count ){

	if( count === 0 ){

		$( id ).prop( 'indeterminate', false )
		$( id ).prop( 'checked', false )
	}
	else if( count === 27 ){

		$( id ).prop( 'indeterminate', false )
		$( id ).prop( 'checked', true )
	}
	else $( id ).prop( 'indeterminate', true )
}








    /////////////////
   //             //
  //   Loopage   //
 //             //
/////////////////


//  Here's the hardcore, low-level loop that's going to run EVERYTHING.
//  See how it delegates to window.racer.states[]?
//  No $( document ).ready() and no requestAnimationFrame() shim.

function loop(){
	
	var state = erno.states[ erno.state ]
	if( document.readyState === 'complete' ){

		erno.stateFrames ++
		if( state instanceof Function ) state()
	}
	requestAnimationFrame(loop)
}



