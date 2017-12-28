package common

import "fmt"

type Argument struct {
	Name                     string
	Description              string
	Ids                      []string
	ValuesName               []string
	PredefinedValues         []string
	DefaultValues            []string
	Required                 bool
	DisableRequiredArguments bool

	defined bool
	values  []string
}

type ArgumentList struct {
	appName    string
	arguments  map[string]*Argument
	parseError bool
}

func NewArgumentList() *ArgumentList {
	return &ArgumentList{
		appName:    "",
		arguments:  map[string]*Argument{},
		parseError: false,
	}
}

func (list *ArgumentList) Add(argument *Argument) {
	list.arguments[argument.Name] = argument
	list.arguments[argument.Name].values = argument.DefaultValues
}

func (list *ArgumentList) Parse(args []string) (parseError bool) {
	fmt.Println(len(args))
	//TODO
	return true
}
