var map;
var latlong;
var marker;
$(function() {
	initMap();
	getMapLatLong();
    validationLot();
    // enterLatLng();
    // submitForm();
    	// Phase 1
	new google.maps.Marker({
		position: { lat: 14.36411592420933, lng: 120.908960894963 },
		map: map,
		icon: "none",
		label: {
			color: 'Black',
			fontWeight: 'bold',
			text: 'Phase 1',
			fontSize: '20px',
		},
	});
	// Phase 2
	new google.maps.Marker({
		position: { lat: 14.36418574973309, lng: 120.90978790446964 },
		map: map,
		icon: "none",
		label: {
			color: 'Black',
			fontWeight: 'bold',
			text: 'Phase 2',
			fontSize: '20px',
		},
	});
	// Phase 3
	new google.maps.Marker({
		position: { lat: 14.364714952994268, lng: 120.90885846718007 },
		map: map,
		icon: "none",
		label: {
			color: 'Black',
			fontWeight: 'bold',
			text: 'Phase 3',
			fontSize: '20px',
		},
	});
	// Phase 4
	new google.maps.Marker({
		position: { lat: 14.364714952994268, lng: 120.90971582565943 },
		map: map,
		icon: "none",
		label: {
			color: 'Black',
			fontWeight: 'bold',
			text: 'Phase 4',
			fontSize: '20px',
		},
	});
});
function initMap(){
	map = new google.maps.Map(document.getElementById("mapAdmin"), {
		center: { lat: 14.3642225, lng: 120.9093891 },
		zoom: 18.5,
		zoomControl: true,
		// gestureHandling: "none",
		mapTypeId: "terrain",
        draggableCursor:"default"
      
	});
	
}
  function setMarker(latitude,longitude){
    if(marker != null || marker != undefined){
        marker.setMap(null);
        marker = new google.maps.Marker({
            animation: google.maps.Animation.DROP,
            map: map,
            position: new google.maps.LatLng(latitude,longitude)
        });
        marker.setMap(map);
    }else{
        marker = new google.maps.Marker({
            animation: google.maps.Animation.DROP,
            map: map,
            position: new google.maps.LatLng(latitude,longitude)
        });
        marker.setMap(map);
    }
  }
  var lat;
  var long;
  function getMapLatLong(){
    $('input#lat').attr("readonly", true); 
	$('input#lng').attr("readonly", true); 
	google.maps.event.addListener(map, 'click', function(event) {
		if(marker != null || marker != undefined){
			marker.setMap(null);
			marker = new google.maps.Marker({
				animation: google.maps.Animation.DROP,
				map: map,
				position: event.latLng
			});
			marker.setMap(map);
			lat = event.latLng.lat();
			long = event.latLng.lng();
		}else{
			marker = new google.maps.Marker({
				animation: google.maps.Animation.DROP,
				map: map,
				position: event.latLng
			});
			marker.setMap(map);
			lat = event.latLng.lat();
			long = event.latLng.lng();
		}
		$('input#lat').val(lat);
		$('input#lng').val(long);
	});
}
function getLatLongBoolean(){
    var lat = $('input#lat').val().length;
    var lng = $('input#lng').val().length;
    if(lat != 0 && lng != 0){
        return true;
    }else{
        return false
    }
}

// function enterLatLng(){
//     $('input#lat').keypress(function(e){
//         if(getLatLongBoolean()){
//             setTimeout(() => {
//                 setMarker($('input#lat').val(),$('input#lng').val());
//             }, "2000")
//         }
//     });
//     $('input#lng').keypress(function(e){
//         if(e.keyCode == 13)
//         {
//             if(getLatLongBoolean()){
//                 setTimeout(() => {
//                     setMarker($('input#lat').val(),$('input#lng').val());
//                 }, "2000")
//             }
//         }
//     });
    
// }
function submitForm(){
   
    var phase = $('#id_phase').val();
    var block = $('#id_block').val();
    var lot = $('#id_lotno').val();
    var lat = $('#lat').val();
    var lng = $('#lng').val();
    var name = $('#id_deceased').val();
    var born = $('#id_born').val();
    var died = $('#id_died').val();
    console.log(lotLawn);
    if ($("#id_lot_0 input[name='lot']:checked").length == 0 || $("#id_lot_1 input[name='lot']:checked").length == 0 || $("#id_lot_2 input[name='lot']:checked").length == 0 || $("#id_lot_3 input[name='lot']:checked").length == 0){
        alert("Lot type is not yet selected");
    }else if((phase.length == 0) || (phase == '') || (phase == null) || (phase == undefined)){
        alert("Phase field is empty");
    }else if((block.length == 0) || (block == '') || (block == null) || (block == undefined)){
        alert("block field is empty");
    }else if((lot.length == 0) || (lot == '') || (lot == null) || (lot == undefined)){
        alert("lot field is empty");
    }else if(((lat.length == 0)) && ((lng.length == 0))){
        console.log("Here lat long")
        alert("Please select the coordinate to fill up the Latitude and Longitude");
    }else if((name.length == 0) || (name == '') || (name == null) || (name == undefined)){
        alert("Name field is empty");
    }else if((born.length == 0) || (born == '') || (born == null) || (born == undefined)){
        alert("Date of born field is empty");
    }else if((died.length == 0) || (died == '') || (died == null) || (died == undefined)){
        alert("Date of died field is empty");
    }else{
        if(confirm("Successfully added user ")) document.location = 'AdminHomepage/2';
    }

   

// $('#form').submit(function(){
   
   

//     // $.ajax({
//     //          type: "POST",
//     //          url: "{% url AddNew %}",
//     //          data: {'username': $('#username').val(), 'csrfmiddlewaretoken': '{{csrf_token}}'},
//     //          dataType: "text",
//     //          success: function(response) {
//     //                 var response = $.parseJSON( response );
//     //                 if (response.success){
//     //                     return true;
//     //                 }
//     //                 else{
//     //                     alert(response.error);
//     //                 }
//     //           },
//     //           error: function(rs, e) {
//     //                  alert(rs.responseText);
//     //           }
//     //     }); 
//   })

}
function validationLot(){

let lot =  $('#id_lotno')
lot.removeAttr('maxlength');
lot.removeAttr('required');
$('#id_lot_3').on('change',function(){
    let regex = /^\d{3}[a-zA-Z]$/;
    if($("#id_lot_3 input[name='lot']:checked")){
        console.log("true")
        $('#id_lotno').keyup(function() {
            let value = $(this).val();
            let isValid =regex.test(value);
            if($(this).val().length >= 4){
                if(!isValid){
                    $(this).val("");
                }
            }
    
    });
    } 
});



}
 

