async function getJson(path) {
    let docs;
    const res = await fetch(path);
    docs = await res.json();
    return docs;
};

const searchDiv = document.querySelector('.searchbar');
const searchField = document.querySelector('.searchbar > input');
const resultsContainer = document.querySelector('.results-container');
resultsContainer.classList.add("inactive");
var focused = false

function* zip(arrays) {
    let iterators = arrays.map(a => a[Symbol.iterator]());
    while (true) {
        let results = iterators.map(it => it.next());
        if (results.some(r => r.done)) return;
        yield results.map(r => r.value);
    }
}

function clearResults() {
    list.innerHTML = ''
};

function ctrl_k(e) {
    if (e.ctrlKey && e.which == 75) {
        if (focused) {
            searchField.blur();
            focused = false;
        } else {
            e.preventDefault();
            searchField.focus();
            searchField.select();
            focused = true;
        };
    } else if (e.key == "Escape") {
        searchField.blur();
        resultsContainer.classList.add('inactive');
        focused = false;
    };
};

document.addEventListener("click", function(event) {
    if (event.target.closest(".searchbar-container")) return
    resultsContainer.classList.add('inactive');
})
document.addEventListener('keydown', ctrl_k, false);
searchField.addEventListener('focus', function (e) {
    resultsContainer.classList.remove('inactive');
})


function displayResultFull (field, item, rest, fieldsPositions) {
    var offset = 0;
    fieldsPositions[item].forEach(matchedPosition => {
        textBefore = rest.slice(0, matchedPosition[0] - offset);
        textMarked = rest.slice(matchedPosition[0] - offset, matchedPosition[0] + matchedPosition[1] - offset);
        rest = rest.slice(matchedPosition[0] + matchedPosition[1] - offset, rest.length);
        field.appendChild(document.createTextNode(textBefore));
        mark = document.createElement('mark');
        mark.appendChild(document.createTextNode(textMarked));
        field.appendChild(mark);
        offset = matchedPosition[0] + matchedPosition[1];
    });
    sp = document.createElement('span');
    sp.appendChild(document.createTextNode(rest));  
    field.appendChild(sp)
};

function displayResult (field, item, rest, fieldsPositions) {

    headChars = 80,

    position = fieldsPositions[item][0]

    start = Math.max(position[0] - headChars, 0);
    end = Math.min(start+260)

    textBefore = rest.slice(start, position[0]);
    textMarked = rest.slice(position[0], position[0] + position[1]);
    textAfter = rest.slice(position[0] + position[1], end);

    mark = document.createElement('mark');
    sp =  document.createElement('span')
    
    if (start > 0) {
        sp.appendChild(document.createTextNode('…'))
    }
    mark.appendChild(document.createTextNode(textMarked));


    sp.appendChild(document.createTextNode(textBefore));
    sp.appendChild(mark);
    sp.appendChild(document.createTextNode(textAfter));
    if (end < rest.length) {
        sp.appendChild(document.createTextNode('…'));
    }
    field.appendChild(sp);
}

function displayResultDefault (field, rest) {
    start = 0;
    end = Math.min(start+260);

    sp = document.createElement('span');

    if(end > rest.length) {
        sp.appendChild(document.createTextNode(rest));
    } else {
        sp.appendChild(document.createTextNode(rest.slice(start, end)+'…'));
    };

    field.appendChild(sp);
}

getJson('./_assets/documents.json').then(docs => {
    const idx = lunr(function () {
        this.ref('link');
        this.field('title', { boost: 10 });
        this.field('content', { boost: 1 });

        this.pipeline.remove(lunr.stopWordFilter);

        this.metadataWhitelist = ['position'];

        docs.forEach(function (doc) {
            this.add(doc)
        }, this);
    });

    // const idx = lunr.Index.load(index);

    searchField.addEventListener('input', (e) => {

        clearResults();

        let query = e.target.value + '~1 ' + e.target.value + '*';
        results = idx.search(query.replace(/\s+$/, ''));

        var results_full = results.map(function (item) {
            return docs.filter(function (query, index, arr) {
                return query.link == item.ref;
            })[0];
        });

        for (const [result, result_full] of zip([results, results_full])) {

            function get_field(field) {
                switch (field) {
                    case 'title': return resultTitle;
                    case 'content': return resultContent;
                };
            };
            function get_result_full(field) {
                switch (field) {
                    case 'title': return result_full.title;
                    case 'content': return result_full.content;
                };
            };

            // creating a li element for each result item
            const resultItem = document.createElement('li');

            const resultLink = document.createElement('a');

            resultLink.href = result_full['link'];

            // adding a class to each item of the results
            resultItem.classList.add('result-item');

            resultTitle = document.createElement('div');
            resultTitle.classList.add('search-result-title');

            if (result_full.number != null) {
                numberSpan = document.createElement('span');
                numberSpan.classList.add('search-result-number')
                numberSpan.appendChild(document.createTextNode(result_full.number))
                resultTitle.append(numberSpan)
            }
            resultContent = document.createElement('div');
            resultContent.classList.add('search-result-content');

            var matchedTerms = []
            var matchedFields = []
            var matchedPositions = []
            Object.keys(result.matchData.metadata).forEach(term => {
                matchedTerms.push(term);
                Object.keys(result.matchData.metadata[term]).forEach(field => {
                    matchedFields.push(field)
                    matchedPositions.push(result.matchData.metadata[term][field].position);
                });
            });

            resultItemLayout = ['title', 'content'];

            var fieldsPositions = new Object;

            matchedFields.map(function (e, i) {
                fieldsPositions[e] = matchedPositions[i];
            });

            resultItemLayout.forEach(item => {

                var field = get_field(item);
                var rest = get_result_full(item);

                if (matchedFields.includes(item)) {
                    displayResult(field, item, rest , fieldsPositions);
                } else {
                    displayResultDefault(field, rest);
                };
                resultLink.appendChild(field);
            });
            resultItem.appendChild(resultLink)
            list.appendChild(resultItem);
        };
    });
});