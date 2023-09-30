state_select = document.querySelectorAll('.state_select')
for (i = 0; i < state_select.length; i++) {
    state_select[i].addEventListener('change', function () {
        state_id = this.value
        city_id = this.dataset.id
        city_select = document.getElementById('id_city_' + city_id)
        fetch(`/fetch/get-city/?state=${state_id}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                length = city_select.options.length;
                for (i = length - 1; i >= 0; i--) {
                    city_select.options[i] = null;
                }

                for (i = 0; i < data.length; i++) {
                    option = document.createElement('option')
                    option.text = data[i]['fields']['name']
                    option.value = data[i]['pk']
                    city_select.append(option)
                }
            })
    })
}

if (state_select[0].value !== '') {
    selected_state_id = parseInt(state_select[0].value)
    city_select = document.getElementById('id_city_1')
    city_select2 = document.getElementById('id_city_2')
    console.log(city_select.dataset.selected)
    fetch(`/fetch/get-cities/${selected_state_id}/?city_selected=${city_select.dataset.selected}`)
        .then(response => response.json())
        .then(data => {
            length1 = city_select.options.length;
            length2 = city_select2.options.length;

            for (i = length1 - 1; i >= 0; i--) {
                city_select.options[i] = null;
            }
            for (i = length2 - 1; i >= 0; i--) {
                city_select2.options[i] = null;
            }
            let empty_option = document.createElement('option')
            empty_option.value = ''
            empty_option.text = '--------'
            let empty_option2 = document.createElement('option')
            empty_option2.value = ''
            empty_option2.text = '--------'
            city_select.append(empty_option)
            city_select2.append(empty_option2)
            let option;
            let option2;
            for (let i = 0; i < data.length; i++) {
                option = document.createElement('option')
                try {
                    option.text = data[i]['fields']['name']
                    option.value = data[i]['pk']
                    city_select.append(option)
                } catch (e) {
                    city_select.value = data[i]['selected']
                }
            }
            for (let i = 0; i < data.length; i++) {
                option2 = document.createElement('option')
                try {
                    option2.text = data[i]['fields']['name']
                    option2.value = data[i]['pk']
                    city_select2.append(option2)
                } catch (e) {
                    city_select2.value = data[i]['selected']
                }
            }
        })
}