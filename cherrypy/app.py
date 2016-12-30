import cherrypy
import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

class Root():
    content = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<link rel="stylesheet" href="static/jquery-ui-1.12.1/jquery-ui.css" type="text/css" media="screen, projection" />

<script type="text/javascript" src="static/jquery-1.12.4.js" ></script>
<script type="text/javascript" src="static/jquery-ui-1.12.1/jquery-ui.js" ></script>

</head>
<body id="spreadsheet_example">
<div id="example">
	<form id="unitconversion">
	<input name="from" type="text" value="1" />
	<select name="fromunit">
		<option selected="true">inch</option>
		<option>cm</option>
	</select>
	<label for="to">=</label>
	<input name="to" type="text" readonly="true" />
	<select name="tounit">
		<option>inch</option>
		<option selected="true">cm</option>
	</select>
	<button name="convert" type="button" icon="../48007.PNG">convert</button>
	</form>
</div>
 <script type="text/javascript" src="static/unitconverter.js" ></script>
</body>
</html>
'''

    @cherrypy.expose
    def index(self):
        return Root.content

if __name__ == "__main__":
	
	cherrypy.quickstart(Root(),config={
		'/static':
		{ 'tools.staticdir.on':True,
		  'tools.staticdir.dir':os.path.join(current_dir,"static")
		}
	})
