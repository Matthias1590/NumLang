# NumLang
A stack-oriented programming language written in python.

# Examples
```rust
// Fibonacci in NumLang

var(a, 4)
var(b, 4) push(1) b store
var(c, 4)

push(0) while b load push(100) < do
    b load print

    a load c store // Store a in c

    b load a store // Store b in a

    c load b load + b store // Add c to b

    push(1) +
end pop
```

```rust
// Variables in NumLang

var(age, 1) // Create a variable called age with a size of 1 byte (will be located at address 0)

push(17) age store // Store 17 in the variable age

age load // Load the value stored in age

print // Print the value stored in age


// Variables can be used in loops to keep track of the current iteration
var(i, 2) // Create a variable called i with a size of 3 bytes (will be located at address 1)
var(j, 1)
push(0) while dup push(1000) < do
    i store // Store the current iteration in i

    // Print the number if j is divisible by 11 or i is divisible by 15
    j load push(11) % push(0) ==
    i load push(15) % push(0) ==
    |
    if
        i load print
    end

    j load push(3) +
    j store
    i load push(1) + // Increment i
end pop
```

For more examples, take a look at the numlang/examples folder.
