const payAmount = document.querySelector(".price").innerHTML;
const serviceCharge = document.querySelector(".service-charge").innerHTML;

// console.log(payAmount);


const getGrandTotal  = (price, charge) =>{
    const cleanedPrice = price.replace(/[^0-9.-]+/g, '');
    const cleanedCharge = charge.replace(/[^0-9.-]+/g, '');

    const addOnPrice = Number(cleanedPrice);
    const addOnCharge = Number(cleanedCharge);

    return addOnCharge + addOnPrice;
}
const totalBookingPrice = (getGrandTotal(payAmount,serviceCharge));
document.querySelector(".result").innerHTML = totalBookingPrice;

