/* checking the correctness of the IP address*/
function ValidateIPAddress(ip) {
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip))
      return true;

    alert("You have entered an invalid IP address!");
    $("#ip_address").val("");
    return false;
}

$('document').ready(function(){
    /* If ip input is change, than it automatically calls for validation */
    $('#ip_address').change(function(){
        ValidateIPAddress($("#ip_address").val());
    })
})