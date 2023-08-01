var stringValue = "";
$(function() {
	dates();
    validateLot();
    appartmentLot();
    // enterLatLng();
    // submitForm();
});

function dates(){
    var currentDate = new Date();
    var previousDate = new Date();

    // Set the maximum date of the date input field to the current date
    // payment page for deceased date
    $('#id_born').attr('max', currentDate.toISOString().substring(0, 10));
    $('#id_died').attr('max', currentDate.toISOString().substring(0, 10));
    $('#date').attr('min', previousDate.toISOString().substring(10, 0));
    // Signup
    $('#id_birth').attr('max', currentDate.toISOString().substring(0, 10));
    
    // for client page date
    $('#id_paid_date').attr('max', currentDate.toISOString().substring(0, 10));
    // $('#id_due_date').attr('max', currentDate.toISOString().substring(0, 10));
    $('#id_duedate').attr('max', currentDate.toISOString().substring(0, 10));
    $('#id_date').attr('max', currentDate.toISOString().substring(0, 10));
    $('#birth').attr('max', currentDate.toISOString().substring(0, 10));
    $('#birdth').attr('max', currentDate.toISOString().substring(0, 10));


}

function validateLot(){
let stringValue;
// let lot =  $('#id_product_lotno');
// lot.removeAttr('maxlength');
// lot.removeAttr('required');
$('#id_product_lottype').on('change', function() {
   stringValue = $(this).find(":selected").val();
   if(stringValue == "Apartment"){
    let regex = /^\d{3}[a-zA-Z]$/;
    $('#id_product_lotno').keyup(function() {
      let value = $(this).val();
      let isValid =regex.test(value);
      if($(this).val().length >= 4){
          if(!isValid){
              $(this).val("")
          }
      }
    });
    
    }  else{
        let regex = /^\d{3}[a-zA-Z]$/;
        $('#id_product_lotno').keyup(function() {
            
            let value = $(this).val();
            let isValid =regex.test(value);
            if($(this).val().length >= 4){
                if(!isValid){
                }
            }
          });
    }   
});

$('#id_lot_lottype').on('change', function() {
    stringValue = $(this).find(":selected").val();
    if(stringValue == "Apartment"){
     let regex = /^\d{3}[a-zA-Z]$/;
     $('#id_lot_lotno').keyup(function() {
       let value = $(this).val();
       let isValid =regex.test(value);
       if($(this).val().length >= 4){
           if(!isValid){
               $(this).val("")
           }
       }
     });
     
     }  else{
         let regex = /^\d{3}[a-zA-Z]$/;
         $('#id_lot_lotno').keyup(function() {
             
             let value = $(this).val();
             let isValid =regex.test(value);
             if($(this).val().length >= 4){
                 if(!isValid){
                 }
             }
           });
     }   
 });

$('#validationFormCheck3').on('change',function(){
    let regex = /^\d{3}[a-zA-Z]$/;
    if($("#validationFormCheck3 input[name='lot_type']:checked")){
        console.log("true");
        $('#lot_no').keyup(function() {
            let value = $(this).val();
            let isValid =regex.test(value);
            if($(this).val().length >= 4){
                if(!isValid){
                    $(this).val("")
                }
            }
    
    });
    } 
});

}
function appartmentLot(){
    let regex = /^\d{3}[a-zA-Z]$/;
    $('#id_apartment_lot').keyup(function() {
      let value = $(this).val();
      let isValid =regex.test(value);
      if($(this).val().length >= 4){
          if(!isValid){
              $(this).val("")
          }
      }
    });
}