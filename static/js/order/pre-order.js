preOrderEditBtns = document.querySelectorAll('.preOrderEditBtn')
for (i = 0; i < preOrderEditBtns.length; i++) {
    preOrderEditBtns[i].addEventListener('click', function () {
        let itemId = this.dataset.id
        let quantity = document.getElementById('quantity_' + itemId).value
        let fee = document.getElementById('order_item_fee_' + itemId).value
        let color = document.querySelector('#color_' + itemId).value
        let featureValueSelect = document.querySelectorAll('.featureValueSelect_' + itemId)
        let featureValueIdList = []
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
                        'quantity': quantity, 'color': color, 'fee': fee
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


preOrderDeleteBtns = document.querySelectorAll('.preOrderDeleteBtn')
for (let i = 0; i < preOrderDeleteBtns.length; i++) {
    preOrderDeleteBtns[i].addEventListener('click', function () {
        let itemId = this.dataset.id
        console.log(this.dataset)
        Swal.fire({
            title: 'آیا مطمئنید؟',
            text: "سفارش حذف شود؟",
            icon: 'error',
            showCancelButton: true,
            confirmButtonText: 'بله، حذف کن!',
            cancelButtonText: 'انصراف',
            customClass: {
                confirmButton: 'btn btn-danger me-3',
                cancelButton: 'btn btn-label-secondary'
            },
            buttonsStyling: false
        }).then(async function (result) {
            let response;
            let url;
            let data;
            if (result.value) {
                url = '/fetch/pre-order-delete/'
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({'itemId': itemId})
                })
                data = await response.json()
                Swal.fire({
                    icon: data['status'],
                    title: 'حذف سفارش!',
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

orderDeleteBtns = document.querySelectorAll('.orderDeleteBtn')
for (let i = 0; i < orderDeleteBtns.length; i++) {
    orderDeleteBtns[i].addEventListener('click', function () {
        let itemId = this.dataset.id
        Swal.fire({
            title: 'آیا مطمئنید؟',
            text: "سفارش حذف شود؟",
            icon: 'error',
            showCancelButton: true,
            confirmButtonText: 'بله، حذف کن!',
            cancelButtonText: 'انصراف',
            customClass: {
                confirmButton: 'btn btn-danger me-3',
                cancelButton: 'btn btn-label-secondary'
            },
            buttonsStyling: false
        }).then(async function (result) {
            let response;
            let url;
            let data;
            if (result.value) {
                url = '/fetch/order-delete/'
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({'itemId': itemId})
                })
                data = await response.json()
                Swal.fire({
                    icon: data['status'],
                    title: 'حذف سفارش!',
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

