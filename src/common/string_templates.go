package common

func HelpCliTemplate() string {
	var name string = "NAME:\n    {{.Name}} - {{.Usage}}\n\n"
	var version string = "VERSION\n    {{.Version}}\n\n"
	var usage string = "USAGE:\n    {{.HelpName}} {{if .VisibleFlags}}[options]{{end}}\n    {{if len .Commands}}\n"
	var options string = "OPTIONS:\n    {{range .VisibleFlags}}{{.}}\n    {{end}}{{end}}{{if .Copyright }}\n"
	var endTemplate string = "{{end}}"
	return name + version + usage + options + endTemplate
}
