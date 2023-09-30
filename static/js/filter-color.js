filterColorRadio = document.querySelectorAll('.filterColor')

filterColorRadio.forEach(element => {
    element.addEventListener('change', async function () {
        productId = this.value
        productName = this.dataset['name']
        // let {request} = this.dataset
        response = await fetch(`/fetch/filter-color/?productId=${productId}&productName=${productName}`)
        data = await response.json()
        $('#colorDiv').html(data['data'])
    })
});