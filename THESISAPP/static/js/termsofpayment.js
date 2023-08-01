var selectedVal = null;
var getLotAddress = null;
var getBalance = null;
var amountPayment = 0;
var amountToBePaid = 0;
var originalAmountToBePaid = $('#id_balance').val();
$(function() {
    // uncomment this function to enable the auto deduct.
    // autoDeductFinalAmount();
    selectedVal = $("#id_terms option:selected").val();
    getLotAddress = $("#id_product option:selected").text();
    if(selectedVal == "" || selectedVal == null || selectedVal == undefined){
        getSelectedTermsOfPayment();
    }else{
        getTermsOfPayment();
    }
});

function getTermsOfPayment(){
    selectedVal = $("#id_terms option:selected").val();
    getLotAddress = $("#id_product option:selected").text();
    getBalance = $("#id_balance").val();
    if(getLotAddress.includes('Lawn Lot')){
        setFieldsTermsOfPayment(getBalance,selectedVal);
        $("#id_pay").val(0);
    }else if(getLotAddress.includes('Apartment')){
        setFieldsTermsOfPayment(getBalance,selectedVal);
        $("#id_pay").val(0);
    }else if(getLotAddress.includes('Niche')){
        setFieldsTermsOfPayment(getBalance,selectedVal);
        $("#id_pay").val(0);
    }else if(getLotAddress.includes('Mausoleum')){
        setFieldsTermsOfPayment(getBalance,selectedVal);
        $("#id_pay").val(0);
    }else{

    }
}

function setFieldsTermsOfPayment(amountToBePaid,paymentTerm){
    if(paymentTerm == "Cash"){
        $("#id_balance").val(amountToBePaid);
        originalAmountToBePaid = amountToBePaid;
        var today = new Date();
        // Format the date as a string in the desired format (YYYY-MM-DD)
        var dateString = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') +'-'+ today.getDate().toString().padStart(2, '0');
        $("#id_due_date").val(dateString);
    }else if (paymentTerm == "1 Year"){
        $("#id_balance").val(amountToBePaid);
        originalAmountToBePaid = amountToBePaid;
        var today = new Date();
        // Add one year to the current date
        today.setFullYear(today.getFullYear() + 1);
        // Format the date as a string in the desired format (YYYY-MM-DD)
        var dateString = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') +'-'+ today.getDate().toString().padStart(2, '0');
        $("#id_due_date").val(dateString);
    }else if (paymentTerm == "2 Years"){
        $("#id_balance").val(amountToBePaid);
        originalAmountToBePaid = amountToBePaid;
        var today = new Date();
        // Add one year to the current date
        today.setFullYear(today.getFullYear() + 2);
        // Format the date as a string in the desired format (YYYY-MM-DD)
        var dateString = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') +'-'+ today.getDate().toString().padStart(2, '0');
        $("#id_due_date").val(dateString);
    }else if (paymentTerm == "3 Years"){
        $("#id_balance").val(amountToBePaid);
        originalAmountToBePaid = amountToBePaid;
        var today = new Date();
        // Add one year to the current date
        today.setFullYear(today.getFullYear() + 3);
        // Format the date as a string in the desired format (YYYY-MM-DD)
        var dateString = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') +'-'+ today.getDate().toString().padStart(2, '0');
        $("#id_due_date").val(dateString);
    }else if (paymentTerm == "Full Down"){
        $("#id_balance").val(amountToBePaid);
        originalAmountToBePaid = amountToBePaid;
        var today = new Date();
        // Add one month to the current date
        today.setMonth(today.getMonth() + 1);
        // Format the date as a string in the desired format (YYYY-MM-DD)
        var dateString = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') + '-' + today.getDate().toString().padStart(2, '0');
        $("#id_due_date").val(dateString);
    }else if (paymentTerm == "Reservation"){
        $("#id_balance").val(amountToBePaid);
        originalAmountToBePaid = amountToBePaid;
        var today = new Date();
        // Add one month to the current date
        today.setMonth(today.getMonth() + 1);
        // Format the date as a string in the desired format (YYYY-MM-DD)
        var dateString = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') + '-' + today.getDate().toString().padStart(2, '0');
        $("#id_due_date").val(dateString);
    }
}
function getSelectedTermsOfPayment(){
    var amount = 0;
    $("#id_terms").change(function() {
        if(selectedVal == "" || selectedVal == null || selectedVal == undefined){
            selectedVal = $("#id_terms option:selected").val();
            getLotAddress = $("#id_product option:selected").text();
            console.log(selectedVal);
            if(getLotAddress.includes('Lawn Lot')){
                amount = computeTotalAmount('Lawn Lot',selectedVal,3000,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else if(getLotAddress.includes('Apartment')){
                amount = computeTotalAmount('Apartment',selectedVal,1200,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else if(getLotAddress.includes('Niche')){
                amount = computeTotalAmount('Niche',selectedVal,5000,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else if(getLotAddress.includes('Mausoleum')){
                amount = computeTotalAmount('Mausoleum',selectedVal,30000,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else{

            }
        }else{
            selectedVal = $("#id_terms option:selected").val();
            getLotAddress = $("#id_product option:selected").text();
            if(getLotAddress.includes('Lawn Lot')){
                amount = computeTotalAmount('Lawn Lot',selectedVal,3000,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else if(getLotAddress.includes('Apartment')){
                amount = computeTotalAmount('Apartment',selectedVal,1200,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else if(getLotAddress.includes('Niche')){
                amount = computeTotalAmount('Niche',selectedVal,5000,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else if(getLotAddress.includes('Mausoleum')){
                amount = computeTotalAmount('Mausoleum',selectedVal,30000,amountPayment);
                setFieldsTermsOfPayment(amount,selectedVal);
            }else{

            }
        }
      
	});
} 
// Here is the auto deduct on amount paid and amount to be paid.
function autoDeductFinalAmount(){
  $('#id_pay').keyup(function(event) {
    var amountPaid = $(this).val();
    if (event.keyCode === 8 && amountPaid === '' || amountPaid === '.') {
      // Handle backspace key
      $('#id_balance').val(originalAmountToBePaid);
      return;
    }

    if (amountPaid === '' || amountPaid === '.') {
      return;
    }

    var amountToBePaid = parseFloat($('#id_balance').val());
    $('#id_balance').val((amountToBePaid - parseFloat(amountPaid)).toFixed(2));
  });

  $('#id_pay').on('input', function() {
    var regex = /^[0-9.]+$/;
    var amountPaid = $(this).val();
    if (!regex.test(amountPaid)) {
      $(this).val('');
      $('#id_balance').val(originalAmountToBePaid);
    }
  });
}
function computeTotalAmount(lotType, paymentTerm, outrightDP, amountPayment) {
    var amount;
    if (lotType == "Apartment") {
      if (paymentTerm == "Cash") {
        amount = 10800.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "1 Year") {
        amount = outrightDP + (974.81 * 12);
        return amount.toFixed(2);
      } else if (paymentTerm == "2 Years") {
        amount = outrightDP + (523.69 * 24);
        return amount.toFixed(2);
      } else if (paymentTerm == "3 Years") {
        amount = outrightDP + (390.53 * 36);
        return amount.toFixed(2);
      } else if (paymentTerm == "Full Down"){
        amount = 10800.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "Reservation"){
        amount = 250.00;
        return amount.toFixed(2);
      }else {

      }
    } else if (lotType == "Niche") {
      if (paymentTerm == "Cash") {
        amount = 45000.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "1 Year") {
        amount = outrightDP + (4061.70 * 12);
        return amount.toFixed(2);
      } else if (paymentTerm == "2 Years") {
        amount = outrightDP + (2182.05 * 24);
        return amount.toFixed(2);
      } else if (paymentTerm == "3 Years") {
        amount = outrightDP + (1627.20 * 36);
        return amount.toFixed(2);
      } else if (paymentTerm == "Full Down"){
        amount = 50000.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "Reservation"){
        amount = 1000.00;
        return amount.toFixed(2);
      }else{

      }
    } else if (lotType == "Lawn Lot") {
      if (paymentTerm == "Cash") {
        amount = 27000.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "1 Year") {
        amount = outrightDP + (2437.02 * 12);
        return amount.toFixed(2);
      } else if (paymentTerm == "2 Years") {
        amount = outrightDP + (1309.23 * 24);
        return amount.toFixed(2);
      } else if (paymentTerm == "3 Years") {
        amount = outrightDP + (976.32 * 36);
        return amount.toFixed(2);
      } else if (paymentTerm == "Full Down"){
        amount = 30000.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "Reservation"){
        amount = 600.00;
        return amount.toFixed(2);
      }else{

      }
    } else if (lotType == "Mausoleum") {
      if (paymentTerm == "Cash") {
        amount = 270000.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "1 Year") {
        amount = outrightDP + (24370.20 * 12);
        return amount.toFixed(2);
      } else if (paymentTerm == "2 Years") {
        amount = outrightDP + (13092.30 * 24);
        return amount.toFixed(2);
      } else if (paymentTerm == "3 Years") {
        amount = outrightDP + (9763.20 * 36);
        return amount.toFixed(2);
      } else if (paymentTerm == "Full Down"){
        amount = 300000.00;
        return amount.toFixed(2);
      } else if (paymentTerm == "Reservation"){
        amount = 6250.00;
        return amount.toFixed(2);
      }else{

      }
    } else {
      return "Invalid lot type";
    }
  }