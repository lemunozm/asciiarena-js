package main

import "arguments"
import "fmt"

func main() {
    s := Argument{
        name: "asdasd", 
        description: "", 
        ids: {}, 
        valuesNames: {}, 
        predefinedValues: {}, 
        defaultValues: {}, 
        required: false,
        disableRequiredArguments: false
    }
    fmt.Println(s)
}