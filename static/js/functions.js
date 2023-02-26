baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

$(document).ready(function () {

    // Toggle device status
    $(".toggle-btn").click(function () {
        var device_id = this.value;
        var btn = $(this)
        if (device_id) {
            $.ajax({
                url: baseURL + '/change_device_status/' + device_id,
                method: 'GET',
                contentType: "application/json",
                beforeSend: function () {
                },
                success: function (data) {
                    console.log(data)
                    if (data["success"]) {
                        $($(btn).find('.toggle-div')[0]).toggle();
                        $($(btn).find('.toggle-div')[1]).toggle();
                    }
                },
                error: function (jqXHR, ex) {
                    alert("Error")
                }
            })
        }
    })
})