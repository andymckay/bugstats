$(function() {
    $.getJSON('/data.json', function(data){
        console.log(JSON.stringify(data.data))
        if (data.data.error) {
            displayError(data.data.error)
        } else {
            dataDisplay(data.data)
            graph(data.data)
        }
    })
})

var dataDisplay = function(data) {
    var tbody = $('#counts tbody')
    data.forEach(function(element, index){
        var row = $('<tr>')
        row.append($('<td>', {
            'text': element.date
        }))
        row.append($('<td>', {
            'text': element.count
        }))
        tbody.prepend(row)
    })
}

var displayError = function(error) {
    $('#graph').append($('h3').text(error))
}