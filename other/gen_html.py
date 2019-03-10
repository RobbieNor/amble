##!/usr/bin/python 

import os, codecs, glob


def run(title, input_dir, output_dir):
    #Write javascript header to index_html
    index_html = codecs.open(output_dir + "/index.html"	, "wb", "utf-8")
    index_html.write(u"""<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>%s</title>
    </head>
    <frameset cols="27%%, *">
      <frame src=".tree.html">
      <frame name="viewer" src="">
    </frameset>
    </html>
    """ % title)
    index_html.close()
    
    #Write javascript to tree_html    
    tree_html = codecs.open(output_dir + "/.tree.html", "wb", "utf-8")
    tree_html.write(u"""<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
    <h1><center>%s</center></h1>
    <BR>
    <style>
    .node
    {
        padding-left: 20px;
        display: block;
    }
    
    .node_collapsed
    {
        padding-left: 20px;
        display: none;
    
        
        visibility: hidden;
        display: none;
    }
    
    
    
    a:active
    {
    text-decoration:none;
    color: #0000FF;
    font-weight: bold;
    }
    
    a:visited
    {
    text-decoration:none;
    color: #000;
    font-weight: bold;
    }
    
    a:link
    {
    text-decoration:none;
    color: #000;
    font-weight: bold;
    }
    
    a:hover
    {
    text-decoration: underline;
    color: #500;
    font-weight: bold;
    }
    
    </style>
    
    
    <script language="javascript">
      
        var displayStates = [];
    
        function showDiv(div)
        {    
            div.style.height     = "";
            div.style.display    = "block";
            div.style.visibility = "visible";
        }
    
        function hideDiv(div)
        {
            div.style.height     = "0px";
            div.style.display    = "none";      
            div.style.visibility = "hidden";
        }
    
        function toggleDiv(div, defaultState)
        {
    
            // set default on first use
            if (displayStates[div] == undefined)
                displayStates[div] = defaultState;
    
            // toggle state
            displayStates[div] = !displayStates[div];       
    
            // hide / show
            if (displayStates[div])
                showDiv(div);
            else {
                hideDiv(div);
            }
        }
    
        function toggleDivName(divname, defaultState)
        {
            toggleDiv(document.getElementById(divname), defaultState);
        }
    
    </script>
    
    """ % title)
    
    def walk(node):
        
        nodeid = node
        #expand = node.get_attr("expanded", False)
        expand = 0
        skip = False
        if os.path.basename(os.path.normpath(node)) == title:
            expand = 1
            skip = True
	if node == (input_dir + '/index.html') or node == (input_dir + '/.tree.html'):
	    skip = True
        dir_name = os.path.basename(os.path.normpath(node))
        parent_path = os.path.abspath(os.path.join(node, os.pardir))
        pattern = node + '/*'
        pattern = pattern.replace('[','[[]').replace(']','[]]')
        children = glob.glob(pattern)
        children.sort(key = lambda l:(os.path.isfile(l), l))
    
        if skip == False:
            if len(children) > 0:
                tree_html.write(u"""<nobr><tt><a href='javascript: toggleDivName("%s", %s)'>+</a>&nbsp;</tt>""" % (nodeid, [u"false", u"true"][int(expand)]))
            else:
                tree_html.write(u"<nobr><tt>&nbsp;&nbsp;</tt>")
        
        
            if os.path.isdir(node):
                tree_html.write(u"%s</nobr><br/>\n" % dir_name)
            else:
                tree_html.write(u"<a href='%s' target='viewer'>%s</a></nobr><br/>\n" % (node, dir_name))
                
            if len(children) > 0:
                tree_html.write(u"<div id='%s' class='node%s'>" % (node, [u"_collapsed", ""][int(expand)]))
                for child in children:
                    walk(child)
        
                tree_html.write(u"</div>\n")
        else:
            for child in children:
                walk(child)
    
    walk(input_dir)
    tree_html.write(u"""</body></html>""")
    tree_html.close()

	


