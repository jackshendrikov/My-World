function decrypt() {
    $("#Encrypt").attr('checked', false);
    $("#Decrypt").attr('checked', true);

    $("#cipherEncrypt").hide();
    $("#cipherDecrypt").show();
}

function encrypt() {
    $("#Decrypt").attr('checked', false);
    $("#Encrypt").attr('checked', true);

    $("#cipherDecrypt").hide();
    if (!!document.getElementById("cipherTable")) {
        $("#cipherTable").hide();
    }
    $("#cipherEncrypt").show();
}

$("#Encrypt").click(function() {
   encrypt();
});

$("#Decrypt").click(function() {
    decrypt();
});