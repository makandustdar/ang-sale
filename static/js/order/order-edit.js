$('#customerSelect').on('select2:select', async function (e) {
    userId = e.params.data.id

    response = await fetch(`/fetch/get-user-info/?userId=${userId}`)
    data = await response.json()

    $('#address').html(data['address'])
    if (data['company']) {
        $('#companyName').html(data['company'])
    }
    $('#zipcode').html(data['zipcode'])
    $('#mobileNumber').html(data['mobile'])

});