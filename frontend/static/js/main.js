M.AutoInit();

$(function() {
    $('#copyButton').click(function () {
        var text = $('#short-url').text();
        copyToClipboard(text);
    });
});

function copyToClipboard(text) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
    M.toast({html: 'Copied: ' + text, classes: 'rounded'});
}

function showModal(text) {
    $('#modal-id .modal-content p').text("");
    var elems = document.querySelectorAll('#modal-id');
    var instances = M.Modal.init(elems);
    $('#modal-id .modal-content p').text(text);
    instances[0].open();
}

$(function() {
    $('#submitButton').click(function() {
         $.ajax({
             type: "POST",
             url: "/create",
             data: JSON.stringify({'url' : $('#url').val()}),
             success: returnSuccess,
             dataType: 'json',
             contentType: "application/json",
             error: function(response) {
                var msg = JSON.parse(response.responseText).detail[0].msg;
                showModal(msg);
             }
         });
    });
});

function returnSuccess(data, textStatus, jqXHR) {
    $('#url').val("");

    $('#short-url').text(data.short_url);
    $('#short-url').attr("href", data.short_url);
    $('#short-url').removeClass("hide");

    $('#copyButton').removeClass("hide");

    $('#openButton').attr("href", data.short_url);
    $('#openButton').removeClass("hide");
}