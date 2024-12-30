const seeAnotherField_new=document.getElementById("seeAnotherField_new")
const doc_type_id=document.getElementById("doc_type_id")
window.onload = (e) => {
    seeAnotherField_new.style.display="none";
    doc_type_id.style.display="none";
}
billing_g.addEventListener('change', (e) => {
    console.log(e.target.value)
    if (e.target.value != '1'){
        seeAnotherField_new.style.display = "block";
    }
  })
seeAnotherField.addEventListener('change', (e) => {
    console.log(e.target.value)
    if (e.target.value != 'none'){
        doc_type_id.style.display = "block";
    }
  })
