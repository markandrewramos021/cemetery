var memorialType = null;
var typeofTerms= null;
$(function(){
    getMemorialAndTermsType();
});

function getMemorialAndTermsType(){
    $('input[type=radio][name=lot_type]').change(function() {
        memorialType = this.value;
        calculateTotalAmountMemorial();
    });
    $('input[type=radio][name=terms]').change(function() {
        typeofTerms = this.value;
        calculateTotalAmountTerms();
    });
}
// if(memorialType === "Lawn Lot"){
        
// }else if(memorialType === "Mausoleum"){

// }else if(memorialType === "Niche"){

// }else if(memorialType === "Apartment Type"){

// }else {
//      $("#amount").val("");
// }
function calculateTotalAmountTerms(){
    if(typeofTerms === "Cash"){
        if(memorialType === "Lawn Lot"){
            $("#amount").val("27,000.00");
        }else if(memorialType === "Mausoleum"){
            $("#amount").val("270,000.00");
        }else if(memorialType === "Niche"){
            $("#amount").val("45,000.00");
        }else if(memorialType === "Apartment Type"){
            $("#amount").val("10,800.00");
        }else {
            $("#amount").val("");
        }
    }else if(typeofTerms === "1 Year"){
        if(memorialType === "Lawn Lot"){
            $("#amount").val("32,244.24");
        }else if(memorialType === "Mausoleum"){
            $("#amount").val("322,442.40");
        }else if(memorialType === "Niche"){
            $("#amount").val("53,740.40");
        }else if(memorialType === "Apartment Type"){
            $("#amount").val("53,740.40");
        }else {
            $("#amount").val("");
        }
    }else if(typeofTerms === "2 Years"){
        if(memorialType === "Lawn Lot"){
            $("#amount").val("34,421.52");
        }else if(memorialType === "Mausoleum"){
            $("#amount").val("344,215.20");
        }else if(memorialType === "Niche"){
            $("#amount").val("57,380.00");
        }else if(memorialType === "Apartment Type"){
            $("#amount").val("13,768.56");
        }else {
             $("#amount").val("");
        }
    }else if(typeofTerms === "3 Years"){
        if(memorialType === "Lawn Lot"){
            $("#amount").val("38,147.52");
        }else if(memorialType === "Mausoleum"){
            $("#amount").val("381,475.20");
        }else if(memorialType === "Niche"){
            $("#amount").val("63,579.20");
        }else if(memorialType === "Apartment Type"){
            $("#amount").val("15,259.08");
        }else {
             $("#amount").val("");
        }
    }else if(typeofTerms === "Full Down"){
        if(memorialType === "Lawn Lot"){
            $("#amount").val("30,000.00");
        }else if(memorialType === "Mausoleum"){
            $("#amount").val("300,000.00");
        }else if(memorialType === "Niche"){
            $("#amount").val("50,000.00");
        }else if(memorialType === "Apartment Type"){
            $("#amount").val("12,000.00");
        }else {
             $("#amount").val("");
        }
    }else if(typeofTerms === "Reservation"){
        if(memorialType === "Lawn Lot"){
            $("#amount").val("600.00");
        }else if(memorialType === "Mausoleum"){
            $("#amount").val("6,250.00");
        }else if(memorialType === "Niche"){
            $("#amount").val("1,000.00");
        }else if(memorialType === "Apartment Type"){
            $("#amount").val("250.00");
        }else {
             $("#amount").val("");
        }
    }else {
        $("#amount").val("");
    }
}
function calculateTotalAmountMemorial(){
    if(memorialType === "Lawn Lot"){
        if(typeofTerms === "Cash"){
            $("#amount").val("27,000.00");
        }else if(typeofTerms === "1 Year"){
            $("#amount").val("32,244.24");
        }else if(typeofTerms === "2 Years"){
            $("#amount").val("34,421.52");
        }else if(typeofTerms === "3 Years"){
            $("#amount").val("38,147.52");
        }else if(typeofTerms === "Full Down"){
            $("#amount").val("30,000.00");
        }else if(typeofTerms === "Reservation"){
            $("#amount").val("600.00");
        }else {
            $("#amount").val("");
        }
    }else if(memorialType === "Mausoleum"){
        if(typeofTerms === "Cash"){
            $("#amount").val("270,000.00");
        }else if(typeofTerms === "1 Year"){
            $("#amount").val("322,442.40");
        }else if(typeofTerms === "2 Years"){
            $("#amount").val("344,215.20");
        }else if(typeofTerms === "3 Years"){
            $("#amount").val("381,475.20");
        }else if(typeofTerms === "Full Down"){
            $("#amount").val("300,000.00");
        }else if(typeofTerms === "Reservation"){
            $("#amount").val("6,250.00");
        }else {
            $("#amount").val("");
        }
    }else if(memorialType === "Niche"){
        if(typeofTerms === "Cash"){
            $("#amount").val("45,000.00");
        }else if(typeofTerms === "1 Year"){
            $("#amount").val("53,740.40");
        }else if(typeofTerms === "2 Years"){
            $("#amount").val("57,380.00");
        }else if(typeofTerms === "3 Years"){
            $("#amount").val("63,579.20");
        }else if(typeofTerms === "Full Down"){
            $("#amount").val("50,000.00");
        }else if(typeofTerms === "Reservation"){
            $("#amount").val("1,000.00");
        }else {
            $("#amount").val("");
        }
    }else if(memorialType === "Apartment Type"){
        if(typeofTerms === "Cash"){
            $("#amount").val("10,800.00");
        }else if(typeofTerms === "1 Year"){
            $("#amount").val("53,740.40");
        }else if(typeofTerms === "2 Years"){
            $("#amount").val("13,768.56");
        }else if(typeofTerms === "3 Years"){
            $("#amount").val("15,259.08");
        }else if(typeofTerms === "Full Down"){
            $("#amount").val("12,000.00");
        }else if(typeofTerms === "Reservation"){
            $("#amount").val("250.00");
        }else {
            $("#amount").val("");
        }
    }else {
        $("#amount").val("");
    }
}

