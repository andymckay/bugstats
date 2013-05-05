$(function() {
    $.getJSON('http://localhost:5000/data.json', function(data){
        var tbody = $('#counts tbody')
        data.dates.forEach(function(element, index){
            var row = $('<tr>')
            row.append($('<td>', {
                'text': element,
            }))
            row.append($('<td>', {
                'text': data.count[index],
            }))
            tbody.prepend(row)
        })
    })
})
