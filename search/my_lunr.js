var search_index = `
[
    {
       "level": 1,
        "title": "1 Chapter title",
        "link": "./my_link.html",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales*. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."
    },
    {
        "level": 2,
        "title": "1.1 Section title",
        "link": "./my_link_2.html",
        "text": "Let’s see an example of how it feels to use a simple Potluck document. Below is a simple recipe for making coffee, which includes an interactive slider that can scale up the number of servings. The demo starts out as a video, but if you click on it you can interact with a live version. Chapter title"
    }
]
`;

search_index = JSON.parse(search_index);

let idx = lunr(function() {
    this.ref('link');
    this.field('title', 5);
    this.field('text', 1);

    search_index.forEach( function (doc) {
        this.add(doc)
    }, this);
});

results = idx.search('lorem');

console.log('Results: ', results.length);
console.log(results);

var results_full = results.map(function (item) {
    return search_index.filter(function (query, index, arr) {
        return query.link == item.ref;
    })[0];
});
console.log(results_full);

const searchField = document.querySelector('.search-field');

searchField.addEventListener('input', (e) => {

    clearResults();

    let query = e.target.value;

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

    words = [...new Set(query.split(" "))]; // remove duplicates
    var starred_words = [];
    var exact_words = [];
    for (const word of words) {
        if (word != "") {
            starred_words.push('*' + word + '*');
            exact_words.push(word)
        }
    }

    query = [starred_words.join(" "), exact_words.join(" ")].join(' ') // add partial words w/ full words

    console.log(query)

    // searching in lunr index if query is not empty

    if (query != '' && query != ' ') {

        results = idx.search(query);
        console.log(results);
        var results_full = results.map(function (item) {
            return search_index.filter(function (query, index, arr) {
                return query.link == item.ref;
            })[0];
        });
        console.log(results_full);
        displayResults(results, results_full);
    }
    else {
        results = []
    }

});


function displayResults(results, results_full) {


    for (const result of results_full) {
        // creating a li element for each result item
        const resultItem = document.createElement('li')

        // adding a class to each item of the results
        resultItem.classList.add('result-item')


        const title = document.createTextNode(result.title)
        const text = document.createTextNode(result.text)
        const ref = result.link

        searchLinkContainer = document.createElement("a");
        searchResultContainer = document.createElement("div");
        searchResultContainer.classList.add('search-result-container')
        searchTitleContainer = document.createElement("span");
        searchTextContainer = document.createElement("span");
        searchLinkContainer.href = ref
        searchTitleContainer.appendChild(title)
        searchTextContainer.appendChild(text)

        searchResultContainer.appendChild(searchTitleContainer)
        searchResultContainer.appendChild(searchTextContainer)
        searchLinkContainer.appendChild(searchResultContainer)
        resultItem.appendChild(searchLinkContainer)

        list.appendChild(resultItem)

    }
}

function clearResults() {
    list.innerHTML = ''
}