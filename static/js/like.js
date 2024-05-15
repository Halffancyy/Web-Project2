$(document).ready(function() {
    $('.like-btn').click(function() {
        var requestId = $(this).data('request-id');
        var likeUrl = likeRequestUrlTemplate.replace('0', requestId);

        $.ajax({
            url: likeUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token() }}'
            },
            success: function(response) {
                console.log('AJAX Success:', response);  // Add this line for debugging
                if (response.error) {
                    alert(response.error);
                } else {
                    $('button[data-request-id="' + requestId + '"] .badge').text(response.likes);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', status, error);  // Add this line for debugging
                alert('Error liking the request.');
            }
        });
    });
});
