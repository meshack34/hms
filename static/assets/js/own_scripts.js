const pay_m_visit_id = document.getElementById("pay_m_visit_id")
const pay_m_uhid = document.getElementById("pay_m_uhid")
const pay_m_bill_no = document.getElementById("pay_m_bill_no")
const mode_type = document.getElementById("mode_type")
const amount = document.getElementById("amount")
const bank = document.getElementById("bank")
const card_no = document.getElementById("card_no")
const utr_id = document.getElementById("utr_id")
const doc_type_id=document.getElementById("doc_type_id")

window.onload = (e) => {
    pay_m_visit_id.style.display = "none";
    pay_m_uhid.style.display = "none";
    pay_m_bill_no.style.display = "none";
//    mode_type.style.display = "none";
    amount.style.display = "none";
    bank.style.display = "none";
    card_no.style.display = "none";
    utr_id.style.display = "none";
    doc_type_id.style.display="none";
}
mode_type.addEventListener('change', (e) => {
    console.log(e.target.value)
    if (e.target.value == 'cash'){
        mode_type.style.display = "block";
        amount.style.display = "block";
        pay_m_visit_id.style.display = "none";
        pay_m_uhid.style.display = "none";
        pay_m_bill_no.style.display = "none";
        bank.style.display = "none";
        card_no.style.display = "none";
        utr_id.style.display = "none";
    }
    else if (e.target.value == 'debit_credit_card'){
        mode_type.style.display = "block";
        amount.style.display = "block";
        pay_m_visit_id.style.display = "none";
        pay_m_uhid.style.display = "none";
        pay_m_bill_no.style.display = "none";
        bank.style.display = "block";
        card_no.style.display = "block";
        utr_id.style.display = "none";

    }
    else if (e.target.value == 'wallet'){
        mode_type.style.display = "block";
        amount.style.display = "block";
        pay_m_visit_id.style.display = "none";
        pay_m_uhid.style.display = "none";
        pay_m_bill_no.style.display = "none";
        bank.style.display = "none";
        card_no.style.display = "none";
        utr_id.style.display = "block";

    }
    else if (e.target.value == 'upi'){
        mode_type.style.display = "block";
        amount.style.display = "block";
        pay_m_visit_id.style.display = "none";
        pay_m_uhid.style.display = "none";
        pay_m_bill_no.style.display = "none";
        bank.style.display = "none";
        card_no.style.display = "none";
        utr_id.style.display = "block";
    }
})