productRadioBtns = document.querySelectorAll('.productRadioBtn')

for (i = 0; i < productRadioBtns.length; i++) {
    productRadioBtns[i].addEventListener('change', async function () {
        productId = this.value
        allCustomOptionDiv = document.querySelectorAll('.custom-option')
        clickedCustomOptionDiv = this.closest('.custom-option')

        if (allCustomOptionDiv.length > 1) {
            clickedCustomOptionDiv = this.closest('.custom-option')

            allCustomOptionDiv.forEach(element => {
                element.classList.remove('checked')
            });
            clickedCustomOptionDiv.classList.add('checked')
        }

        response = await fetch(`/fetch/get-product-features/?productId=${productId}`)
        data = await response.json()
        $('#feature_div').html(data['data'])
    })

}