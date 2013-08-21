$(function() {
  $.getJSON('/stats.json', function(data) {
    if (data.error) {
      $('#graph').append($('<h3>', {text: data.error}))
    } else {
      graph(data.stats)
    }
  })
  $.getJSON('/bugs.json', function(data) {
    if (data.error) {
      $('#bugs').append($('<h3>', {text: data.error}))
    } else {
      var list = $('#bugs')
      data.bugs.forEach(function(element) {
        var item = $('<li>')
        $('<span>', {
          class: 'target_milestone'
        , text: element.target_milestone
        }).appendTo(item)
        item.append(document.createTextNode(': '))

        $('<span>', {
          class: 'priority'
        , text: element.priority
        }).appendTo(item)
        item.append(document.createTextNode(' '))

        $('<span>', {
          class: 'summary'
        , text: element.summary
        }).appendTo(item)
        item.append(document.createTextNode(' ('))

        $('<a>', {
          class: 'bug_link'
        , href: 'https://bugzilla.mozilla.org/show_bug.cgi?id=' + element.id
        , text: 'bug ' + element.id
        }).appendTo(item)
        item.append(document.createTextNode(')'))

        item.appendTo(list)
      })
    }
  })
  $.getJSON('/prs.json', function(data) {
    if (data.error) {
      $('#prs').append($('<h3>', {text: data.error}))
    } else {
      var prs_container = $('#prs')
      data.forEach(function(repo) {
        var container = $('<div>', {class: 'span4'})
        container.append($('<h4>', {text: repo.name}))
        var list = $('<ul>', {class: 'unstyled'})
        container.append(list)
        repo.prs.forEach(function(pr) {
          var item = $('<li>')
          var link = $('<a>', {
            text: pr.number,
            href: pr.url
          })
          item.append(link)
          item.append(document.createTextNode(': ' + pr.title))
          list.append(item)
        })
        prs_container.append(container)
      })
    }
  })
})
