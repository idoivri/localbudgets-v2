Templates = {}
Templates.project_list =  [
"<ul>",
"    {{#each items}}",
"        <li>{{this.name}}</li>",
"    {{/each}}",
"</ul>"
].join("\n");



//<script id="project_list" type="text/x-handlebars-template" src='template.js'></script>
    
