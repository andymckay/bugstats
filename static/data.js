$(function() {
    $.getJSON('http://localhost:5000/data.json', function(data){
        console.log(JSON.stringify(data.data))
        dataDisplay(data.data)
        graph(data.data)
    })
})

var dataDisplay = function(data) {
    var tbody = $('#counts tbody')
    data.forEach(function(element, index){
        var row = $('<tr>')
        row.append($('<td>', {
            'text': element.date,
        }))
        row.append($('<td>', {
            'text': element.count,
        }))
        tbody.prepend(row)
    })
}
