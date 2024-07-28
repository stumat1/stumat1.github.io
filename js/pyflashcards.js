const flashcards = [
    { topic: "Variables", info: "Variables in Python are containers for storing data values. You don't need to declare the type of a variable in Python." },
    { topic: "Data Types", info: "Common data types in Python include integers, floats, strings, lists, tuples, sets, and dictionaries." },
    { topic: "Control Flow", info: "Control flow tools in Python include if statements, for and while loops, and try/except blocks." },
    { topic: "Functions", info: "Functions are blocks of reusable code that perform a specific task. They are defined using the def keyword." },
    { topic: "Classes & Objects", info: "Python is an object-oriented programming language. You can create your own classes to encapsulate data and functions." },
    { topic: "Modules", info: "Modules are files containing Python code that can be imported into other Python programs. They help in organizing code." },
    { topic: "List Comprehensions", info: "List comprehensions provide a concise way to create lists. It consists of brackets containing an expression followed by a for clause." },
    { topic: "File I/O", info: "Python allows you to read from and write to files using built-in functions like open(), read(), write(), and close()." },
    { topic: "Exception Handling", info: "Python provides a way to handle errors using try, except, and finally blocks to ensure the program runs smoothly." },
    { topic: "Decorators", info: "Decorators are functions that modify the behavior of other functions or methods. They are often used for logging, access control, etc." },
    { topic: "Generators", info: "Generators are special functions that return an iterable set of items, one at a time, in a special way using the yield keyword." },
    { topic: "Lambda Functions", info: "Lambda functions are small anonymous functions defined with the lambda keyword. They can have any number of arguments but only one expression." },
    { topic: "List Methods", info: "Python lists have several built-in methods like append(), remove(), pop(), sort(), reverse(), and more." },
    { topic: "String Methods", info: "Strings in Python have many built-in methods such as upper(), lower(), strip(), split(), join(), and more." },
    { topic: "Dictionaries", info: "Dictionaries are collections of key-value pairs. Keys must be unique and immutable, while values can be of any data type." },
    { topic: "Set Operations", info: "Sets are unordered collections of unique elements. They support operations like union, intersection, difference, and symmetric difference." },
    { topic: "Inheritance", info: "Inheritance allows a class to inherit attributes and methods from another class, promoting code reuse." },
    { topic: "Polymorphism", info: "Polymorphism allows different classes to be treated as instances of the same class through inheritance. It supports method overriding." },
    { topic: "Recursion", info: "Recursion is a programming technique where a function calls itself. It's useful for tasks that can be defined in terms of similar subtasks." },
    { topic: "Standard Library", info: "Python's standard library is a vast collection of modules and packages that provide pre-written code to help with various tasks." }
];

let currentIndex = 0;

function updateFlashcard() {
    document.getElementById('flashcard-front').textContent = flashcards[currentIndex].topic;
    document.getElementById('flashcard-back').innerHTML = `<p>${flashcards[currentIndex].info}</p>`;
}

function flipCard() {
    document.getElementById('flashcard').classList.toggle('flip');
}

function nextCard() {
    currentIndex = (currentIndex + 1) % flashcards.length;
    updateFlashcard();
    if (document.getElementById('flashcard').classList.contains('flip')) {
        document.getElementById('flashcard').classList.remove('flip');
    }
}

function prevCard() {
    currentIndex = (currentIndex - 1 + flashcards.length) % flashcards.length;
    updateFlashcard();
    if (document.getElementById('flashcard').classList.contains('flip')) {
        document.getElementById('flashcard').classList.remove('flip');
    }
}

// Initialize the first flashcard
updateFlashcard();