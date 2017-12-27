package arguments

type Argument struct {
    name string
    description string
    ids []string
    valuesNames []string
    predefinedValues []string
    defaultValues []string
    required bool
    disableRequiredArguments bool
}