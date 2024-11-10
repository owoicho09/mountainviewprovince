$('#room-selection-form').on('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    let selectedRoomCategory = $("input[name='selected_room_category']:checked").val();
    let rate_type = $("input[name='hostel_rate']:checked").val();
    let rate_price = $("input[name='hostel_rate']:checked").data("price");
    let csrfToken = $("input[name='csrfmiddlewaretoken']").val();

    // Validate selection
    if (!selectedRoomCategory) {
        Swal.fire({
            icon: "warning",
            title: "Selection Missing",
            text: "Please select a room category",
            timer: 2000,
            showConfirmButton: false
        });
        return;
    }

    // Show loading indicator
    Swal.fire({
        title: 'Processing...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    // AJAX request to submit the form data
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: {
            'selected_room_category': selectedRoomCategory,
            'rate_type': rate_type,
            'rate_price': rate_price,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            Swal.close(); // Close loading indicator

            if (response.redirect_url) {
                Swal.fire({
                    icon: "success",
                    title: "Success",
                    text: "Your selection has been submitted!",
                    timer: 2000,
                    showConfirmButton: false
                }).then(() => {
                    window.location.href = response.redirect_url;
                });
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: response.message || "An error occurred while processing your request.",
                    timer: 2000,
                    showConfirmButton: false
                });
            }
        },
        error: function(xhr) {
            Swal.close(); // Close loading indicator
            let errorMessage = xhr.responseJSON && xhr.responseJSON.message ? xhr.responseJSON.message : "An error occurred!";
            Swal.fire({
                icon: "error",
                title: "Request Failed",
                text: errorMessage,
                timer: 2000,
                showConfirmButton: false
            });
        }
    });
});
