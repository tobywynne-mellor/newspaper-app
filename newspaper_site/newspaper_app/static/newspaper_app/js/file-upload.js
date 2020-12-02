// this bad boy creates badge with filename and button to cancel upload
$(".upload").on("change", function() {
    if ($(".upload").val() != '') {
        var fileName = $(this).val().split("\\").pop();
        $(".upload-status").html(fileName);
        $(".cancel-upload").remove();
        $(".upload-status").after('<span class="btn btn-sm cancel-upload"><i class="fas fa-times"></i></span>')
    }
    if ($(".upload").val() == '') {
        $(".upload-status").html('');
        $(".cancel-upload").remove();
    }
});

// canceling upload via button or browser cancel button from file input removes badge and cancel button
$(document).on('click', '.cancel-upload, .btn-dismiss, .btn-profile-put', function() {
    $(".upload").val('');
    $(".upload-status").html('');
    $(".cancel-upload").remove();
}
);