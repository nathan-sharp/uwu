# Examples

Annotated example programs that demonstrate the UWU language features.

All examples can be run with:

```sh
paws run <filename>.uwu
```

---

## Hello, world

The simplest possible program.

```
print "Hello, world!"
```

**Output:**

```
Hello, world!
```

---

## Basic arithmetic

```
let x = 2
let y = 3
print x + y * 10
print "uwu online"
```

Because `*` has higher precedence than `+`, `y * 10` is evaluated first, giving `30`, then `2 + 30 = 32`.

**Output:**

```
32
uwu online
```

> Source: `examples/hello.uwu`

---

## Variable reassignment

Variables can be updated after they are declared.

```
let total = 1
total = total + 41
print total
```

**Output:**

```
42
```

> Source: `examples/reassign.uwu`

---

## FizzBuzz

A classic programming exercise — print numbers 1 through 15, replacing multiples of 3 with "fizz", multiples of 5 with "buzz", and multiples of 15 with "fizzbuzz".

```
print "PAWS FizzBuzz (1..15)"

let i = 1

while i <= 15
    if (i % 15) == 0
        print "fizzbuzz"
    else
        if (i % 3) == 0
            print "fizz"
        else
            if (i % 5) == 0
                print "buzz"
            else
                print i
            end
        end
    end

    i = i + 1
end
```

**Output:**

```
PAWS FizzBuzz (1..15)
1
2
fizz
4
buzz
fizz
7
8
fizz
buzz
11
fizz
13
14
fizzbuzz
```

> Source: `examples/fizzbuzz.uwu`

---

## Counting down

```
let n = 5
while n > 0
    print n
    n = n - 1
end
print "Lift off!"
```

**Output:**

```
5
4
3
2
1
Lift off!
```

---

## String concatenation

The `+` operator joins two strings.

```
let first = "Hello"
let second = ", world!"
print first + second
```

**Output:**

```
Hello, world!
```

---

## Comparison and branching

```
let a = 10
let b = 20

if a == b
    print "equal"
else
    if a < b
        print "a is smaller"
    else
        print "a is larger"
    end
end
```

**Output:**

```
a is smaller
```

---

## Summing a range

Calculate the sum of integers from 1 to 100.

```
let sum = 0
let i = 1
while i <= 100
    sum = sum + i
    i = i + 1
end
print sum
```

**Output:**

```
5050
```
