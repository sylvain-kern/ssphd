async function getJson() {
    let docs;
    const res = await fetch('./documents.json')
    docs = await res.json();
    return docs
};

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

function displayResults(results) {

}

function clearResults() {
    list.innerHTML = ''
};

function ctrl_k(e)  {
    if (e.ctrlKey && e.which == 75) {
        if(focused) {
            searchField.blur();
            focused = false;
        } else {
            e.preventDefault();
            searchField.focus();
            focused = true;
        };
    } else if (e.key == "Escape") {
        searchField.blur();
        focused = false;
    };
};

document.addEventListener('keydown', ctrl_k, false);
searchField.addEventListener('focus', function(e) {
    resultsContainer.classList.remove('inactive');
})

searchField.addEventListener('blur', function(e) {
    resultsContainer.classList.add('inactive');
});

getJson().then(docs => {
    const idx = lunr(function() {
        this.ref('link');
        this.field('title', {boost: 10});
        this.field('content', {boost: 1});
        // this.pipeline.remove(lunr.stemmer);
        this.pipeline.remove(lunr.stopWordFilter);

        this.metadataWhitelist = ['position'];

        docs.forEach( function (doc) {
            this.add(doc)
        }, this);
    });

    searchField.addEventListener('input', (e) => {

        clearResults();

        let query = e.target.value + '~1';
        results = idx.search(query);

        console.log(results);

        var results_full = results.map(function (item) {
            return docs.filter(function (query, index, arr) {
                return query.link == item.ref;
            })[0];
        });

        console.log(results_full);

        for (const [result, result_full] of zip([results, results_full])) {

            // creating a li element for each result item
            const resultItem = document.createElement('li');

            // adding a class to each item of the results
            resultItem.classList.add('result-item');

            resultTitle = document.createElement('div');
            resultContent = document.createElement('div');

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


            console.log('matched terms')
            console.log(matchedTerms);
            console.log('matched fields')
            console.log(matchedFields);
            console.log('matched positions')
            console.log(matchedPositions);

            var title = result_full.title;
            var text = result_full.content;
            var rest = text;
            var offset = 0
            console.log(matchedPositions.length);

            matchedPositions[0].forEach(function (matchedPosition) {
                textBefore = rest.slice(0, matchedPosition[0] - offset)
                textMarked = rest.slice(matchedPosition[0] - offset, matchedPosition[0] + matchedPosition[1]- offset);
                rest = rest.slice(matchedPosition[0] + matchedPosition[1] - offset, rest.length);
                resultContent.appendChild(document.createTextNode(textBefore));
                mark = document.createElement('mark');
                mark.appendChild(document.createTextNode(textMarked));
                resultContent.appendChild(mark);
                offset = matchedPosition[0] + matchedPosition[1];
            });

            resultContent.appendChild(document.createTextNode(rest));

            // var rest = title;

            // matchedPositions[1].forEach(function (matchedPosition) {
            //     titleBefore = rest.slice(0, matchedPosition[0] - offset)
            //     titleMarked = rest.slice(matchedPosition[0] - offset, matchedPosition[0] + matchedPosition[1]- offset);
            //     rest = rest.slice(matchedPosition[0] + matchedPosition[1] - offset, rest.length);
            //     resultTitle.appendChild(document.createTextNode(textBefore));
            //     mark = document.createElement('mark');
            //     mark.appendChild(document.createTextNode(titleMarked));
            //     resultTitle.appendChild(mark);
            //     offset = matchedPosition[0] + matchedPosition[1];
            // });

            resultTitle.appendChild(document.createTextNode(title))
            resultItem.appendChild(resultTitle);
            resultItem.appendChild(resultContent);

            list.appendChild(resultItem);
        }

    });
});