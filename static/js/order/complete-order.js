adminCompleteOrderBtns = document.querySelectorAll('.adminCompleteOrder')
for (i = 0; i < adminCompleteOrderBtns.length; i++) {
    adminCompleteOrderBtns[i].addEventListener('click', function () {
        action = this.dataset.action
        orderId = this.dataset.orderid

        if (action == 'cancel') {
            text = 'سفارش لفو شود؟'
            icon = 'danger'
            confirmBtnClass = 'btn btn-danger me-3'
        } else {
            text = 'سفارش تکمیل شود؟'
            icon = 'success'
            confirmBtnClass = 'btn btn-success me-3'
        }
        Swal.fire({
            title: 'آیا مطمئنید؟',
            text: text,
            icon: icon,
            showCancelButton: true,
            confirmButtonText: 'بله!',
            cancelButtonText: 'انصراف',
            customClass: {
                confirmButton: confirmBtnClass,
                cancelButton: 'btn btn-label-secondary'
            },
            buttonsStyling: false
        }).then(async function (result) {
            if (result.value) {
                url = '/fetch/order-complete/'
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ 'orderId': orderId, 'action': action })
                })
                data = await response.json()
                Swal.fire({
                    icon: data['status'],
                    title: data['title'],
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