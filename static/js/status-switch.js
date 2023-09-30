statusSwitchBtns = document.querySelectorAll('.statusSwitch')
for (i = 0; i < statusSwitchBtns.length; i++) {
    statusSwitchBtns[i].addEventListener('change', function () {
        id = this.dataset.id
        value = this.checked
        db = this.dataset.db
        if (value) {
            text = 'وضعیت فعال شود؟'
            icon = 'info'
        } else {
            text = 'وضعیت غیرفعال شود؟'
            icon = 'warning'
        }
        Swal.fire({
            title: 'آیا مطمئنید؟',
            text: text,
            icon: icon,
            showCancelButton: true,
            confirmButtonText: 'بله',
            cancelButtonText: 'انصراف',
            customClass: {
                confirmButton: 'btn btn-success me-3',
                cancelButton: 'btn btn-label-secondary'
            },
            buttonsStyling: false
        }).then(async function (result) {
            if (result.value) {
                url = '/fetch/update-status/'
                response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ 'id': id, 'value': value, 'db': db })
                })
                data = await response.json()
                Swal.fire({
                    icon: data['status'],
                    title: 'ویرایش وضعیت!',
                    text: data['text'],
                    customClass: {
                        confirmButton: 'btn btn-success'
                    },
                    confirmButtonText: 'باشه'
                })
            }
        })
    })
}
