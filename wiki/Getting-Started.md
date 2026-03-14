# Getting Started

This guide walks you through installing the PAWS runtime, writing your first `.uwu` program, and running it.

## 1. Install PAWS

See the [Installation](Installation) page for full instructions. The quickest path on Linux/macOS is:

```sh
curl -fsSL https://raw.githubusercontent.com/nathan-sharp/uwu/main/install.sh | sh
```

Verify the install:

```sh
paws version
```

## 2. Write your first program

Create a file called `hello.uwu`:

```
print "Hello, world!"
```

Run it:

```sh
paws run hello.uwu
```

Output:

```
Hello, world!
```

## 3. Variables and arithmetic

```
let x = 10
let y = 3
print x + y
print x - y
print x * y
print x / y
```

Output:

```
13
7
30
3.3333333333333335
```

## 4. Branching with `if`

```
let score = 85

if score >= 90
    print "A"
else
    if score >= 80
        print "B"
    else
        print "C"
    end
end
```

Output:

```
B
```

## 5. Looping with `while`

```
let i = 1
while i <= 5
    print i
    i = i + 1
end
```

Output:

```
1
2
3
4
5
```

## 6. Next steps

- Read the [Language Reference](Language-Reference) to explore the full syntax.
- Browse the [Examples](Examples) page for ready-to-run programs.
- Check the `examples/` directory in the repository for the source files shipped with the project.

## PAWS runtime commands

| Command | Description |
|---------|-------------|
| `paws run <file.uwu>` | Execute a `.uwu` source file |
| `paws help` | Show available commands and the project link |
| `paws version` | Print the installed PAWS version |
| `paws update` | Update PAWS to the latest release |
| `paws uninstall` | Remove PAWS and all PAWS-managed files |
