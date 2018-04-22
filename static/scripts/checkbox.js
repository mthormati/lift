$('input[type="checkbox"]').on('click', (event) => {
    url = 'http://localhost:5000/handleCheck'
    data = {
        'workoutId': event.target.dataset.workout,
        'exerciseId': event.target.dataset.exercise,
        'checked': event.target.checked,
    }

    $.ajax(
        {
            type: "POST",
            url: url,
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
        }
    )
})