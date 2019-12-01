![Kotlin](./kotlin-1.svg)

# Advent of Code 2019 - in Kotlin!

I'm going to attempt (likely with varying degrees of motivation) to implement all of the advent of code problems in Kotlin. Since VSCode and other IDEs rely on Gradle or MAven at the moment to supply code completion for Kotlin, each day of the advent is a simple Gradle project, but you can run the code without gradle. Either way, you will however, need to have Java installed.

## Running the code

I've included the input file supplied by advent of code for each problem. 

Using gradle, from `<day>`
```
    gradle run -Pinput=input
```


Manually, without gradle, from `<day>/src/main/kotiln`
```
   java -jar Solution.jar ../../../input
```
