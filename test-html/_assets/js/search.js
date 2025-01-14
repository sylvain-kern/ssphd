var search_index = `
[
    {
        "level": 1,
        "title": "1 Chapter title",
        "link": "./my_link.html",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales*. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit.",
        "parent": null
    },
    {
        "level": 2,
        "title": "1.1 Section title",
        "link": "./my_link_2.html",
        "content": "Let’s see an example of how it feels to use a simple Potluck document. Below is a simple recipe for making coffee, which includes an interactive slider that can scale up the number of servings. The demo starts out as a video, but if you click on it you can interact with a live version. Chapter title",
        "parent": "1 Chapter title"
    }
]
`;

search_index = JSON.parse(search_index);

console.log("\n============\nSEARCH INDEX:")
console.log(search_index)

let idx = lunr(function() {
    this.ref('link');
    this.field('title', {boost: 5});
    this.field('content', {boost: 1});

    this.metadataWhitelist = ['position'];

    search_index.forEach( function (doc) {
        this.add(doc)
    }, this);
});

const searchField = document.querySelector('.searchbar > input');
const resultsContainer = document.querySelector('.results-container');
resultsContainer.classList.add("inactive");


searchField.addEventListener('input', (e) => {

    clearResults();

    let query = e.target.value;

    if (query == "") {
        searchField.classList.remove("typing");
        resultsContainer.classList.add("inactive");
    } else {
        searchField.classList.add("typing");
        resultsContainer.classList.remove("inactive");
    };

    // search query formatting

    if (query && query.trim().length > 0){
        // 3. redefine 'query' to exclude white space and change input to all lowercase
         query = query.trim().toLowerCase()
        // 4. return the results only if the query of the search is included in the person's name
        // we need to write code (a function for filtering through our data to include the search input query)
    } else {
        // 5. return nothing
        // input is invalid -- show an error message or show no results

    }

    // 1. just add stars to word to match any string in the content field

    // 2. concatenate words and starred words in a list

    // words = [...new Set(query.split(" "))]; // remove duplicates
    // var starred_words = [];
    // var exact_words = [];
    // for (const word of words) {
    //     if (word != "") {
    //         starred_words.push('*' + word + '*');
    //         exact_words.push(word)
    //     }
    // }

    // query = [starred_words.join(" "), exact_words.join(" ")].join(' ') // add partial words w/ full words

    // searching in lunr index if query is not empty

    const initialQuery = query;
    console.log('\n=====\nQUERY:');
    console.log(query);

    if (query != '' && query != ' ') {

        query = query + '*';

        results = idx.search(query);
        var results_full = results.map(function (item) {
            return search_index.filter(function (query, index, arr) {
                return query.link == item.ref;
            })[0];
        });
        displayResults(results, results_full, initialQuery);
    }
    else {
        results = []
    }
});

function* zip(arrays) {
    let iterators = arrays.map(a => a[Symbol.iterator]());
    while (true) {
      let results = iterators.map(it => it.next());
      if (results.some(r => r.done)) return;
      yield results.map(r => r.value);
    }
}

function displayResults(results, results_full, initialQuery) {

    console.log(results);

    const queryLength = initialQuery.length;

    for (const [result, result_full] of zip([results, results_full])) {

        console.log('\nRESULT:')

        var matched_terms = [];
        var matched_fields = [];
        var matched_positions = [];

        // getting info on the matched query
        Object.keys(result.matchData.metadata).forEach(term => {
            matched_terms.push(term);
            Object.keys(result.matchData.metadata[term]).forEach(field => {
                matched_fields.push(field)
                matched_positions.push(result.matchData.metadata[term][field].position);
            });
        });

        console.log('matched terms')
        console.log(matched_terms);
        console.log('matched positions')
        console.log(matched_positions);

        const matched_term = matched_terms[0];
        const matched_term_length = matched_term.length;
        const first_position = matched_positions[0][0][0];

        console.log('first position')
        console.log(first_position);

        const matchingSpan = document.createElement('span');
        matchingSpan.classList.add('match');

        // creating a li element for each result item
        const resultItem = document.createElement('li');

        // adding a class to each item of the results
        resultItem.classList.add('result-item');

        if (result_full.parent != null) {
            var parent = document.createTextNode("~ › " + result_full.parent + " ›");
        } else {
            var parent = document.createTextNode("~ ›");
        };
        const title = document.createTextNode(result_full.title);
        let text = result_full.content;

        var matchingSpanMargin = 80;

        slicedtext = [
            '…' + text.slice(Math.max(first_position - matchingSpanMargin, 0),first_position),
            text.slice(first_position, first_position + queryLength),
            text.slice(first_position + queryLength, first_position + queryLength + matchingSpanMargin) + '…'
        ];
        matchingSpan.innerText = slicedtext[1];

        let textNode = document.createElement('span');

        textNode.appendChild(document.createTextNode(slicedtext[0]));
        textNode.appendChild(matchingSpan);
        textNode.appendChild(document.createTextNode(slicedtext[2]));

        const ref = result_full.link;

        const searchLinkContainer = document.createElement("a");
        const searchResultContainer = document.createElement("div");
        const searchTitleContainer = document.createElement("div");
        const searchTextContainer = document.createElement("div");
        const pathContainer = document.createElement("div");

        pathContainer.classList.add('search-result-path');
        searchResultContainer.classList.add('search-result-container');
        searchTitleContainer.classList.add("search-result-title");
        searchTextContainer.classList.add("search-result-text");

        searchLinkContainer.href = ref;

        searchTitleContainer.appendChild(title);
        searchTextContainer.appendChild(textNode);
        pathContainer.appendChild(parent);

        searchResultContainer.appendChild(pathContainer)
        searchResultContainer.appendChild(searchTitleContainer);
        searchResultContainer.appendChild(searchTextContainer);
        searchLinkContainer.appendChild(searchResultContainer);
        resultItem.appendChild(searchLinkContainer);

        list.appendChild(resultItem);
    };
    console.log('results length')
    console.log(results.length);
    if (results.length == 0) {
        const emptyResult = document.createElement('div');
        emptyResult.classList.add('empty');
        const emptyResultSpan = document.createElement("span");
        emptyResultSpan.innerText = 'No results found for “' + initialQuery + '”.';
        emptyResult.appendChild(emptyResultSpan);
        list.appendChild(emptyResult);
    }
}

function clearResults() {
    list.innerHTML = ''
}

var focused = false

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
}

document.addEventListener('keydown', ctrl_k, false);
searchField.addEventListener('focus', function(e) {
    resultsContainer.classList.remove('inactive');
});
searchField.addEventListener('blur', function(e) {
    resultsContainer.classList.add('inactive');
});