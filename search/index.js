const people = [
    { name: 'adri'},
    { name: 'becky'},
    { name: 'chris'},
    { name: 'dillon'},
    { name: 'evan'},
    { name: 'frank'},
    { name: 'georgette'},
    { name: 'hugh'},
    { name: 'igor'},
    { name: 'jacoby'},
    { name: 'kristina'},
    { name: 'lemony'},
    { name: 'matilda'},
    { name: 'nile'},
    { name: 'ophelia'},
    { name: 'patrick'},
    { name: 'quincy'},
    { name: 'roslyn'},
    { name: 'solene'},
    { name: 'timothy'},
    { name: 'uff'},
    { name: 'violet'},
    { name: 'wyatt'},
    { name: 'x'},
    { name: 'yadri'},
    { name: 'zack'},
]

const searchInput = document.querySelector('.input')

searchInput.addEventListener("input", (e) => {
    // inside, we will need to achieve a few things:
    // 1. declare and assign the value of the event's target to a variable AKA whatever is typed in the search bar
    let value = e.target.value

    // 2. check: if input exists and if input is larger than 0
    if (value && value.trim().length > 0){
        // 3. redefine 'value' to exclude white space and change input to all lowercase
         value = value.trim().toLowerCase()
        // 4. return the results only if the value of the search is included in the person's name
        // we need to write code (a function for filtering through our data to include the search input value)
    } else {
        // 5. return nothing
        // input is invalid -- show an error message or show no results

    }

})

const clearButton = document.getElementById('clear')

clearButton.addEventListener("click", () => {
    // 1. write a function that removes any previous results from the page
    clearList()
})

function setList(results){

    for (const person of results){
        // creating a li element for each result item
        const resultItem = document.createElement('li')

        // adding a class to each item of the results
        resultItem.classList.add('result-item')

        // grabbing the name of the current point of the loop and adding the name as the list item's text
        const text = document.createTextNode(person.name)

        // appending the text to the result item
        resultItem.appendChild(text)

        // appending the result item to the list
        list.appendChild(resultItem)
    }
}

searchInput.addEventListener("input", (e) => {
    let value = e.target.value

    if (value && value.trim().length > 0){
         value = value.trim().toLowerCase()

        //returning only the results of setList if the value of the search is included in the person's name
        setList(people.filter(person => {
            return person.name.includes(value)
        }))
    }
})


function clearList() {
    list.innerHTML = ''
}



function noResults(){
    // create an element for the error; a list item ("li")
    const error = document.createElement('li')
    // adding a class name of "error-message" to our error element
    error.classList.add('error-message')

    // creating text for our element
    const text = document.createTextNode('No results found. Sorry!')
    // appending the text to our element
    error.appendChild(text)
    // appending the error to our list element
    list.appendChild(error)
}

function setList(results){
    clearList()
    for (const person of results){
        const resultItem = document.createElement('li')
        resultItem.classList.add('result-item')
        const text = document.createTextNode(person.name)
        resultItem.appendChild(text)
        list.appendChild(resultItem)
    }

    if (results.length === 0 ){
        noResults()
    }
}

