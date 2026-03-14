# Language Reference

Complete reference for the UWU language as implemented in the current prototype.

---

## Source files

UWU programs are plain-text files with the `.uwu` extension. They are encoded as UTF-8. Each statement occupies its own line; a semicolon (`;`) may be used as an alternative line terminator.

---

## Comments

> **Not yet supported.** Comments will be added in a future version.

---

## Types

UWU currently has two value types:

| Type | Description | Example literals |
|------|-------------|-----------------|
| Number | 64-bit floating-point value | `42`, `3.14`, `0` |
| String | UTF-8 text | `"hello"`, `"line\none"` |

Numbers that have no fractional part are displayed without a decimal point (e.g. `10.0` is printed as `10`).

---

## Literals

### Number literals

```
42
3.14
0
```

### String literals

String literals are enclosed in double quotes. The following escape sequences are recognised:

| Escape | Meaning |
|--------|---------|
| `\n` | Newline |
| `\t` | Horizontal tab |
| `\"` | Double quote |
| `\\` | Backslash |

```
"Hello, world!"
"line one\nline two"
"tab\there"
"she said \"hi\""
```

---

## Operators

### Arithmetic

Arithmetic operators work on two Number operands.

| Operator | Operation | Example |
|----------|-----------|---------|
| `+` | Addition | `x + 1` |
| `-` | Subtraction | `x - 1` |
| `*` | Multiplication | `x * 2` |
| `/` | Division | `x / 4` |
| `%` | Modulo (remainder) | `x % 3` |

The `+` operator also concatenates two String values:

```
let greeting = "Hello, " + "world!"
print greeting
```

Mixing a Number and a String with any operator is a runtime error.

### Comparison

Comparison operators return `1` (true) or `0` (false) as a Number. They work on two Numbers or two Strings.

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |

### Operator precedence

From highest to lowest:

| Level | Operators |
|-------|-----------|
| 1 (highest) | `*`, `/`, `%` |
| 2 | `+`, `-` |
| 3 | `<`, `<=`, `>`, `>=` |
| 4 (lowest) | `==`, `!=` |

Use parentheses to override precedence:

```
let result = (2 + 3) * 4
```

---

## Variables

### Declaration — `let`

```
let <name> = <expression>
```

Declares a new variable and assigns it an initial value. Variables are globally scoped for the lifetime of the program. Re-declaring a variable that already exists overwrites it.

```
let x = 10
let message = "ready"
```

### Reassignment

```
<name> = <expression>
```

Assigns a new value to an existing variable. Assigning to an undeclared name is a runtime error.

```
x = x + 1
message = "done"
```

---

## Statements

### `print`

```
print <expression>
```

Evaluates the expression and writes its value to standard output, followed by a newline.

```
print 42
print "hello"
print x + y
```

### `if` / `else` / `end`

```
if <condition>
    <statements>
end

if <condition>
    <statements>
else
    <statements>
end
```

Executes the `then` branch when the condition is truthy (non-zero number or non-empty string), otherwise the `else` branch (if present). `else` branches can be nested to form `else if` chains.

```
if x > 0
    print "positive"
else
    if x == 0
        print "zero"
    else
        print "negative"
    end
end
```

### `while` / `end`

```
while <condition>
    <statements>
end
```

Repeats the body as long as the condition is truthy.

```
let i = 0
while i < 10
    print i
    i = i + 1
end
```

---

## Truthiness

A value is **truthy** when:

- It is a Number and not equal to `0`.
- It is a String and not equal to `""` (empty string).

A value is **falsy** when it is `0` or `""`.

---

## Errors

The runtime reports three categories of errors:

| Category | Trigger |
|----------|---------|
| **Lex error** | An unrecognised character in the source |
| **Parse error** | A token that does not fit the grammar |
| **Runtime error** | Undefined variable, type mismatch, division by zero, etc. |

All errors print a message to standard error and exit with a non-zero status code.
