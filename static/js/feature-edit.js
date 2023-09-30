featureValueEditBtns = document.querySelectorAll('.featureValueEditBtn')
for (i = 0; i < featureValueEditBtns.length; i++) {
    featureValueEditBtns[i].addEventListener('click', function () {
        id = this.dataset.id
        name = document.querySelector('#name_' + id).value
        code = document.querySelector('#code_' + id).value
        product = document.querySelector('#product_' + id).value
        // priority = document.querySelector('#priority_' + id).value

        Swal.fire({
            title: 'آیا مطمئنید؟',
            text: "مشخصه محصول ویرایش شود؟",
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
                url = '/fetch/featurevalue-edit/'
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ 'id': id, 'name': name, 'code': code, 'product': product })
                })
                data = await response.json()
                Swal.fire({
                    icon: data['status'],
                    title: 'ویرایش مشخصه محصول!',
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