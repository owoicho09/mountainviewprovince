$('#room-selection-form').on('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    // Gather form data
    let hostel_type_id = $("input[name='hostel_type_id']:checked").val();
    let selected_room_category = $("#selected-room").val();  // Use hidden input value

    let rate_type = $("input[name='hostel_rate']:checked").val();
    let rate_price = $("input[name='hostel_rate']:checked").data("price");
    let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    const isFlexiblePlanChecked = $('.flexible-plan').is(':checked');

    //console.log("Flexible Plan Checked: ", isFlexiblePlanChecked);
    //console.log('---',rate_type)
    //console.log(rate_price)
    //console.log(selected_room_category)

    // Validate room category selection
    if (!hostel_type_id) {
        Swal.fire({
            icon: "warning",
            title: "Selection Missing",
            text: "Please select a Hostel Type category.",
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
            'selected_room_category':selected_room_category,
            'hostel_type_id': hostel_type_id,
            'rate_type': rate_type,
            'rate_price': rate_price,
            'flexible_plan': isFlexiblePlanChecked,

            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            Swal.close(); // Close loading indicator

            if (response.redirect_url) {
                Swal.fire({
                    icon: "success",
                    title: "Success",
                    text: "Booking in progress!",
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
            let errorMessage = xhr.responseJSON && xhr.responseJSON.message
                ? xhr.responseJSON.message
                : "An error occurred!";
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
