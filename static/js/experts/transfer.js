transformallcustomersBtns = document.querySelectorAll('.transformallcustomers')
for (i = 0; i < transformallcustomersBtns.length; i++) {
    transformallcustomersBtns[i].addEventListener('click', function () {
        itemId = this.dataset.id
        quantity = document.querySelector('#quantity_' + itemId).value
        color = document.querySelector('#color_' + itemId).value
        featureValueSelect = document.querySelectorAll('.featureValueSelect_' + itemId)
        featureValueIdList = []
        featureValueSelect.forEach(item => {
            featureValueIdList.push(item.value)
        })

        Swal.fire({
            title: 'آیا مطمئنید؟',
            text: "سفارش ویرایش شود؟",
            icon: 'info',
            showCancelButton: true,
            confirmButtonText: 'بله، ویرایش کن!',
            cancelButtonText: 'انصراف',
            customClass: {
                confirmButton: 'btn btn-primary me-3',
                cancelButton: 'btn btn-label-secondary'
            },
            buttonsStyling: false
        }).then(async function (result) {
            if (result.value) {
                url = '/fetch/pre-order-edit/'
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'itemId': itemId, 'featureValueIdList': featureValueIdList,
                        'quantity': quantity, 'color': color
                    })
                })
                data = await response.json()
                Swal.fire({
                    icon: data['status'],
                    title: 'ویرایش سفارش!',
                    text: data['text'],
                    customClass: {
                        confirmButton: 'btn btn-success'
                    },
                    confirmButtonText: 'باشه'
                })
                    .then(function (result) {
                        if (result.value) {
                            location.reload()
                        }
                    })

            }
        });

    })
}
